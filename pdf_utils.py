import fitz  # PyMuPDF

def extract_text_from_pdf(file):
    """
    Extracts all text from the uploaded PDF using PyMuPDF.
    :param file: Uploaded PDF file (from Streamlit uploader)
    :return: Extracted plain text (string)
    """
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in pdf:
        text += page.get_text()
    return text

