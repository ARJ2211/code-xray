from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import VerticalScroll
from textual.reactive import reactive
from rich.text import Text
from rich.syntax import Syntax
from pathlib import Path

class Line(Static):
    def __init__(self, number: int, content: str, language: str = "python"):
        self.number = number
        self.content = content
        self.language = language
        super().__init__()
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
        ("q", "quit", "Quit"),
        ("up", "cursor_up", "Move Up"),
        ("down", "cursor_down", "Move Down"),
        ("shift+up", "select_up", "Select Up"),
        ("shift+down", "select_down", "Select Down"),
    ]

    current_line = reactive(0)
    selection_start = reactive(0)

    def __init__(self, file_path: Path):
        super().__init__()
        self.file_path = file_path
        self.code_lines = self.file_path.read_text(encoding="utf-8").splitlines()
        self.language = file_path.suffix.lstrip(".") or "python"
        self.container = VerticalScroll()
        self.line_widgets = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield self.container
        yield Footer()

    async def on_mount(self) -> None:
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
        self.call_after_refresh(lambda: self.container.scroll_to_widget(self.line_widgets[self.current_line]))

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
