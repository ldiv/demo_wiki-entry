from bs4 import BeautifulSoup
import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor


DEFAULT_TERM = "Dickens"
URL = "https://en.wikipedia.org/wiki/{}"


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def get_description(term=DEFAULT_TERM):
    url = URL.format(term)
    async with aiohttp.ClientSession() as session:
        task = fetch(session, url)
        results = await asyncio.gather(task)
        return parse_description(results[0])


def parse_description(response):
    def parse(res):
        content_id = "mw-content-text"
        soup = BeautifulSoup(res)
        all_content = soup.find_all("div", id=content_id)[0]
        try:
            first_p = all_content.find_all("p")[1]
            if first_p.text.strip() == "":
                # The number of leading empty p elements vary
                first_p = all_content.find_all("p")[2]
            res = first_p.text
        except IndexError:
            res = "Content not found"
        return res

    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(parse, response)
        return future.result()

