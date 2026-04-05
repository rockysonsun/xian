---
name: docx-reader
description: Read and extract text content from Microsoft Word documents (.docx and .doc files). Use when the user needs to read, extract, or convert Word documents to plain text. Supports both modern DOCX format and legacy DOC format. Handles text extraction, formatting preservation, and batch processing.
---

# DOCX Reader

Extract text content from Microsoft Word documents (.docx, .doc).

## Quick Start

```bash
# Extract text from DOCX
python3 ~/.openclaw/workspace/skills/docx-reader/scripts/read_docx.py document.docx

# Save to file
python3 ~/.openclaw/workspace/skills/docx-reader/scripts/read_docx.py document.docx output.txt
```

## Installation

First time use - install dependencies:

```bash
bash ~/.openclaw/workspace/skills/docx-reader/scripts/install.sh
```

This installs:
- `python-docx` - Modern DOCX handling
- `docx2txt` - Alternative DOCX parser
- Optional: `antiword` for legacy .doc files (install separately with `brew install antiword`)

## Usage Patterns

### Single File Extraction

```python
# In Python code
import subprocess
result = subprocess.run(
    ['python3', 'skills/docx-reader/scripts/read_docx.py', 'file.docx'],
    capture_output=True, text=True
)
text_content = result.stdout
```

### Batch Processing

```bash
# Convert all DOCX files in directory
for file in *.docx; do
    python3 skills/docx-reader/scripts/read_docx.py "$file" "${file%.docx}.txt"
done
```

### Handling Different Encodings

The script automatically handles UTF-8. For files with Chinese characters or other non-ASCII text, the output is properly encoded.

## Supported Formats

| Format | Extension | Support Level |
|--------|-----------|---------------|
| Word 2007+ | .docx | Full support |
| Word 97-2003 | .doc | Requires antiword |

## Troubleshooting

### "Module not found" error
Run the install script first:
```bash
bash skills/docx-reader/scripts/install.sh
```

### Legacy .doc files not working
Install antiword:
```bash
brew install antiword
```

### Chinese characters garbled
The script outputs UTF-8. If reading the output file, ensure your editor uses UTF-8 encoding.

## Alternative: Direct Python Usage

```python
# If python-docx is installed
try:
    from docx import Document
    doc = Document('file.docx')
    text = '\n'.join([p.text for p in doc.paragraphs])
except ImportError:
    # Fallback to script
    import subprocess
    result = subprocess.run(
        ['python3', 'skills/docx-reader/scripts/read_docx.py', 'file.docx'],
        capture_output=True, text=True
    )
    text = result.stdout
```
