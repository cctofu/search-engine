import json

# Function to print the contents of specified keys to an output file
def print_keys_to_file(json_file, keys, output_file):
    # Load the JSON file
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    # Open the output file
    with open(output_file, 'w') as f:
        # Iterate over the specified keys
        for key in keys:
            # Check if the key exists in the JSON data
            if key in data:
                # Write the key and its value to the output file
                f.write(f"{key}: {data[key]}\n")
            else:
                # Handle the case where the key does not exist
                f.write(f"{key}: Key not found\n")

# Define the JSON file and the keys to print
json_file = 'g_claims_2023.json'  # Replace with your JSON file name
keys = ['11813286', '11847345', '11701383']  # Replace with your desired keys
output_file = 'output.txt'

# Call the function
print_keys_to_file(json_file, keys, output_file)
