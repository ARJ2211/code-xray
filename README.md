<p align="center">
  <img src="https://raw.githubusercontent.com/ARJ2211/code-xray/main/assets/code-xray.png" alt="code-xray logo"/>
</p>

# 🧠 code-xray

`code-xray` is a terminal-based code exploration and explanation tool powered by local LLMs (like Ollama).  
Select lines of code interactively, send them for explanation, and get human-friendly insights – right in your terminal.

<p align="center">
  <img src="assets/detail.gif" alt="Demo" width="600" height="400" />
</p>

---

## ✨ Features

- ✅ Terminal-based file viewer with syntax highlighting
- ✅ Line-by-line navigation and selection
- ✅ Interactive directory tree when run without arguments
- ✅ Integration with local LLMs via [Ollama](https://ollama.com)
- ✅ On-demand code explanation using selected lines and full-file context
- ✅ Works fully offline
- ✅ Switch between file viewer and file tree (`b` to go back)
- ✅ Customizable LLM model and port via CLI

---

## 🚀 Usage

### 1. Launch without arguments

```bash
code-xray
```

This opens a **directory tree** starting from your current working directory.  
You can navigate folders and open files for explanation. Press `b` inside a viewer to return to the file tree.

### 2. Launch with a file directly

```bash
code-xray /path/to/your/file.py
```

This opens an interactive terminal interface to browse and explain code.

### 3. Launch with custom model and port

```bash
code-xray /path/to/your/file.py --model mistral --port 11434
```

- `--model` or `-m`: LLM model name (e.g. `mistral`, `llama3`, `codellama`)
- `--port` or `-p`: Port where Ollama is running (default is `11434`)

---

## 🧭 Keybindings

| Key       | Action                       |
| --------- | ---------------------------- |
| `h`       | Move up one line             |
| `l`       | Move down one line           |
| `Shift+h` | Expand selection up          |
| `Shift+l` | Expand selection down        |
| `e`       | Explain selected code        |
| `b`       | Go back to file tree         |
| `q`       | Quit viewer or popup         |
| `Esc`     | Close explanation popup      |
| `Enter`   | Select file or enter folder  |
| `../`     | Navigate up in the file tree |

---

## 🛠 Requirements

- Python 3.10+
- [Ollama](https://ollama.com) running locally with your preferred model

Example to pull a model:

```bash
ollama pull mistral
```

Then start the server:

```bash
ollama serve
```

---

## 🧩 Installation

```bash
pip install code-xray
```

> Make sure `code-xray` is available in your PATH or create an alias.

---

## 🙌 Acknowledgements

- [Textual](https://github.com/Textualize/textual) for the beautiful terminal UI
- [Ollama](https://ollama.com) for local model hosting
- [Rich](https://github.com/Textualize/rich) for the syntax highlighting

---

## 🔗 Contributions

Pull requests welcome! Feel free to fork and build on top of this.
