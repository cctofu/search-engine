import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import time
import pickle

start_time = time.time()
cpu_index = faiss.read_index('index.faiss')
res = faiss.StandardGpuResources()
gpu_index = faiss.index_cpu_to_gpu(res, 0, cpu_index) 
with open('patent_ids.pkl', 'rb') as f:
    patent_ids = pickle.load(f)
end_time = time.time()
print(end_time - start_time)

start_time = time.time()
local_model_path = './local_model'
model = SentenceTransformer(local_model_path)
end_time = time.time()
print(end_time - start_time)

def query_patent(query, k=1):
    query_embedding = model.encode(query).astype('float32').reshape(1, -1)

    start_time = time.time()
    
    D, I = gpu_index.search(query_embedding, k)

    end_time = time.time()

    print(f"distance {D[0]}")
    print(f"Index {I[0]}")
    print(end_time - start_time)
    
    closest_patent_ids = [patent_ids[i] for i in I[0]]
    
    for i, pid in enumerate(closest_patent_ids):
        print(f"rank {i+1}: {pid}")
        
    return closest_patent_ids

query = "A new method for data processing"
result = query_patent(query, k=5)

start_time = time.time()
with open('./data/g_claims_text_2023.json', 'r') as f:
    patent_claims = json.load(f)

for pid in result:
    print(patent_claims[pid])
print(time.time() - start_time)