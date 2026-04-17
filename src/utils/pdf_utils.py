import fitz
import base64

def get_pdf_pages(attachments):
    pages = []

    for att in attachments:
        if att.get("contentType", "").startswith("application/pdf"):
            content = base64.b64decode(att.get("contentBytes", ""))
            doc = fitz.open(stream=content, filetype="pdf")

            for page in doc:
                pages.append(page.get_text())

    return pages if pages else [""]