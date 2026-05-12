from chroma_setup import collection

# Team coding style rules
style_rules = [
    {
        "id": "rule_1",
        "text": "Use snake_case for function names",
        "category": "naming"
    },
    {
        "id": "rule_2",
        "text": "Avoid hardcoded secrets in code",
        "category": "security"
    },
    {
        "id": "rule_3",
        "text": "Use try-except blocks for API calls",
        "category": "error_handling"
    },
    {
        "id": "rule_4",
        "text": "Add docstrings for public functions",
        "category": "documentation"
    },
    {
        "id": "rule_5",
        "text": "Keep functions small and modular",
        "category": "clean_code"
    }
]

# Store rules in ChromaDB
for rule in style_rules:
    collection.add(
        documents=[rule["text"]],
        metadatas=[{"category": rule["category"]}],
        ids=[rule["id"]]
    )

print("✅ Style rules stored successfully!")