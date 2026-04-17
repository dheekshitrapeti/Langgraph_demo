# src/models/state.py

from typing import TypedDict, Any, List


# -------------------------------
# Base Email Metadata
# -------------------------------
class EmailMetadata(TypedDict):
    msg_id: str
    conversation_id: str
    from_email: str
    to_email: str
    subject: str
    body: str
    attachments: List[dict]
    status: str


# -------------------------------
# Classified Email (after classification)
# -------------------------------
class ClassifiedEmail(EmailMetadata, total=False):
    service: str
    sub_service: str  
    classification_confidence: float


# -------------------------------
# Extraction Result
# -------------------------------
class ExtractionResult(TypedDict, total=False):
    invoice_page_index: int
    invoice_data: dict
    line_items: List[dict]
    extraction_confidence: float
    used_fallback: bool


# -------------------------------
# Root Graph State
# -------------------------------
class RootState(TypedDict, total=False):
    raw_emails: List[EmailMetadata]
    batches: List[List[EmailMetadata]]
    classified_results: List[ClassifiedEmail]


# -------------------------------
# Classification State (per email)
# -------------------------------
class ClassificationState(TypedDict, total=False):
    email: EmailMetadata             
    text_content: str
    service: str
    sub_service: str                 
    classification_confidence: float 
    reason: str
    extracted_email: str


# -------------------------------
# Extraction State (per email)
# -------------------------------
class ExtractionState(TypedDict, total=False):  
    email: ClassifiedEmail
    invoice_page_index: int
    invoice_page_content: Any
    extracted_data: dict
    line_items: List[dict]
    extraction_confidence: float
    used_fallback: bool