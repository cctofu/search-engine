import json

def extract_claims(json_file, output_file):
    # Read the JSON file
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Initialize the new data structure
    new_data = {}

    # Check if the keys 'patent-applications' and 'us-patent-application' exist
    if 'patent-applications' in data and 'us-patent-application' in data['patent-applications']:
        applications = data['patent-applications']['us-patent-application']
        
        # Iterate over each application
        for application in applications:
            # Extract the doc-number
            try:
                doc_number = application['us-bibliographic-data-application']['application-reference']['document-id']['doc-number']
            except KeyError:
                print("Missing doc-number in one of the applications.")
                continue
            
            # Extract the claims
            claims = application.get('claims', None)
            
            # Add to new data structure
            if claims is not None:
                new_data[doc_number] = claims
            else:
                print(f"No claims found for doc-number: {doc_number}")

    # Write the new data to a JSON file
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(new_data, file, indent=4)
    
    print(f"Successfully created {output_file}")

# File paths
json_file_path = 'app.json'
output_file_path = 'extracted_claims.json'

# Extract claims and create new JSON file
extract_claims(json_file_path, output_file_path)
