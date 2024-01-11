"""Build Elasticsearch index for URL endpoints."""

import subprocess
import sys
import time
from bs4 import BeautifulSoup
from django.conf import settings
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError
from whoosh.fields import SchemaClass, ID, TEXT
from whoosh.analysis import StemmingAnalyzer
from whoosh import index

RUNSERVER_WAIT_SECONDS = 3


class PageSchema(SchemaClass):
    title = TEXT(stored=True, analyzer=StemmingAnalyzer())
    description = TEXT(stored=True, analyzer=StemmingAnalyzer())
    headings = TEXT(stored=True, analyzer=StemmingAnalyzer())
    body = TEXT(stored=True, analyzer=StemmingAnalyzer())
    url = ID(stored=True)


class Runserver:
    """Run Django development server to be queried by ElasticSearch."""

    HOSTNAME = '127.0.0.1:8000'
    ARGS = (
        sys.executable,
        'manage.py',
        'runserver',
        HOSTNAME,
    )

    def __init__(self):
        try:
            self.server = subprocess.Popen(
                self.ARGS,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as exc:
            print(exc)
            raise RuntimeError(
                'Could not run Django development server'
                ' - check errors above.')

    def __enter__(self):
        time.sleep(RUNSERVER_WAIT_SECONDS)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.terminate()

    def terminate(self):
        if self.server.poll() is not None:
            stdout, stderr = self.server.communicate()
            if self.server.returncode:
                print(f'\nDjango development server exited with code'
                      f' {self.server.returncode}')
                print("\nServer stderr:")
                print(stderr.decode('utf-8'))
        self.server.terminate()


def build_index():
    settings.SEARCH_INDEX_DIR.mkdir(exist_ok=True)
    ix = index.create_in(settings.SEARCH_INDEX_DIR, PageSchema)

    docs = []
    with Runserver() as server:
        for relpath in settings.SITE_SEARCH_URLS:
            url = f'http://{server.HOSTNAME}/{relpath.strip("/")}'
            print(f"Fetching HTML content for webpage: {url}")
            try:
                html = urlopen(url).read()
            except URLError as exc:
                url_file = Path(__file__).parent / 'url.py'
                sys.stderr.write(str(exc))
                sys.stderr.write(
                    f'\n\nError: could not open URL {url}.\n'
                    f' Please check {url_file} and confirm that this URL is'
                    ' valid.')
                server.terminate()
                return 0
            content = extract_data_fields(html)
            doc = {**content, 'url': relpath}
            docs.append(doc)

    ix_count = 0
    writer = ix.writer()
    for doc in docs:
        print(f"Indexing webpage: {doc['url']}")
        writer.add_document(**doc)
        ix_count += 1
    writer.commit()

    return ix_count


def extract_data_fields(html):
    """Strip HTML tags and return text."""
    def get_text(selector):
        match = soup.find(selector)
        if match:
            return match.get_text()
        return ''

    soup = BeautifulSoup(html, features="html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    title = get_text('title').replace('| Apollo Portal', '')
    description = get_text('meta[name="description"]')
    headings = '\n'.join([
        h.get_text()
        for h in soup.find_all('h1,h2,h3,h4')
    ])
    raw_text = get_text('main')
    lines = (
        line.strip()
        for line in raw_text.splitlines()
    )
    chunks = (
        phrase.strip()
        for line in lines
        for phrase in line.split("  ")
    )
    body = '\n'.join(chunk for chunk in chunks if chunk)
    return {
        'title': title,
        'description': description,
        'headings': headings,
        'body': body,
    }
