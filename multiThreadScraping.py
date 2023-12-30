import requests
import csv
import re
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_links(url="https://books.toscrape.com/", links=[]):
    try:
        r = requests.get(url)
        r.raise_for_status()  # Check for HTTP errors
        print(r.url, flush=True)
        
        soup = BeautifulSoup(r.text, "html.parser")
        for link in soup.select("h3 a"):
            links.append(urljoin(url, link.get("href")))
            
        next_page = soup.select_one("li.next a")
        if next_page:
            return fetch_links(urljoin(url, next_page.get("href")), links)
        else:
            return links
    except Exception as e:
        print(f"Error fetching links from {url}: {e}")
        return links

if __name__ == "__main__":
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=100) as p:
        results = p.map(fetch_links, [f"https://books.toscrape.com/catalogue/page-{page}.html" for page in range(1, 6)])

    # Flatten the list of lists into a single list
    all_links = [link for sublist in results for link in sublist]

    # Print the total number of links and the time taken
    print(f"Total links: {len(all_links)}")
    print(f"Time taken: {time.time() - start_time} seconds")
