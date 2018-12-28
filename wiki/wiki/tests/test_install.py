import asyncio


async def test_install(wiki_requester):  # noqa
    async with wiki_requester as requester:
        response, _ = await requester('GET', '/db/guillotina/@addons')
        assert 'wiki' in response['installed']
