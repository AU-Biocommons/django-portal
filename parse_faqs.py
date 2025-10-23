import json
import re
from bs4 import BeautifulSoup


CARD_HEADER = r'<button[^>]+>(.+?)</button>'
CARD_BODY = r'<div class="card-body">(.+?)</div>'
FAQS_OUTPUT_JSON = 'app/home/migrations/data/faqs.json'

relpath = 'app/home/templates/home/resources/faqs-old.html'
data = []


def html_text_collapse(string):
    soup = BeautifulSoup(string, "html.parser")
    return soup.prettify()


with open(relpath) as f:
    content = f.read().replace('\n', ' ')
    headers = [
        html_text_collapse(x) for x in re.findall(CARD_HEADER, content)
    ]
    bodies = [
        html_text_collapse(x) for x in re.findall(CARD_BODY, content)
    ]

assert len(headers) == len(bodies)
data = [
    {
        'question': header,
        'answer': body,
    }
    for header, body in zip(headers, bodies)
]

with open(FAQS_OUTPUT_JSON, 'w') as f:
    json.dump(data, f, indent=2)
