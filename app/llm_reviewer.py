from groq import Groq
import os
import json
import logging

# Import ChromaDB collection
from app.rag.chroma_setup import collection

logger = logging.getLogger(__name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# -----------------------------
# Retrieve relevant style rules
# -----------------------------
def retrieve_relevant_styles(diff: str):

    results = collection.query(
        query_texts=[diff],
        n_results=3
    )

    return results["documents"][0]


# -----------------------------
# Build AI Prompt
# -----------------------------
def build_prompt(diff: str, styles):

    style_context = "\n".join(
        [f"- {style}" for style in styles]
    )

    prompt = f"""
You are a senior software engineer reviewing a pull request.

Review the code according to these TEAM CODING STANDARDS:

{style_context}

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

    return prompt


# -----------------------------
# Main Review Function
# -----------------------------
def review_code(diff: str):

    try:

        # Step 1: Retrieve relevant styles
        styles = retrieve_relevant_styles(diff)

        logger.info(f"✅ Retrieved styles: {styles}")

        # Step 2: Build RAG-enhanced prompt
        prompt = build_prompt(diff, styles)

        logger.info("✅ Prompt built successfully")

        # Step 3: Send to Groq LLM
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        text = response.choices[0].message.content.strip()

        logger.info("✅ LLM response received")

        # -----------------------------
        # Clean JSON Response
        # -----------------------------
        if "```" in text:
            text = text.replace("```json", "").replace("```", "").strip()

        start = text.find("[")
        end = text.rfind("]") + 1
        clean_json = text[start:end]

        parsed_response = json.loads(clean_json)

        logger.info("✅ JSON parsed successfully")

        return parsed_response

    except Exception as e:
        logger.error(f"❌ Groq error: {e}")
        return {"error": str(e)}