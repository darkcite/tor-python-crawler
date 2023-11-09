import os
import requests
import time

# Define the TOR proxy
PROXY = 'socks5h://localhost:9050'

# Define the URL of the onion service (replace with the actual URL you want to use)
ONION_URL = 'http://darkfailenbsdla5mal2mxn2uz66od5vtzd5qozslagrfzachha3f3id.onion'

# Define the path to save the content
SAVE_PATH = '/tmp/onion_site_content.html'

def fetch_onion_site(url):
    try:
        print("Starting to scrape")
        
        # Configure requests to use the TOR proxy
        session = requests.session()
        session.proxies = {'http': PROXY, 'https': PROXY}

        # Send request to the onion URL
        response = session.get(url)
        response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code

        # Save the response content to a file
        with open(SAVE_PATH, 'w') as file:
            file.write(response.text)
        print(f'Content saved to {SAVE_PATH}')

    except requests.exceptions.RequestException as e:
        print(f'An error occurred while fetching the onion site: {e}')

if __name__ == '__main__':
    fetch_onion_site(ONION_URL)
