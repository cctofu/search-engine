import json
import numpy as np
import faiss
import pickle

# Load the JSON file
with open('./data/g_claims_embedding_2023.json', 'r') as f:
    g_patent_embeddings = json.load(f)

with open('./data/g_claims_text_2023.json', 'r') as f:
    g_patent_text = json.load(f)

print("The data has been prepared")

g_patent_ids = list(g_patent_embeddings.keys())
g_patent_texts = list(g_patent_text.values())
g_embeddings = np.array([g_patent_embeddings[pid] for pid in g_patent_ids]).astype('float32')

d = g_embeddings.shape[1]
cpu_index = faiss.IndexFlatL2(d)
cpu_index.add(g_embeddings)

# Save the FAISS index to a file
faiss.write_index(cpu_index, 'index.faiss')
print("The FAISS index has been saved to index.faiss")

# Save the patent IDs to a file
with open('patent_ids.pkl', 'wb') as f:
    pickle.dump(g_patent_ids, f)
print("The patent IDs have been saved to patent_ids.pkl")

with open('patent_texts.pkl', 'wb') as f:
    pickle.dump(g_patent_texts, f)
print("The patent IDs have been saved to patent_texts.pkl")
