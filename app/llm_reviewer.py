import requests
import os
import json
import logging
import time

logger = logging.getLogger(__name__)

HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('HF_API_KEY')}"
}


def call_hf_api(prompt):
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 500,
            "temperature": 0.2
        }
    }
    
    response = requests.post(
    HF_API_URL,
    headers=HEADERS,
    json=payload
)

    # 🔁 Retry logic (VERY IMPORTANT)
    for attempt in range(3):
        response = requests.post(HF_API_URL, headers=HEADERS, json=payload)

        if response.status_code == 200:
            return response.json()

        elif response.status_code == 503:
            logger.warning("⏳ Model loading... retrying")
            time.sleep(3)

        else:
            logger.error(f"❌ HF Error: {response.text}")
            break

    return {"error": "HF API failed"}


def review_code(diff: str):
    prompt = f"""
You are a senior software engineer reviewing a pull request.

Analyze the following git diff and provide:

- Code issues
- Security risks
- Style improvements
- Suggestions

Return ONLY valid JSON.
No explanation. No markdown. No extra text.

Format:
[
  {{
    "severity": "critical | warning | suggestion",
    "comment": "...",
    "line": "optional"
  }}
]

Diff:
{diff}
"""

    try:
        result = call_hf_api(prompt)

        if "error" in result:
            return result

        # HF usually returns list
        text = result[0]["generated_text"].strip()

        # 🧹 Clean output
        if "```" in text:
            text = text.replace("```json", "").replace("```", "").strip()

        # Extract JSON safely
        start = text.find("[")
        end = text.rfind("]") + 1
        clean_json = text[start:end]

        return json.loads(clean_json)

    except Exception as e:
        logger.error(f"❌ HF Parsing Error: {e}")
        return {
            "error": str(e),
            "raw": result if 'result' in locals() else None
        }