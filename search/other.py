# import os
# import time
# os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
# from transformers import AutoTokenizer, AutoModel
# start_time = time.time()
# tokenizer = AutoTokenizer.from_pretrained("data/chatglm3-6b", trust_remote_code=True)
# model = AutoModel.from_pretrained("data/chatglm3-6b", trust_remote_code=True).half().cuda()
# model.config.eos_token_id = tokenizer.eos_token_id
# model.config.pad_token_id = tokenizer.pad_token_id
# model.config.unk_token_id = tokenizer.unk_token_id
# model = model.eval()
# response, history = model.chat(tokenizer, f"Write five complete and grammatically correct continuation phrases for me for 'A new method for' to complete the phrase. Each phrase should start with a number followed by a dot and a space . Ensure that each phrase is complete and does not end abruptly.", history=[])
# print(time.time() - start_time)
# print(type(response))
# print(response)
# lines = response.splitlines()
# phrases = [line.split('. ', 1)[1] for line in lines if line[0].isdigit() and line[1] == '.']
# print(phrases)

from sentence_transformers import SentenceTransformer
from transformers import BartTokenizer, BartForConditionalGeneration, pipeline
from keybert import KeyBERT
import json
local_model_path = "../search_engine/search/local_model"
local_bart_path = "data/bart-large-cnn"
sentence_model = SentenceTransformer(local_model_path,device="cuda")
kw_model = KeyBERT(model=sentence_model)
bart_tokenizer = BartTokenizer.from_pretrained(local_bart_path)
bart_model = BartForConditionalGeneration.from_pretrained(local_bart_path)
summarizer = pipeline("summarization", model=bart_model, tokenizer=bart_tokenizer,device="cuda")
print("Load model")
patent_claims = {}
patent_details = {}
def generate_keywords(text):
    keywords = kw_model.extract_keywords(
            text,
            keyphrase_ngram_range=(2, 5),
            stop_words='english',
            use_maxsum=True,
            nr_candidates=20,
            top_n=5
        )
    return list(dict(keywords).keys())

def generate_summary(text):
    all_text = " ".join(text)
    summary = summarizer(all_text, max_length=100, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    return summary[0]["summary_text"]

for g in ["g","pg"]:
        with open(f'data/{g}_claims_text_2023.json', 'r') as f:
            patent_claims.update(json.load(f))

print("Load")

cnt = 0
for patent_id, claim_texts in patent_claims.items():
    keywords = generate_keywords(claim_texts[0])
    summary = generate_summary(claim_texts[:5])
    patent_details[patent_id] = {
        "keywords": keywords,
        "summary": summary
    }
    cnt += 1
    print(cnt)

with open('data/patent_details_2023.json', 'w') as file:
    json.dump(patent_details, file, ensure_ascii=False, indent=4)
