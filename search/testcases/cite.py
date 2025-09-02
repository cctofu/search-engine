import csv
import json
from tqdm import tqdm

def csv_to_json(csv_file_path, json_file_path):
    data = {}
    
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in tqdm(csv_reader):
            app_id = row['app_id']
            entry = {
                'citation': row['citation_pat_pgpub_id'],
            }
            if app_id not in data:
                data[app_id] = []
            data[app_id].append(entry)
    
    with open(json_file_path, mode='w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)

csv_file_path = 'citations.csv'
json_file_path = 'citations_original.json'
csv_to_json(csv_file_path, json_file_path)
