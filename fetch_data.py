import requests
import json
import os
import time


os.makedirs("data/raw", exist_ok=True)
def search_pubmed(query, max_results=10):
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }

    response = requests.get(url,params=params)
    data = response.json()

    ids = data["esearchresult"]["idlist"]
    print(f"Found {len(ids)} articles")
    return ids

def fetch_abstracts(ids):
    
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    
    params = {
        "db": "pubmed",
        "id": ",".join(ids),  # join all IDs into one comma-separated string
        "rettype": "abstract", # we want the abstract specifically
        "retmode": "text"      # give it to us as plain text
    }

    response = requests.get(url, params=params)
    return response.text

if __name__ =="__main__":
    query = "Alzheimer's disease amyloid tau"
    print(f"Searching PubMed for: {query}")

    ids = search_pubmed(query, max_results=10)
    print(f"Article IDs found: {ids}")

    time.sleep(1)

    print("Fetching abstracts..")
    abstracts = fetch_abstracts(ids)

    output_path = "data/raw/abstracts.txt"
    with open(output_path,"w",encoding="utf-8") as f:
        f.write(abstracts)

    print(f"Saved to {output_path}")
    print("\nFirst 500 characters preview:")
    print(abstracts[:500])
