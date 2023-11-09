import csv
import os
import requests
from concurrent.futures import ThreadPoolExecutor

# Define the TOR proxy
PROXY = 'socks5h://localhost:9050'

# Define the path of the CSV file with onion links
CSV_PATH = '/tmp/merged_onion_links.csv'

# Define the directory to save the content
SAVE_DIR = '/tmp/tor_pages'

# Ensure the SAVE_DIR exists
os.makedirs(SAVE_DIR, exist_ok=True)

def fetch_onion_site(url, save_path):
    try:
        print(f"Starting to scrape {url}")

        # Configure requests to use the TOR proxy
        session = requests.session()
        session.proxies = {'http': PROXY, 'https': PROXY}

        # Send request to the onion URL
        response = session.get(url, timeout=180)  # Adding a timeout for the request
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code

        # Save the response content to a file
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f'Content saved to {save_path}')

    except requests.exceptions.RequestException as e:
        print(f'An error occurred while fetching the onion site: {e}')

def scrape_link(link):
    if link:
        # Sanitize the file name from the onion link
        filename = link.replace('.onion', '') + '.html'
        save_path = os.path.join(SAVE_DIR, filename)
        fetch_onion_site('http://' + link, save_path)

def main(csv_path, save_dir):
    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        links = [row[0] for row in reader if row]  # Collect all links assuming they are in the first column

    # Use ThreadPoolExecutor to create a pool of threads and execute tasks concurrently
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust the number of workers as needed
        executor.map(scrape_link, links)

if __name__ == '__main__':
    main(CSV_PATH, SAVE_DIR)
