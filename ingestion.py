import os
from pypdf import PdfReader


def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF.

    Returns:
        str: Extracted text
    """

    reader = PdfReader(file_path)

    text = ""

    for page_number, page in enumerate(reader.pages, start=1):

        page_text = page.extract_text()

        if page_text:
            text += f"\n--- Page {page_number} ---\n"
            text += page_text

    return text


def load_documents(folder_path):
    """
    Load all PDFs from a folder.

    Returns:
        list of dictionaries
    """

    documents = []

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for filename in os.listdir(folder_path):

        if filename.lower().endswith(".pdf"):

            file_path = os.path.join(folder_path, filename)

            text = extract_text_from_pdf(file_path)

            documents.append(
                {
                    "source": filename,
                    "text": text
                }
            )

    return documents