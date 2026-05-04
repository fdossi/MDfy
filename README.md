# MDfy

Batch conversion of PDF files to Markdown using Microsoft MarkItDown.

## Requirements

- Python 3.9+
- `markitdown` package

Install dependency:

```powershell
pip install markitdown
```

## Script

Main script: `mdfy.py`

Usage:

```powershell
python mdfy.py <input_folder> [output_folder]
```

- `input_folder`: folder with PDF files (search is recursive)
- `output_folder` (optional): destination for `.md` files
	- if omitted, output is written under `input_folder`

## Behavior

- Skips files already converted (`.md` exists)
- Detects duplicate PDFs by SHA-256 content hash and ignores duplicates
- Preserves relative subfolder structure in output to avoid filename collisions

Example:

- `input/a/report.pdf` -> `output/a/report.md`
- `input/b/report.pdf` -> `output/b/report.md`

## Examples (Windows / PowerShell)

Run from this repo folder:

```powershell
python .\mdfy.py "D:\zotero-pdfs\Microplasticos" ".\markdown"
```

Run from another VS Code window (or any folder):

```powershell
python "C:\Users\fabio\OneDrive\Documentos\GitHub\MDfy\MDfy\mdfy.py" "." ".\markdown"
```

In the second example, `.` means the current folder where you run the command.