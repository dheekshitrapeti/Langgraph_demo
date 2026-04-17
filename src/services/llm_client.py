# src/services/llm_client.py

import json
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from src.config import settings


class LLMClient:
    def __init__(self):
        self.primary = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.1,
        )

        self.fallback = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.1,
        )

    # ---------------------------
    # Robust JSON extractor
    # ---------------------------
    def _safe_json(self, text: str) -> dict:
        try:
            # Extract JSON block even if extra text exists
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                return json.loads(match.group())
        except Exception:
            pass
        return {}

    # ---------------------------
    # Identify invoice page
    # ---------------------------
    def identify_invoice_page(self, pages):
        prompt = f"""
You are an invoice detection system.

Find which page contains the invoice.

Look for:
- invoice number
- total amount
- billing details
- vendor name

Return ONLY valid JSON:
{{"page_index": int, "confidence": float}}

Pages:
{pages[:3]}
"""

        resp = self.primary.invoke(prompt)
        return self._safe_json(resp.content)

    # ---------------------------
    # Extract invoice data
    # ---------------------------
    def extract_invoice(self, text: str, use_fallback: bool = False):
        model = self.fallback if use_fallback else self.primary

        prompt = f"""
You are an advanced invoice data extraction system.

Your task is to extract structured information from the given invoice text.

Return ONLY valid JSON. Do NOT include any explanation or extra text.

---------------------
OUTPUT FORMAT (STRICT)
---------------------

{{
"invoice_id": string or null,
"invoice_date": string or null,
"transferee_name": string or null,
"po_number": string or null,
"bill_to": string or null,
"partner_name": string or null,
"partner_bank_details": string or null,
"reference_number": string or null,
"due_date": string or null,
"total_amount": number or null,
"service_date": string or null,
"registration_number": string or null,
"customer_name": string or null,
"customer_number": string or null,
"currency_type": string or null,
"amount_due": number or null,
"discount_percentage": number or null,
"discount_amount": number or null,
"pricing_notes": string or null,
"billing_address": string or null,
"vendor_address": string or null,
"client_id": string or null,
"property_name": string or null,
"checkin_date": string or null,
"checkout_date": string or null,
"occupants": number or null,
"property_address": string or null,
"line_items": [
    {{
        "description": string,
        "quantity": number,
        "unit_price": number,
        "amount": number
    }}
],
"confidence": number (0-100)
}}

---------------------
EXTRACTION RULES
---------------------

1. If a field is not present, return null.
2. Do NOT guess missing values.
3. Extract exact values from the text.
4. Dates → ISO format (YYYY-MM-DD) if possible.
5. Numbers → numeric only (no symbols).
6. currency_type → USD, INR, EUR, etc.
7. "bill_to" → billing party.
8. "partner_name" → vendor/service provider.
9. "transferee_name" → relocated person (if present).
10. "property_*" → housing-related info.
11. "occupants" → number only.
12. Ensure JSON is valid.

---------------------
INVOICE TEXT
---------------------

{text}
"""

        resp = model.invoke(prompt)
        return self._safe_json(resp.content)


# Singleton instance
llm_client = LLMClient()