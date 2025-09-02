import re

def clean_xml(xml_file):
    # Read the XML file
    with open(xml_file, 'r', encoding='utf-8') as file:
        xml_content = file.read()
    
    # Remove lines starting with <?xml or <!DOCTYPE
    xml_content = re.sub(r'<\?xml.*?\?>', '', xml_content, flags=re.DOTALL)
    xml_content = re.sub(r'<!DOCTYPE.*?>', '', xml_content, flags=re.DOTALL)
    # Remove <b> and </b> tags within the lines
    xml_content = re.sub(r'<b>', '', xml_content)
    xml_content = re.sub(r'</b>', '', xml_content)

    xml_content = re.sub(r'<claim-text>', '', xml_content)
    xml_content = re.sub(r'</claim-text>', '', xml_content)
    
    return xml_content

def remove_empty_lines(content):
    # Split the content into lines and filter out empty lines
    lines = content.split('\n')
    non_empty_lines = [line for line in lines if line.strip() != '']
    return '\n'.join(non_empty_lines)

def save_cleaned_xml(original_file, new_file):
    # Clean the XML file
    cleaned_content = clean_xml(original_file)
    
    # Remove any empty lines
    cleaned_content_no_empty_lines = remove_empty_lines(cleaned_content)
    
    # Wrap the cleaned content with <patent-applications> tags
    final_text = f"<patent-applications>\n{cleaned_content_no_empty_lines}\n</patent-applications>"
    
    # Write the final text back to a new file
    with open(new_file, 'w', encoding='utf-8') as file:
        file.write(final_text)
    
    print(f"Successfully cleaned {original_file} and saved to {new_file}")

# File paths
xml_file_path = 'ipa150108.xml'
new_file_path = 'clean.xml'

# Clean the XML file and save to a new file
save_cleaned_xml(xml_file_path, new_file_path)
