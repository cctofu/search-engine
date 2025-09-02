import json

# Load the JSON file
with open('final.json', 'r') as f:
    data = json.load(f)

# Ensure the data is a dictionary
if isinstance(data, dict):
    # Get the number of keys
    num_keys = len(data)
    print(f"Number of keys in the JSON file: {num_keys}")
else:
    print("The JSON file does not contain a dictionary at the top level.")
