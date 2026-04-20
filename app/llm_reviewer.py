import google.generativeai as genai
import os
import json
import logging

logger = logging.getLogger(__name__)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-pro")


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
        response = model.generate_content(prompt)
        text = response.text.strip()

        # 🧹 Clean unwanted prefixes (Gemini sometimes adds text)
        if text.startswith("```"):
            text = text.strip("```").strip()

        if text.lower().startswith("json"):
            text = text[4:].strip()

        # ✅ Parse JSON
        return json.loads(text)

    except json.JSONDecodeError:
        logger.error("❌ Failed to parse JSON from Gemini")
        return {
            "error": "Invalid JSON from model",
            "raw": text
        }

    except Exception as e:
        logger.error(f"❌ Gemini error: {e}")
        return {
            "error": str(e)
        }