![code-xray](https://github.com/user-attachments/assets/620738dd-8dfc-4fec-abf3-a2259ba090c7)

# 🧠 code-xray

`code-xray` is a terminal-based code exploration and explanation tool powered by local LLMs (like Ollama).  
Select lines of code interactively, send them for explanation, and get human-friendly insights – right in your terminal.

<img src="assets/detail.gif" alt="Demo" width="600" height="400" />

---

## ✨ Features

- ✅ Terminal-based file viewer with syntax highlighting
- ✅ Line-by-line navigation and selection
- ✅ Integration with local LLMs via [Ollama](https://ollama.com)
- ✅ On-demand code explanation using selected lines and full-file context
- ✅ Works fully offline
- ✅ Customizable LLM model and port via CLI

---

## 🚀 Usage

### 1. Basic Command

```bash
code-xray /path/to/your/file.py
```

This opens an interactive terminal interface to browse and explain code.

### 2. With Custom Model and Port

```bash
code-xray /path/to/your/file.py --model mistral --port 11434
```

- `--model` or `-m`: LLM model name (e.g. `mistral`, `llama3`, `codellama`)
- `--port` or `-p`: Port where Ollama is running (default is `11434`)

---

## 🧭 Keybindings

| Key       | Action                  |
| --------- | ----------------------- |
| `h`       | Move up one line        |
| `l`       | Move down one line      |
| `Shift+h` | Expand selection up     |
| `Shift+l` | Expand selection down   |
| `e`       | Explain selected code   |
| `q`       | Quit viewer or popup    |
| `Esc`     | Close explanation popup |

---

## 🛠 Requirements

- Python 3.10+
- [Ollama](https://ollama.com) running locally with desired model pulled

Example to pull a model:

```bash
ollama pull mistral
```

Then ensure it's running:

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
