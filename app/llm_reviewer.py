from groq import Groq
import os
import json
import logging

logger = logging.getLogger(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def review_code(diff: str):
    prompt = f"""
You are a senior software engineer reviewing a pull request.

Return ONLY valid JSON in this format:
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
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # 🔥 powerful + free
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        text = response.choices[0].message.content.strip()

        # Clean JSON
        if "```" in text:
            text = text.replace("```json", "").replace("```", "").strip()

        start = text.find("[")
        end = text.rfind("]") + 1
        clean_json = text[start:end]

        return json.loads(clean_json)

    except Exception as e:
        logger.error(f"❌ Groq error: {e}")
        return {"error": str(e)}