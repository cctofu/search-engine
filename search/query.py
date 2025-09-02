import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import time

patent_claims = {}
with open('./data/g_claims_text_2023.json', 'r') as f:
    patent_claims = json.load(f)

with open('./data/pg_claims_text_2023.json', 'r') as f:
    patent_claims.update(json.load(f))

patent_embeddings = {}
with open('./data/g_claims_embedding_2023.json', 'r') as f:
    patent_embeddings = json.load(f)

with open('./data/pg_claims_embedding_2023.json', 'r') as f:
    patent_embeddings.update(json.load(f))

patent_ids = list(patent_embeddings.keys())
embeddings = np.array([patent_embeddings[pid] for pid in patent_ids]).astype('float32')

d = embeddings.shape[1]
cpu_index = faiss.IndexFlatL2(d)
cpu_index.add(embeddings)

res = faiss.StandardGpuResources()
gpu_index = faiss.index_cpu_to_gpu(res, 0, cpu_index) 

model = SentenceTransformer('./local_model')

def query_patent(query, k=1):
    query_embedding = model.encode(query).astype('float32').reshape(1, -1)
    start_time = time.time()
    D, I = gpu_index.search(query_embedding, k)
    print(f"distance {D[0]}")
    print(time.time() - start_time)

    closest_patent_ids = [patent_ids[i] for i in I[0]]
    
    return [patent_claims[pid] for pid in closest_patent_ids]

query = "A new method for data processing"
result = query_patent(query, k=5)

for i, claim_text in enumerate(result):
    print(f"Result {i+1}: {claim_text}")
