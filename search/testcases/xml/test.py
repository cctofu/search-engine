import json

# Load the JSON file
with open('results.json', 'r') as file:
    data = json.load(file)

print(len(data))