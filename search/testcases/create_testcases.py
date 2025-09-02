import json

# Load the data JSON file
with open('./xml/results.json', 'r') as f:
    data = json.load(f)
print("loaded patent data")

# Load the testcase JSON file
with open('citations2.json', 'r') as f:
    testcase = json.load(f)
print("loaded citation data")

# Find the common keys
common_keys = set(data.keys()).intersection(testcase.keys())
print(f"Number of common keys: {len(common_keys)}")

del_key = []

for key in data:
    if key not in common_keys:
        del_key.append(key)

for key in del_key:
    del data[key]
    
with open('cite.json', 'w') as f:
    json.dump(data, f, indent=2)