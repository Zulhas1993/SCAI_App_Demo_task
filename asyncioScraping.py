import aiohttp
import asyncio
import re
import csv
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

async def fetch_links(url="https://books.toscrape.com/", links=None):
    if links is None:
        links = []

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(resp.url, flush=True)
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")

            for link in soup.select("h3 a"):
                links.append(urljoin(url, link.get("href")))

            next_page = soup.select_one("li.next a")

            if next_page:
                await fetch_links(urljoin(url, next_page.get("href")), links)
            else:
                return links

async def refresh_links():
    links = await fetch_links()

    with open('links.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows([[link] for link in links])

async def get_links():
    links = []

    with open("links.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            links.append(row[0])

    return links

async def get_response(session, url):
    try:
        async with session.get(url) as resp:
            resp.raise_for_status()  # Check for HTTP errors
            text = await resp.text()
            exp = r'(<title>).*(<\/title>)'
            return re.search(exp, text, flags=re.DOTALL).group(0)
    except aiohttp.ClientError as e:
        print(f"Error fetching {url}: {e}")
        return f"Error fetching {url}"

async def main():
    start_time = time.time()
    

    await refresh_links()

    async with aiohttp.ClientSession() as session:
        tasks = [get_response(session, url) for url in await get_links()]
        results = await asyncio.gather(*tasks)

        for result in results:
            print(result)

    print(f"{time.time() - start_time:.2f} seconds")

def run_main():
    asyncio.run(main())

if __name__ == '__main__':
    run_main()


# async def main():
# 	start_time = time.time()

# 	async with aiohttp.ClientSession() as session:
# 		tasks = []
# 		for url in get_links():
# 			tasks.append(asyncio.create_task(get_response(session, url)))
# 		results = await asyncio.gather(*tasks)
# 		for result in results:
# 			print(result)
# 	print(f"{(time.time() - start_time):.2f} seconds")