import uuid

def extract_risks_from_text(text: str):
    # Replace with real LLM-based extraction
    if "supplier" in text.lower():
        return {
            "third_parties": [{
                "id": f"tp_{uuid.uuid4().hex[:6]}",
                "name": "Example Supplier",
                "role": "supplier"
            }],
            "risks": [{
                "id": f"r_{uuid.uuid4().hex[:6]}",
                "label": "Supplier concentration",
                "category": "SupplyChain"
            }],
            "relations": []
        }
    return {"third_parties": [], "risks": [], "relations": []}
