import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_risks_from_text(text: str):
    """
    Use an LLM to extract risks and related entities from 10-K text chunks.
    Returns a list of dicts: [{"risk": "...", "parties": ["..."]}, ...]
    """
    if not text.strip():
        return []

    prompt = f"""
You are an expert in financial risk analysis. Extract risk-related statements 
from the following 10-K filing text. For each risk, return a JSON list where 
each item contains:
- "risk": a concise summary of the risk
- "parties": list of company names or entities involved (if any)

Text:
{text[:4000]}  # limit to prevent over-token
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        raw_output = response.choices[0].message.content.strip()

        # Try parsing as JSON
        import json
        risks = json.loads(raw_output)
        if isinstance(risks, list):
            return risks
        else:
            return []
    except Exception as e:
        print("LLM extraction error:", e)
        return []
