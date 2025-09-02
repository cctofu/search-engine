import json
import re

# Function to cleanse the citation values
def cleanse_citations(data):
    for key, value in data.items():
        for citation_entry in value:
            if 'citation' in citation_entry:
                # Remove non-numeric characters from the citation
                citation_entry['citation'] = re.sub(r'\D', '', citation_entry['citation'])
    return data

# Function to remove duplicate citation values under the same key
def remove_duplicates(data):
    for key, value in data.items():
        # Use a set to track unique citations and a list to store the cleaned entries
        seen = set()
        unique_entries = []
        for citation_entry in value:
            if 'citation' in citation_entry:
                citation = citation_entry['citation']
                if citation not in seen:
                    seen.add(citation)
                    unique_entries.append(citation_entry)
        data[key] = unique_entries
    return data

# Load the JSON file
with open('output.json', 'r') as f:
    data = json.load(f)

# Ensure the data is a dictionary
if isinstance(data, dict):
    # Cleanse the citations
    cleansed_data = cleanse_citations(data)

    # Remove duplicate citations
    cleaned_data = remove_duplicates(cleansed_data)

    # Save the cleaned data back to a file
    with open('citations_final.json', 'w') as f:
        json.dump(cleaned_data, f, indent=2)

    print("Cleansed and deduplicated data has been saved to 'citations_final.json'.")
else:
    print("The JSON file does not contain a dictionary at the top level.")
