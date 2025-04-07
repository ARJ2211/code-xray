import httpx
import asyncio
from pathlib import Path
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, RichLog
from textual.containers import VerticalScroll, Vertical
from textual.reactive import var
from rich.text import Text
from rich.syntax import Syntax


class ExplanationScreen(Screen):
    BINDINGS = [
        Binding("q", "close", "Close"),
        Binding("escape", "close", "Close"),
    ]

    def __init__(self):
        super().__init__()
        self.rich_log = RichLog(highlight=True, markup=True, wrap=True)

    def compose(self) -> ComposeResult:
        yield Vertical(self.rich_log)

    def update_text(self, new_text: str):
        self.rich_log.clear()
        self.rich_log.write("[dim]Press Q or Esc to close[/dim]\n")
        self.rich_log.write(new_text)
        self.rich_log.scroll_home(animate=False)

    def action_close(self):
        self.app.pop_screen()
        self.app.set_focus(None)


class Line(Static):
    can_focus = False

    def __init__(self, number: int, content: str, language: str = "python"):
        super().__init__()
        self.number = number
        self.content = content
        self.language = language
        self.update_style(False)

    def update_style(self, is_selected: bool):
        syntax = Syntax(self.content, self.language, theme="monokai", line_numbers=False)
        highlighted = list(syntax.highlight(self.content))
        text = Text.assemble((f"{self.number:>4}    ", "bold dim"), *highlighted)
        if is_selected:
            text.stylize("reverse")
        self.update(text)


class CodeViewerApp(App):
    CSS = """
    VerticalScroll {
        overflow: auto;
        height: 1fr;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("h", "cursor_up", "Move Up"),
        Binding("l", "cursor_down", "Move Down"),
        Binding("H", "select_up", "Shift+H to select up", show=True),
        Binding("L", "select_down", "Shift+L to select down", show=True),
        Binding("e", "explain", "Explain Code"),
        Binding("b", "back_to_tree", "Back to Tree"),  # NEW
    ]

    current_line = var(0)
    selection_start = var(0)

    def __init__(self, file_path: Path, model: str, port: int):
        super().__init__()
        self.title = "Code X-Ray"
        self.file_path = file_path
        self.model = model
        self.port = port
        self.code_lines = file_path.read_text().splitlines()
        self.language = file_path.suffix.lstrip(".") or "python"
        self.container = VerticalScroll()
        self.line_widgets = []
        self.explanation_screen = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield self.container
        yield Footer(show_command_palette=False)

    async def on_mount(self):
        for i, line in enumerate(self.code_lines):
            widget = Line(i + 1, line, self.language)
            self.line_widgets.append(widget)
            await self.container.mount(widget)
        self.highlight_lines()
        self.set_focus(None)

    def highlight_lines(self):
        low = min(self.selection_start, self.current_line)
        high = max(self.selection_start, self.current_line)
        for i, widget in enumerate(self.line_widgets):
            widget.update_style(low <= i <= high)
        self.call_after_refresh(
            lambda: self.container.scroll_to_widget(self.line_widgets[self.current_line])
        )

    def action_cursor_up(self):
        if self.current_line > 0:
            self.current_line -= 1
            self.selection_start = self.current_line
            self.highlight_lines()

    def action_cursor_down(self):
        if self.current_line < len(self.code_lines) - 1:
            self.current_line += 1
            self.selection_start = self.current_line
            self.highlight_lines()

    def action_select_up(self):
        if self.current_line > 0:
            self.current_line -= 1
            self.highlight_lines()

    def action_select_down(self):
        if self.current_line < len(self.code_lines) - 1:
            self.current_line += 1
            self.highlight_lines()

    def action_explain(self):
        self.explanation_screen = ExplanationScreen()

        low = min(self.selection_start, self.current_line)
        high = max(self.selection_start, self.current_line)
        selected_code = "\n".join(self.code_lines[low:high + 1])
        full_context = "\n".join(self.code_lines)

        prompt = f"""
        You are a helpful coding assistant.
        Here is the full file for context:
        ```{self.language}
        {full_context}
        ```

        Now explain only the selected lines:
        ```{self.language}
        {selected_code}
        ```
        """

        self.explanation_screen.update_text("[yellow]Loading explanation...[/yellow]")
        self.push_screen(self.explanation_screen)
        self.run_worker(self.send_to_ollama(prompt), exclusive=True)

    async def send_to_ollama(self, prompt: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"http://localhost:{self.port}/api/generate",
                    json={"model": self.model, "prompt": prompt, "stream": False},
                    timeout=30
                )
                result = response.json()
                text = result.get("response", "").strip() or "[red]No explanation received.[/red]"
                await asyncio.sleep(0.1)
                if self.explanation_screen:
                    self.explanation_screen.update_text(text)
        except Exception as e:
            if self.explanation_screen:
                self.explanation_screen.update_text(f"[red]Error:[/red] {e}")

    def action_back_to_tree(self):
        self.exit(None)
