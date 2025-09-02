from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.apps import apps

def request_success(data={}):
    return JsonResponse({"code": 0, "info": "Succeed", **data})

import json
import numpy as np
import faiss
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

@csrf_exempt
def search(req: HttpRequest):
    if req.method == "POST":
        model = apps.get_app_config("search").sentence_model
        bucket_index = faiss.read_index('search/2023_test_buckets/bucket_index.faiss')
        body = json.loads(req.body.decode("utf-8"))
        query = body["query"]
        k  = 20
        query_embedding = model.encode(query).astype('float32').reshape(1, -1)
        D, I = bucket_index.search(query_embedding, 1)
        closest_bucket = I[0][0]
        with open(f'search/2023_test_buckets/embeddings_bucket_{closest_bucket}.json', 'r') as f:
            bucket_embeddings = json.load(f)
        
        with open(f'search/2023_test_buckets/claims_bucket_{closest_bucket}.json', 'r') as f:
            bucket_claims = json.load(f)

        bucket_patent_ids = list(bucket_embeddings.keys())
        bucket_embeddings_array = np.array([bucket_embeddings[pid] for pid in bucket_patent_ids]).astype('float32')

        d = bucket_embeddings_array.shape[1]
        bucket_index = faiss.IndexFlatL2(d)
        bucket_index.add(bucket_embeddings_array)
        res = faiss.StandardGpuResources()
        gpu_index = faiss.index_cpu_to_gpu(res, 0, bucket_index) 
        D, I = gpu_index.search(query_embedding, k)

        closest_patent_ids = [bucket_patent_ids[i] for i in I[0]]
        result = {"data": []}
        for pid in closest_patent_ids:
            claims = bucket_claims[pid]
            claim_embeddings = model.encode(claims).astype('float32')
            similarities = [cosine_similarity(query_embedding, ce) for ce in claim_embeddings]
            most_similar_claim_index = int(np.argmax(similarities))
            result["data"].append({
                "patent_id": pid,
                "claims": claims,
                "most_similar_claim_index": most_similar_claim_index,
            })
        return request_success(result)

@csrf_exempt
def autocomplete(req: HttpRequest, short_query: any):
    if req.method == "GET":
        llm_model = apps.get_app_config("search").llm_model
        llm_tokenizer = apps.get_app_config("search").llm_tokenizer
        short_query = str(short_query)
        prompt = f"Write five complete and grammatically correct continuation phrases that start with '{short_query}' to complete the phrase. Each phrase should start with a number followed by a dot and a space, and must begin with the word '{short_query}'. Ensure that each phrase is complete and does not end abruptly."
        # prompt = f"Write five complete and grammatically correct continuation phrases for me for '{short_query}' to complete the phrase. Each phrase should start with a number followed by a dot and a space. Ensure that each phrase is complete and does not end abruptly."
        response, history = llm_model.chat(llm_tokenizer, prompt)
        lines = response.splitlines()
        phrases = [line.split('. ', 1)[1] for line in lines if line[0].isdigit() and line[1] == '.']
        result = {"data": phrases}
        return request_success(result)

@csrf_exempt
def details(req: HttpRequest):
    if req.method == "POST":
        kw_model = apps.get_app_config("search").kw_model
        summarizer = apps.get_app_config("search").summarizer
        body = json.loads(req.body.decode("utf-8"))
        claim_texts = body["claim_texts"]
        result = {"data":[]}
        keywords = kw_model.extract_keywords(
            claim_texts[0],
            keyphrase_ngram_range=(2, 3),
            stop_words='english',
            use_maxsum=True,
            nr_candidates=20,
            top_n=5
        )
        keywords_list = list(dict(keywords).keys())
        all_text = " ".join(claim_texts)
        summary = summarizer(all_text, max_length=100, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
        result["data"] = {"keyword":keywords_list,
                          "abstract":summary[0]["summary_text"]}
        return request_success(result)

# Create your views here.