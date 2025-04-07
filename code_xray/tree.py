# code_xray/tree.py

from textual.app import App, ComposeResult
from textual.widgets import Tree, Footer, Header
from textual.containers import Container
from pathlib import Path
from code_xray.viewer import CodeViewerApp

class FilePickerApp(App):
    CSS = """
    VerticalScroll {
        overflow: auto;
        height: 1fr;
    }
    """

    BINDINGS = [("q", "quit", "Quit the tree viewer")]

    def __init__(self, model: str, port: int):
        super().__init__()
        self.title = 'code-xray'
        self.model = model
        self.port = port
        self.tree_widget = None  # Will be assigned in compose()

    def compose(self) -> ComposeResult:
        self.tree_widget = Tree(f"🌳 Current Dir: {Path.cwd()}")
        self.populate_tree(self.tree_widget.root, Path.cwd())
        yield Header(show_clock=True)
        yield Container(self.tree_widget)
        yield Footer()

    def populate_tree(self, node, path: Path):
        # Dynamically update the label at the top
        node.label = f"🌳 Current Dir: {path}"

        try:
            if path.parent != path:
                up_node = node.add("🔙 ../", data=path.parent)
                up_node.allow_expand = True

            for entry in sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
                if entry.name.startswith("."):
                    continue  # Skip hidden files
                label = f"📁 {entry.name}" if entry.is_dir() else f"📄 {entry.name}"
                child = node.add(label, data=entry)
                if entry.is_dir():
                    child.allow_expand = True
        except PermissionError:
            pass

    async def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        node = event.node
        path = node.data
        if path and path.is_dir() and not node.children:
            self.populate_tree(node, path)

    async def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        path = event.node.data
        if path:
            if path.is_file():
                self.exit(path)
            elif path.is_dir():
                # Clear current tree view
                for child in list(self.tree_widget.root.children):
                    child.remove()

                # Update label and populate contents
                self.populate_tree(self.tree_widget.root, path)
                self.tree_widget.root.expand()

    def action_quit(self):
        self.exit(None)

def launch_directory_tree(model: str = "mistral", port: int = 11434):
    while True:
        selected_path = FilePickerApp(model=model, port=port).run()
        if selected_path:
            result = CodeViewerApp(file_path=selected_path, model=model, port=port).run()
            if result is None:
                continue  # go back to the tree
            else:
                break  # viewer exited with return value
        else:
            break  # user pressed 'q' in tree viewer
