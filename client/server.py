from aiohttp import web
import jinja2
import aiohttp_jinja2
import aiohttp
from wikipedia import get_description
from wiki_entry import get_wiki_entries, save_wiki_entry, delete_wiki_entry


@aiohttp_jinja2.template('wiki.html')
async def main(request):
    message = "Welcome!"
    entries = await get_wiki_entries()
    return {'message': message, "current_entries": entries, "len": len(entries)}


async def get_wikipedia_entry(request):
    term = request.match_info.get('term', None)
    if term:
        entry_title = term
        entry_body = await get_description(term)
        content = {"title": entry_title, "body": entry_body}
    else:
        content = {"error": "invalid term"}
    return web.json_response(content)


async def save_entry_to_store(request):
    title = request.match_info.get('term', None)
    body = await get_description(title)
    result = await save_wiki_entry(title, body)
    return web.json_response(result)


async def delete_entry_from_store(request):
    uuid = request.match_info.get('uuid', None)
    result = await delete_wiki_entry(uuid)
    return web.json_response(result)


app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app.add_routes([web.get('/', main),
                web.get('/get_wikipedia_entry/{term}', get_wikipedia_entry),
                web.post('/save_entry_to_store/{term}', save_entry_to_store),
                web.post('/delete_entry_from_store/{uuid}', delete_entry_from_store),
                web.static('/static', "static")])

web.run_app(app, port=8090)