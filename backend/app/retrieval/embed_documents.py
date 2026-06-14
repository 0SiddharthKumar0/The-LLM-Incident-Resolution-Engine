from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

sample_text = "database timeout in payment api"

embedding = model.encode(sample_text)

print(f"Embedding length: {len(embedding)}")
print(embedding[:10])