import requests
import re
import time
from multiprocessing import Pool, cpu_count
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_links():
    # Provide a list of URLs to scrape
    # Example: replace the following with your list of URLs
    # return ["https://example.com/page1", "https://example.com/page2", "https://example.com/page3"]
    return ["https://books.toscrape.com/"]

def get_response(url):
    try:
        resp = requests.get(url)
        resp.raise_for_status()  # Check for HTTP errors

        print('.', end='', flush=True)

        soup = BeautifulSoup(resp.text, 'html.parser')
        title_tag = soup.find('title')

        if title_tag:
            return title_tag.text.strip()
        else:
            return f"No title found for {url}"

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return f"Error fetching {url}"

def main():
    start_time = time.time()
    links = get_links()

    # Use the number of available CPU cores
    cores_nr = cpu_count()

    with Pool(cores_nr) as p:
        results = p.map(get_response, links)

        for result in results:
            print(result)

    print(f"{time.time() - start_time:.2f} seconds")

if __name__ == '__main__':
    main()
