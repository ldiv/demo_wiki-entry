from .. import wiki_entry
import pytest
import requests


# blocking not a concern in this testing instance so using requests
test_session = requests.Session()
test_session.auth = ('root', 'root')
test_session.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})


def delete_test_container():
    container_name = "test"
    url = "http://{}:8080/db/{}".format(wiki_entry.SERVER, container_name)
    test_session.delete(url)


@pytest.fixture()
def test_container():
    delete_test_container()
    container_name = "test"
    data = {"@type": "Container",
            "description": "Test",
            "id": container_name}
    url = "http://{}:8080/db/".format(wiki_entry.SERVER)
    res = test_session.post(url, json=data)
    if res.status_code == 200:
        return container_name
    return res


def test_instance_available():
    url = "http://{}:8080/db/".format(wiki_entry.SERVER)
    res = test_session.get(url)
    assert res.status_code == 200


def test_container_exists():
    url = wiki_entry.URL
    res = test_session.get(url)
    assert res.status_code == 200


def test_insert_duplicate(test_container):
    container_name = test_container
    url = "http://{}:8080/db/{}".format(wiki_entry.SERVER, container_name)
    entry1 = {"@type": "WikiEntry", "Title": "test title", "Body": "test body"}
    entry2 = {"@type": "WikiEntry", "Title": "test title", "Body": "test body"}
    test_session.post(url, json=entry1)
    try:
        test_session.post(url, json=entry2)
        # If second create succeeds test fails
        assert False
    except:
        assert True
    finally:
        delete_test_container()



