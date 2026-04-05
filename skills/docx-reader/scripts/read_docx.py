#!/usr/bin/env python3
"""
DOCX Reader - Extract text content from Word documents
Usage: python3 read_docx.py <docx_file> [output_txt_file]
"""

import sys
import os

def read_docx(file_path):
    """Extract text from DOCX file using python-docx or docx2txt"""
    try:
        # Try python-docx first
        try:
            from docx import Document
            doc = Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return '\n'.join(full_text)
        except ImportError:
            pass
        
        # Fallback to docx2txt
        try:
            import docx2txt
            return docx2txt.process(file_path)
        except ImportError:
            pass
        
        # Last resort: unzip and read word/document.xml
        import zipfile
        from xml.etree import ElementTree as ET
        
        with zipfile.ZipFile(file_path, 'r') as z:
            xml_content = z.read('word/document.xml')
        
        tree = ET.fromstring(xml_content)
        
        # Define namespace
        namespaces = {
            'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
        }
        
        # Extract text from all paragraphs
        paragraphs = []
        for paragraph in tree.findall('.//w:p', namespaces):
            texts = [node.text for node in paragraph.findall('.//w:t', namespaces) if node.text]
            if texts:
                paragraphs.append(''.join(texts))
        
        return '\n'.join(paragraphs)
        
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def read_doc(file_path):
    """Extract text from legacy DOC file using antiword or textract"""
    try:
        # Try textract
        try:
            import textract
            return textract.process(file_path).decode('utf-8', errors='ignore')
        except ImportError:
            pass
        
        # Try antiword via subprocess
        import subprocess
        result = subprocess.run(['antiword', file_path], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error with antiword: {result.stderr}"
            
    except FileNotFoundError:
        return "Error: antiword not installed. Install with: brew install antiword"
    except Exception as e:
        return f"Error reading DOC: {str(e)}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 read_docx.py <docx_file> [output_txt_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
    
    # Determine file type and read
    if input_file.lower().endswith('.docx'):
        content = read_docx(input_file)
    elif input_file.lower().endswith('.doc'):
        content = read_doc(input_file)
    else:
        print(f"Error: Unsupported file format. Use .docx or .doc")
        sys.exit(1)
    
    # Output
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Content saved to: {output_file}")
    else:
        print(content)

if __name__ == '__main__':
    main()
