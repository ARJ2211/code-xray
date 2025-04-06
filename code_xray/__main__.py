import typer
from pathlib import Path
from code_xray.viewer import CodeViewerApp

app = typer.Typer()

@app.command()
def view(
    file: Path = typer.Argument(..., help="Path to the source code file."),
    model: str = typer.Option("mistral", "--model", "-m", help="Ollama model to use (e.g., mistral, llama3)"),
    port: int = typer.Option(11434, "--port", "-p", help="Port where Ollama is running"),
):
    """Launch the code-xray viewer for a given file, with model and port options."""
    if not file.exists():
        typer.echo(f"[Error] File not found: {file}")
        raise typer.Exit(1)

    CodeViewerApp(file_path=file, model=model, port=port).run()

if __name__ == "__main__":
    app()
