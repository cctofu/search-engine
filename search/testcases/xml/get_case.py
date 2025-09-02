import json

# Load the JSON file
with open('filtered_claims.json', 'r') as file:
    data = json.load(file)

dump_data = {}

for app in data:
    claim = data[app]["claim"]
    if isinstance(claim, list):
        calaims = []

        for cla in claim:
            text = cla['#text']
            if 'canceled' in text:
                continue
            calaims.append(text)
            
        dump_data[app] = {
            'claims': calaims
        }
    else:
        print(type(claim))
    
with open('results.json', 'w') as f:
    json.dump(dump_data, f, indent=2)
