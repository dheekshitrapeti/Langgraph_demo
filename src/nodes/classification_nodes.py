

from src.services.classification_service import classification_service
from src.utils.file_utils import decode_attachment, extract_text_from_pdf_bytes


def extract_text(state: dict):
    # 🔥 ALWAYS preserve email
    email = state.get("email", {})

    attachments = email.get("attachments", [])

    if not attachments:
        return {
            "email": email,         
            "text_content": ""
        }

    att = attachments[0]
    file_bytes = decode_attachment(att)

    text = extract_text_from_pdf_bytes(file_bytes)

    return {
        "email": email,             
        "text_content": text
    }


def classify_document(state: dict):
    email = state.get("email", {})  

    filename = email.get("msg_id", "unknown")

    result = classification_service.classify(
        filename,
        state.get("text_content", "")
    )

    return {
        "email": email, 
        "service": result.get("service", "Host Country"),
        "sub_service": result.get("sub_service", "Unknown"),
        "confidence": result.get("confidence", "Low"),
        "reason": result.get("reason", ""),
        "extracted_email": result.get("email"),
    }