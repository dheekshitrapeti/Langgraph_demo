from src.graphs.extraction import extraction_graph
from pathlib import Path
import base64

def load_pdf(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

pdf_path = "/home/aasritha/Langgraph_approach/Langgraph_demo/Invoice_16198_from_Homeport_Stays_LLC.pdf"   

test_input = {
    "email": {
        "msg_id": "test-1",
        "attachments": [
            {
                "contentType": "application/pdf",
                "contentBytes": load_pdf(pdf_path)
            }
        ]
    }
}

result = extraction_graph.invoke(test_input)

print("\n===== RESULT =====")
print(result)