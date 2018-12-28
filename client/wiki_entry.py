import json
import aiohttp
import asyncio
from logger import wiki_logger, log_crud


SERVER = "localhost"
URL = "http://{}:8080/db/wikientry".format(SERVER)


async def fetch(session, url):
    async with session.get(url,
                           headers={'Accept': 'application/json', },
                           auth=aiohttp.BasicAuth('root', 'root')
                           ) as response:
        return await response.text()


async def post(session, url, data):
    async with session.post(url, json=data,
                            headers={'Accept': 'application/json', },
                            auth=aiohttp.BasicAuth('root', 'root')
                            ) as response:
        return await response.text()


async def delete(session, url):
    async with session.delete(url,
                            headers={'Accept': 'application/json', },
                            auth=aiohttp.BasicAuth('root', 'root')
                            ) as response:
        return await response.text()


async def get_wiki_entry(url):
    tasks = []
    async with aiohttp.ClientSession() as session:
        tasks.append(fetch(session, url))
        results = await asyncio.gather(*tasks)
        entry = json.loads(results[0])
        return {
            "Title": entry["Title"],
            "Body": entry["Body"],
            "uuid": entry["@name"]
        }


async def get_wiki_entries():
    tasks = []
    async with aiohttp.ClientSession() as session:
        tasks.append(fetch(session, URL))
        results = await asyncio.gather(*tasks)
        if results[0] == '{}':
            return []
        all_entries = json.loads(results[0])["items"]
        wiki_entries = []
        for entry in all_entries:
            entry_url = entry["@id"]
            wiki_entries.append(await get_wiki_entry(entry_url))
        return wiki_entries


async def save_wiki_entry(title, body):
    data = {'@type': 'WikiEntry', 'Title': title, 'Body': body}
    async with aiohttp.ClientSession() as session:
        task = post(session, URL, data)
        results = await asyncio.gather(task)
        log_crud("CREATE", {"status": "success"}, title)
        return json.loads(results[0])


async def delete_wiki_entry(uuid):
    url = URL + '/' + uuid
    async with aiohttp.ClientSession() as session:
        task = delete(session, url)
        results = await asyncio.gather(task)
        results = {"status": "success"} if results[0] == '' else {"status": "error"}
        log_crud("DELETE", results, uuid)
        return results


