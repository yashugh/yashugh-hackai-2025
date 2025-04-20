# -----------------------------
# FILE: pdf_utils.py
# -----------------------------
import fitz  # PyMuPDF

def extract_text_and_tables_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    full_text = ""
    tables = []

    for page in doc:
        full_text += page.get_text()
        blocks = page.get_text("blocks")
        for b in blocks:
            if "\t" in b[4] or b[4].count(" ") > 10:
                tables.append(b[4])

    doc.close()
    return full_text, tables