from openai import OpenAI
import os
import json
import logging

logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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
        response = client.chat.completions.create(
            model="gpt-4o-mini",   # fast + cheap + reliable
            messages=[
                {"role": "system", "content": "You are a strict code reviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        text = response.choices[0].message.content.strip()

        # 🧹 Clean JSON if needed
        if "```" in text:
            text = text.replace("```json", "").replace("```", "").strip()

        start = text.find("[")
        end = text.rfind("]") + 1
        clean_json = text[start:end]

        return json.loads(clean_json)

    except json.JSONDecodeError:
        logger.error("❌ JSON parse failed")
        return {
            "error": "Invalid JSON",
            "raw": text
        }

    except Exception as e:
        logger.error(f"❌ OpenAI error: {e}")
        return {
            "error": str(e)
        }