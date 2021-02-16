import os
import sys

import typesense
import unittest
import urllib.request
from typesense.exceptions import ObjectNotFound

curr_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(curr_dir, os.pardir)))


WORDS_FILE_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"


def getSearch(api_key: str, host: str = "127.0.0.1", port: str = "8108", protocol: str = "http",
              timeout: int = 3) -> typesense.Client:
    """
    Gets a Typesense client.

    :param api_key: Typesense api key.
    :param host: Host, default ot localhost.
    :param port: Port, default to 8108.
    :param protocol: Protocol, defaults to http.
    :param timeout: Connection timeout in seconds, defaults to 3.

    :return typesense.Client: Returns a Typesense client.
    """
    return typesense.Client({
        'nodes': [{
            'host': host,
            'port': port,
            'protocol': protocol
        }],
        'api_key': api_key,
        'connection_timeout_seconds': timeout,
    })


def getWordSchema(collection_name: str = "words") -> dict:
    """
    Gets the word schema.

    :param collection_name: A name to give to the collection.

    :return dict: The schema.
    """
    return {
        "name": collection_name,
        "fields": [
            {
                "name": "word",
                "type": "string"
            },
            {
                "name": "word_priority_score",
                "type": "int32",
            },
        ],
        "default_sorting_field": "word_priority_score",
    }


def createTestWords(client: typesense.Client, collection_name: str = "words", max_words: int = None):
    """
    Inserts dictionary words into a Typesense collection.

    :param client: A typesense client instance.
    :param collection_name: The Typesense collection name.
    :param max_words: A maximum number of words to add.
    """

    # Delete the test schema if it's there.
    try:
        print("Deleting collection {}...".format(collection_name))
        client.collections[collection_name].delete()
    except ObjectNotFound:
        print("No existing collection found with name {}.".format(collection_name))
        pass

    # Create the schema.
    print("Creating collection {}...".format(collection_name))
    client.collections.create(getWordSchema(collection_name))
    print("Created collection {}.".format(collection_name))

    words = [line.strip() for line in urllib.request.urlopen(WORDS_FILE_URL).read().decode("utf-8").split("\n")]

    if max_words:
        print("{} Words found, indexing a maximum of {}...".format(len(words), max_words))
    else:
        print("{} Words found, indexing all...".format(len(words)))

    for i, word in enumerate(words):
        if max_words and i >= max_words:
            break

        client.collections[collection_name].documents.create({
            "id": str(i),
            "word": word,
            "word_priority_score": 10,
        })

    print("Indexing complete.")


class TestPagination(unittest.TestCase):
    api_key = ""
    host = "127.0.0.1"
    port = "8108"
    protocol = "http"
    collection_name = "words"
    timeout = 3
    max_pages = 10
    items_per_page = 10

    def test_pagination_duplication(self):
        """
        Tests to see if the pagination results duplicate.
        """
        previous_hits = []
        client = getSearch(api_key=self.api_key, host=self.host, port=self.port, protocol=self.protocol, timeout=3)

        for page in range(1, self.items_per_page + 1):
            result = client.collections[self.collection_name].documents.search({
                "q": "*",
                "items_per_page": self.items_per_page,
                "page": page,
            })

            if not result or "hits" not in result:
                break
            if previous_hits:
                msg = "Duplicate hits found starting at page {}.".format(page)
                self.assertNotEqual(result["hits"], previous_hits, msg)
            previous_hits = result["hits"]


if __name__ == "__main__":
    API_KEY = "abcd"
    COLLECTION = "words"
    HOST = "127.0.0.1"
    PORT = "8108"
    PROTOCOL = "http"
    TIMEOUT = 3
    MAX_WORDS = 2500
    MAX_PAGES = 10
    ITEMS_PER_PAGE = 10

    # Index up to a maximum amount of words.
    ts_client = getSearch(api_key=API_KEY, host=HOST, port=PORT, protocol=PROTOCOL, timeout=TIMEOUT)
    createTestWords(client=ts_client, collection_name=COLLECTION, max_words=MAX_WORDS)

    # Set variables for test case.
    TestPagination.host = HOST
    TestPagination.api_key = API_KEY
    TestPagination.collection_name = COLLECTION
    TestPagination.port = PORT
    TestPagination.protocol = PROTOCOL
    TestPagination.timeout = TIMEOUT
    TestPagination.max_pages = MAX_PAGES
    TestPagination.items_per_page = ITEMS_PER_PAGE

    # Run the tests.
    unittest.main()
