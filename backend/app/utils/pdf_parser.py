from typing import Tuple
from pathlib import Path
import fitz  # PyMuPDF


def extract_text_from_pdf(path: str) -> Tuple[str, int]:
    """Extract full text and page count from a PDF file using PyMuPDF.

    Args:
        path: path to pdf file
    Returns:
        tuple(full_text, page_count)
    """
    doc = fitz.open(path)
    texts = []
    for page in doc:
        texts.append(page.get_text())
    full_text = "\n".join(texts)
    return full_text, doc.page_count
