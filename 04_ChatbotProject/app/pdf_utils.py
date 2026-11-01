# Extractor Function to basically extract all the text from the PDF files.

from pypdf import PdfReader

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        # Extract text from each page, add a newline character to separate pages and concatenates everything into 'text'.
        text += page.extract_text() + "\n" # Example: "Welcome to Page 1\nThis is Page 2\nEnd of Page 3\n"
    return text