---
name: office-reader
description: Read Microsoft Office documents (.doc, .docx, .xls, .xlsx) and extract text content. Use when the user needs to read Word or Excel files from the workspace. Supports extracting text from documents, paragraphs, tables, and spreadsheets.
---

# Office Reader

Read Microsoft Office documents and extract text content.

## Supported Formats

- **Word**: .docx (recommended), .doc (requires antiword or textract)
- **Excel**: .xlsx (recommended), .xls (requires xlrd)

## Prerequisites

Install required Python packages:

```bash
pip install python-docx openpyxl xlrd
```

For .doc files (optional):
```bash
# macOS
brew install antiword

# Or use textract
pip install textract
```

## Usage

### Reading Word Documents

```bash
python skills/office-reader/scripts/read_office.py /path/to/document.docx
```

Output includes:
- All paragraph text
- Table content (formatted as text)

### Reading Excel Spreadsheets

```bash
python skills/office-reader/scripts/read_office.py /path/to/spreadsheet.xlsx
```

Output includes:
- All worksheet names
- All row data (formatted as text)
- Empty cells are shown as blank

## Example Workflow

When user asks to read an Office file:

1. Check if the file exists in workspace
2. Run the read_office.py script with the file path
3. Display the extracted content to the user

Example:
```bash
# Check file exists
ls -la document.docx

# Read content
python skills/office-reader/scripts/read_office.py document.docx
```

## Limitations

- .doc files require additional tools (antiword or textract)
- Formatting (fonts, colors, styles) is not preserved, only text content
- Images in documents are not extracted
- Complex Excel formulas show calculated values, not formulas
