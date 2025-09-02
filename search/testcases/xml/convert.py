import xmltodict
import json

# Function to convert XML to JSON
def convert_xml_to_json(xml_file, json_file):
    with open(xml_file, 'r', encoding='utf-8') as file:
        xml_content = file.read()
    
    data_dict = xmltodict.parse(xml_content)
    json_data = json.dumps(data_dict, indent=4)
    
    with open(json_file, 'w', encoding='utf-8') as file:
        file.write(json_data)
    
    print(f"Successfully converted {xml_file} to {json_file}")

# File paths
xml_file_path = 'clean.xml'
json_file_path = 'app.json'

# Convert the XML file to JSON
convert_xml_to_json(xml_file_path, json_file_path)
