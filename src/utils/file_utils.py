

import base64
import fitz


def extract_text_from_pdf_bytes(file_bytes):
    text = ""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            text += page.get_text()
    except:
        pass
    return text[:4000]


def decode_attachment(att):
    return base64.b64decode(att.get("contentBytes", ""))