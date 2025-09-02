import json

def remove_claims_with_claim_ref(json_file, output_file):
    # Read the JSON file
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Iterate over each patent application
    for doc_number, application in data.items():
        if 'claim' in application and isinstance(application['claim'], list):
            claims = application['claim']
            # Filter out claims that have 'claim-ref' in 'claim-text' when claim-text is a dictionary
            filtered_claims = []
            for claim in claims:
                if isinstance(claim, dict):
                    if isinstance(claim, dict):
                        if 'claim-ref' not in claim:
                            filtered_claims.append(claim)
                    else:
                        filtered_claims.append(claim)
            # Update the claims
            application['claim'] = filtered_claims
            # Remove the "@id": "claims" key
            if '@id' in application:
                del application['@id']
    
    # Write the updated data to the new JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
    
    print(f"Successfully removed claims with 'claim-ref' and '@id' key and saved to {output_file}")

# File paths
json_file_path = 'extracted_claims.json'
output_file_path = 'filtered_claims.json'

# Remove claims with 'claim-ref' and save to a new file
remove_claims_with_claim_ref(json_file_path, output_file_path)
