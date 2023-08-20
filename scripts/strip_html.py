"""Strip hard-coded styling from HTML files."""

import re


def strip_span(line):
    """Remove span elements from HTML line."""
    if '<span' not in line.replace('</', '<'):
        return line
    if 'class="material-icons"' in line:
        return line
    return ""


def strip_style(line):
    """Remove style elements from HTML line."""
    if 'style=' not in line:
        return line
    return re.sub(r'style=".*?"', '', line)


in_files = [
    'input/terms.html',
]

for file in in_files:
    with open(file, 'r') as f:
        text = f.read()
    text = text.replace('<', '\n<')
    text = text.replace('>', '>\n')
    clean_lines = []
    for line in text.split('\n'):
        cleaned = strip_span(line)
        cleaned = strip_style(cleaned)
        cleaned = cleaned.strip()
        if cleaned:
            clean_lines.append(cleaned)

    outfile = file.replace('input/', 'output/')
    with open(outfile, 'w') as f:
        f.write('\n'.join(clean_lines))
    print(f"Stripped {file} to {outfile}")
