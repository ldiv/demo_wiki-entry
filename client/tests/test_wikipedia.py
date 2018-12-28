from .. import wikipedia
import pytest
import asyncio


test_titles = [
    'Dickens',
    'Andromeda Galaxy',
    'Platinum',
    'Australia',
    'nonsense',
    'm31',
    'hole in one',
    'magic square',
    'Bad Title'
]


@pytest.mark.parametrize("entry_title", test_titles)
def test_entry_exceeds_max_length(entry_title):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(wikipedia.get_description(entry_title))
    assert len(result) <= 2048


@pytest.mark.parametrize("entry_title", test_titles)
def test_body_is_valid(entry_title):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(wikipedia.get_description(entry_title))
    assert result != "Content not found"
