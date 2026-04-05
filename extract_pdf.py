#!/usr/bin/env python3
import PyPDF2
import sys

def extract_pdf_text(pdf_path):
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page_num, page in enumerate(reader.pages, 1):
                text += f"\n--- 第 {page_num} 页 ---\n"
                text += page.extract_text() or "[无法提取文本]"
            return text
    except Exception as e:
        return f"错误: {e}"

if __name__ == "__main__":
    for pdf_file in sys.argv[1:]:
        print(f"\n{'='*60}")
        print(f"文件: {pdf_file}")
        print('='*60)
        print(extract_pdf_text(pdf_file))
