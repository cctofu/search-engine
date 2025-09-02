# import json
# import numpy as np
# from sentence_transformers import SentenceTransformer
# import pandas as pd
# model = SentenceTransformer('./local_model')

# for year in range(2016,2023):
#     for g in ["g","pg"]:
#         file_path = f'data/{g}_claims_{year}.tsv'
#         if g == "g":
#             data = pd.read_csv(file_path, sep='\t', dtype={'patent_id': str})
#             data = data.sort_values(by=['patent_id', 'claim_sequence'])
#             data = data[~data['claim_text'].str.contains(r'\(canceled\)', case=False)]
#             patent_to_claims = data.groupby('patent_id')['claim_text'].apply(list).to_dict()
#         else:
#             data = pd.read_csv(file_path, sep='\t', dtype={'patent_id': str})
#             data = data.sort_values(by=['pgpub_id', 'claim_sequence'])
#             data = data[~data['claim_text'].str.contains(r'\(canceled\)', case=False)]
#             patent_to_claims = data.groupby('pgpub_id')['claim_text'].apply(list).to_dict()
#         patent_to_embedding = {}
#         for patent_id, claims in patent_to_claims.items():
#             embeddings = model.encode(claims)
#             final_embedding = np.mean(embeddings, axis=0)
#             patent_to_embedding[patent_id] = final_embedding.tolist()
#         with open(f'data/{g}_claims_embedding_{year}.json', 'w') as f:
#             json.dump(patent_to_embedding, f)
#         with open(f"data/{g}_claims_text_{year}.json","w") as f:
#             json.dump(patent_to_claims,f)


import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
from transformers import BartTokenizer, BartForConditionalGeneration

model_name = "facebook/bart-large-cnn"
save_directory = "data/bart-large-cnn"

tokenizer = BartTokenizer.from_pretrained(model_name)
tokenizer.save_pretrained(save_directory)

model = BartForConditionalGeneration.from_pretrained(model_name)
model.save_pretrained(save_directory)
