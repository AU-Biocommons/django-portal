"""Search ElasticSearch index for webpage content."""

from django.conf import settings
from whoosh import index
from whoosh.qparser import MultifieldParser, OrGroup

SEARCH_FIELDS = [
    "url",
    "title",
    "desciption",
    "headers",
    "body",
]


def search(query):
    ix = index.open_dir(settings.SEARCH_INDEX_DIR)
    with ix.searcher() as searcher:
        parser = MultifieldParser(
            SEARCH_FIELDS,
            schema=ix.schema,
            group=OrGroup,
        )
        parsed_query = parser.parse(query)
        hits = searcher.search(
            parsed_query,
            limit=None,
            sortedby="",
            terms=True,
        )

        return hits
