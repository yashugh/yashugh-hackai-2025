# pdf_utils.py
import fitz  # PyMuPDF

def extract_pdf_text(uploaded_file):
    """
    Takes a Streamlit‐uploaded file (bytes) and returns all text.
    """
    # open the PDF from the uploaded file’s bytes
    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = []
    for page in pdf:
        text.append(page.get_text())
    return "\n".join(text)
