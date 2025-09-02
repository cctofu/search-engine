import json
from transformers import AutoTokenizer
from nltk.stem import PorterStemmer

def tokenize_and_stem(text, tokenizer, stemmer):
    tokens = tokenizer.tokenize(text)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return stemmed_tokens

def check_lengths(input_file, tokenizer, stemmer):
    with open(input_file, 'r') as file:
        patents = json.load(file)
    
    total_keys = len(patents)
    longer_than_512 = 0
    total_length = 0

    for claim in patents.values():
        stemmed_tokens = tokenize_and_stem(claim, tokenizer, stemmer)
        length = len(stemmed_tokens)
        total_length += length
        if length > 512:
            longer_than_512 += 1
    
    average_length = total_length / total_keys if total_keys > 0 else 0
    
    return total_keys, longer_than_512, average_length

def main(input_file):
    tokenizer = AutoTokenizer.from_pretrained('./all-mpnet-base-v2_tokenizer/')
    stemmer = PorterStemmer()
    
    total_keys, longer_than_512, average_length = check_lengths(input_file, tokenizer, stemmer)
    
    print(f"Total number of keys: {total_keys}")
    print(f"Number of keys with values longer than 512 tokens after stemming: {longer_than_512}")
    print(f"Average length of the values after stemming: {average_length:.2f}")

if __name__ == "__main__":
    input_file = 'g_claims_2023.json'
    main(input_file)
