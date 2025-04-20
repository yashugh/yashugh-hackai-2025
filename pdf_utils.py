# -----------------------------
# FILE: pdf_utils.py
# -----------------------------
import fitz  # PyMuPDF
import os
import tempfile
from PIL import Image
import pytesseract
import io
import re

def clean_text(text):
    """Clean extracted text to remove unnecessary whitespace and formatting."""
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    # Remove unnecessary line breaks
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    # Remove multiple consecutive line breaks
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def extract_text_and_tables_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    full_text = ""
    tables = []
    extracted_image_text = []
    
    # Get total pages for progress reporting
    total_pages = len(doc)
    
    # Process only the first 30 pages if document is very large
    max_pages = min(30, total_pages)
    
    for page_num in range(max_pages):
        page = doc[page_num]
        
        # Extract text
        page_text = page.get_text()
        full_text += page_text
        
        # Identify potential tables
        blocks = page.get_text("blocks")
        for b in blocks:
            if "\t" in b[4] or b[4].count(" ") > 10:
                # Only include reasonably sized tables
                if len(b[4]) < 2000:  # Limit table size
                    tables.append(b[4])
        
        # Extract images (limit to first 10 pages to avoid processing too many images)
        if page_num < 10:
            image_list = page.get_images(full=True)
            
            # Process only up to 3 images per page to prevent overload
            for img_index, img in enumerate(image_list[:3]):
                try:
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    # Convert to PIL Image
                    image = Image.open(io.BytesIO(image_bytes))
                    
                    # Skip very small images (likely icons or decorations)
                    if image.width < 100 or image.height < 100:
                        continue
                    
                    # Extract text from image using OCR
                    img_text = pytesseract.image_to_string(image)
                    if img_text.strip() and len(img_text) > 20:  # Only add substantial text
                        extracted_image_text.append(f"Image text (page {page_num+1}): {img_text}")
                except Exception as e:
                    print(f"OCR error on page {page_num+1}, image {img_index+1}: {e}")
    
    doc.close()
    
    # Clean the extracted text
    full_text = clean_text(full_text)
    
    # Add image text if available
    if extracted_image_text:
        full_text += "\n\n" + "\n".join(extracted_image_text)
    
    # Limit the total text length to prevent token overflows
    if len(full_text) > 100000:
        full_text = full_text[:100000] + "\n\n[Document truncated due to size limitations]"
    
    # Limit the number of tables 
    tables = tables[:20]  # Maximum 20 tables
    
    return full_text, tables