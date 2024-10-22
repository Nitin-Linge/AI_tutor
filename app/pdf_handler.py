from PyPDF2 import PdfReader
import re

def extract_text_from_pdf(file_path: str, max_pages: int = 10) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page_num in range(min(max_pages, len(reader.pages))):
        page = reader.pages[page_num]
        text += page.extract_text()

    processed_text = re.sub(r'\s+', ' ', text).strip()
    return processed_text