import requests
import zipfile
import os

def download_file(url, local_filename):
    # Send a GET request to the URL
    with requests.get(url, stream=True) as r:
        r.raise_for_status()  # Raise an error for bad status
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return local_filename

def unzip_file(zip_filename, extract_to):
    # Extract a ZIP file
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def main():
    base_urls = [
        "https://s3.amazonaws.com/data.patentsview.org/pregrant_publications/pg_claims_{year}.tsv.zip",
        "https://s3.amazonaws.com/data.patentsview.org/claims/g_claims_{year}.tsv.zip"
    ]
    
    years = range(2022, 2024)
    
    for year in years:
        for base_url in base_urls:
            url = base_url.format(year=year)
            local_zip_filename = url.split('/')[-1]
            extract_to = "."

            # Download the file
            print(f"Downloading {url}...")
            download_file(url, local_zip_filename)
            print(f"Downloaded {local_zip_filename}")

            # Unzip the file
            print(f"Unzipping {local_zip_filename}...")
            unzip_file(local_zip_filename, extract_to)
            print(f"Unzipped to {extract_to}")

            # Optionally, delete the zip file after extraction
            os.remove(local_zip_filename)
            print(f"Deleted the zip file {local_zip_filename}")

if __name__ == "__main__":
    main()
