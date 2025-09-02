import json
import random

# Load the JSON file
with open('citations2.json', 'r') as f:
    data = json.load(f)

# Ensure the data is a dictionary
if isinstance(data, dict):
    # Get a list of all keys
    keys = list(data.keys())

    # Randomly sample 20 keys
    random_keys = random.sample(keys, min(20, len(keys)))

    # Print the contents of the 20 random keys
    for key in random_keys:
        print(f"Key: {key}")
        print(f"Value: {data[key]}")
        print("-" * 50)
else:
    print("The JSON file does not contain a dictionary at the top level.")
