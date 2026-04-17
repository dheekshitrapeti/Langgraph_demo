# test_classification.py

from src.graphs.classification_graph import classification_graph
import base64


# -------------------------------
# Helper: load PDF → base64
# -------------------------------
def load_pdf(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# -------------------------------
# Input Simulation (IMPORTANT)
# -------------------------------
pdf_path = "/home/aasritha/Langgraph_approach/Langgraph_demo/Invoice_16198_from_Homeport_Stays_LLC.pdf"   

test_input = {
    "email": {
        "msg_id": "test-1",
        "conversation_id": "conv-1",
        "from_email": "sender@example.com",
        "to_email": "receiver@example.com",
        "subject": "Hotel Invoice for Temporary Stay",
        "body": "Please find attached invoice for your stay.",
        "attachments": [
            {
                "contentType": "application/pdf",
                "contentBytes": load_pdf(pdf_path)
            }
        ],
        "status": "fetched"
    }
}


# -------------------------------
# Run Graph
# -------------------------------
result = classification_graph.invoke(test_input)


# -------------------------------
# Output
# -------------------------------
print("\n===== CLASSIFICATION RESULT =====")
print(result)