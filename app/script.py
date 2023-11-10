import csv
import os
import requests
from concurrent.futures import ThreadPoolExecutor
from web_page_classifier import WebPageClassifier  # Import the WebPageClassifier class

# Define the TOR proxy
PROXY = 'socks5h://localhost:9050'

# Define the path of the CSV file with onion links
CSV_PATH = '/tmp/merged_onion_links.csv'

# CSV output file for classification results
CLASSIFICATION_CSV = '/tmp/classification_results.csv'

def fetch_onion_site(url):
    try:
        print(f"Starting to scrape {url}")

        # Configure requests to use the TOR proxy
        session = requests.session()
        session.proxies = {'http': PROXY, 'https': PROXY}

        # Send request to the onion URL
        response = session.get(url, timeout=180)  # Adding a timeout for the request
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code

        return response.text

    except requests.exceptions.RequestException as e:
        print(f'An error occurred while fetching the onion site: {e}')
        return None

def classify_and_save(link, classifier, writer):
    html_content = fetch_onion_site('http://' + link)
    if html_content:
        classification = classifier.classify_page(html_content)
        classification['url'] = link
        writer.writerow(classification)

def main(csv_path, classification_csv):
    classifier = WebPageClassifier()

    with open(classification_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['url', 'name', 'category', 'language', 'has_auth_form', 'asks_for_javascript', 'asks_for_cookies', 'has_captcha']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        with open(csv_path, newline='') as links_file:
            reader = csv.reader(links_file)
            links = [row[0] for row in reader if row]  # Collect all links assuming they are in the first column

        # Use ThreadPoolExecutor to create a pool of threads and execute tasks concurrently
        with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust the number of workers as needed
            for link in links:
                executor.submit(classify_and_save, link, classifier, writer)

if __name__ == '__main__':
    main(CSV_PATH, CLASSIFICATION_CSV)
