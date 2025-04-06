import typer
from pathlib import Path
from code_xray.viewer import CodeViewerApp  # updated import if inside code_xray/

app = typer.Typer()

@app.command()
def view(file: Path):
    """Launch code-xray viewer for a given file."""
    if not file.exists():
        typer.echo(f"[Error] File not found: {file}")
        raise typer.Exit(1)
    CodeViewerApp(file_path=file).run()

if __name__ == "__main__":
    app()
