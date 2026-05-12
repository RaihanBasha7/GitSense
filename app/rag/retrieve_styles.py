from chroma_setup import collection

# Query from code review
query = "API call without error handling"

# Retrieve relevant style rules
results = collection.query(
    query_texts=[query],
    n_results=3
)

# Print results
print("\n🔍 Retrieved Style Rules:\n")

for i, doc in enumerate(results["documents"][0], start=1):
    print(f"{i}. {doc}")