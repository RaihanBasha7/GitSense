import chromadb

# Create persistent database
client = chromadb.PersistentClient(path="./chroma_db")

# Create or get collection
collection = client.get_or_create_collection(
    name="code_styles"
)

print("✅ ChromaDB connected successfully!")