from src.models.state import ExtractionState
from src.services.llm_client import llm_client
from src.utils.pdf_utils import get_pdf_pages
from src.config import settings


def identify_invoice_page(state: ExtractionState):
    pages = get_pdf_pages(state["email"]["attachments"])

    try:
        result = llm_client.identify_invoice_page(pages)
        return {"invoice_page_index": result.get("page_index", 0)}
    except:
        return {"invoice_page_index": 0}


def detach_invoice_page(state: ExtractionState):
    pages = get_pdf_pages(state["email"]["attachments"])
    idx = state.get("invoice_page_index", 0)

    return {
        "invoice_page_content": pages[idx] if idx < len(pages) else pages[0]
    }


def extract_invoice_details(state: ExtractionState):
    try:
        result = llm_client.extract_invoice(
            state["invoice_page_content"]
        )

        return {
            "extracted_data": result,
            "line_items": result.get("line_items", []),
            "extraction_confidence": float(result.get("confidence", 0)),
            "used_fallback": False,
        }

    except:
        return {
            "extracted_data": {},
            "line_items": [],
            "extraction_confidence": 0.0,
            "used_fallback": False,
        }


def extraction_router(state: ExtractionState):
    confidence = float(state.get("extraction_confidence", 0.0))

    if confidence < settings.EXTRACTION_CONFIDENCE_THRESHOLD:
        return "fallback"

    return "end"


def fallback_extract(state: ExtractionState):
    try:
        result = llm_client.extract_invoice(
            state["invoice_page_content"],
            use_fallback=True
        )

        return {
            "extracted_data": result,
            "line_items": result.get("line_items", []),
            "extraction_confidence": float(result.get("confidence", 0)),
            "used_fallback": True,
        }

    except:
        return {
            "extracted_data": {},
            "line_items": [],
            "extraction_confidence": 0.0,
            "used_fallback": True,
        }