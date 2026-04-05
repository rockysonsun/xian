#!/bin/bash
# Install dependencies for docx-reader skill

echo "Installing docx-reader dependencies..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Install Python packages
echo "Installing python-docx and docx2txt..."
pip3 install --user python-docx docx2txt 2>/dev/null || pip install --user python-docx docx2txt 2>/dev/null

# Check for antiword (for .doc files)
if ! command -v antiword &> /dev/null; then
    echo ""
    echo "Note: antiword is not installed (needed for .doc files)"
    echo "Install with: brew install antiword"
fi

echo ""
echo "Installation complete!"
echo "Usage: python3 scripts/read_docx.py <file.docx> [output.txt]"
