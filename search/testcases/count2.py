import json

# Load the JSON file
with open('cite.json', 'r') as file:
    data = json.load(file)

print(len(data))