"""
Utilities for extracting text from PDF documents.
"""

import logging
from pathlib import Path # turns paths into smart objects that know how to do things themselves

"""
Without pathlib: a path is just a string like "documents/notes.txt". To do anything with it, you 
call separate functions (os.path.exists(...), open(...), os.path.join(...)) and pass the string.

With pathlib: a path is a Path object. It carries its own methods (my_file.exists(), 
my_file.read_text(), Path("documents") / "notes.txt") etc.
"""

from pypdf import PdfReader

# Configure logging 
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger(__name__)

# (pdf_file: str | Path) -> str: is a Python type hint which tells that the input pdf_file can be 
# either a regular text string (like "/documents/file.pdf") OR a pathlib.Path object and it will 
# return a string of text
def extract_text_from_pdf(pdf_file: str | Path) -> str:
    """
    Extract text from a PDF file and return it as a single string.
    
    Args:
        pdf_file: Path to the PDF file.
        
    Returns:
        Extracted text from all pages, separated by newline characters.
        
    Raises:
        FileNotFoundError: If the PDF file does not exist.
        Exception: If PDF parsing or text extraction fails.
    """
    
    try:
        pdf_path = Path(pdf_file) # converts pdf_file into a Path object so that we can methods like .is_file(), .exists() etc.
        
        if not pdf_path.is_file(): # .is_file() returns True only if the path exists and is a regular file and not a directory
            raise FileNotFoundError(f"PDF file not found: {pdf_path}") # {pdf_path} gets replaced with the actual path value to makes the error message include the exact path that failed

        reader = PdfReader(pdf_path) # to open and parse the PDF

        extracted_pages = []

        # loops over every page in the PDF, giving you both the page object and its number
        for page_number, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() # Returns the visible text as a string, returns None if no text is found on the page

            extracted_pages.append(page_text or "") # adds the page's text to the list, if page_text is None, it adds an empty string instead

            logger.debug("Extracted text from page %d", page_number) # Logs a debug message with the page number

        extracted_text = "\n".join(extracted_pages) # joined all the page text currently in the list into a single string separated by newline characters

        logger.info("Successfully extracted text from %s (%d pages).", pdf_path, len(reader.pages))

        return extracted_text

    except FileNotFoundError:
        logger.exception("File not found: %s", pdf_file)
        raise

    except Exception:
        logger.exception("PDF extraction failed: %s", pdf_file)
        raise

# Testing this file directly from here
# if __name__ == "__main__":

    # pdf_file = Path("medical_history_1.pdf")
    # pdf_file = r"C:\Users\Dell\Downloads\medical_history_1.pdf"
    # pdf_file = Path(r"05_Assignments\sample_data\medical_history_1.pdf") # relative path did not worked
    # pdf_file = Path(r"C:\Users\AdityaRajPanda\OneDrive - Cubastion Consulting Pvt Ltd\Desktop\genai-bootcamp\05_Assignments\sample_data\medical_history_1.pdf")

    # try:
    #     extracted_text = extract_text_from_pdf(pdf_file)

    #     print("\n========== EXTRACTED PDF TEXT ==========\n")
    #     print(extracted_text)
    #     print("\n========== EXTRACTION COMPLETED ==========")
    
    # except Exception as error:
    #     print(f"Pdf extraction has failed: {error}")
        
