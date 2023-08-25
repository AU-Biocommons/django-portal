"""Strip hard-coded styling from HTML files."""

import re

keep_span_close = False


def strip_span(line):
    """Remove span elements from HTML line."""
    global keep_span_close
    if '<span' not in line.replace('</', '<'):
        return line
    if 'class="material-icons"' in line:
        return line
    if keep_span_close and '</span>' in line:
        keep_span_close = False
        return line
    return ""


def strip_style(line):
    """Remove style attributes from HTML line."""
    if 'style=' not in line:
        return line
    return re.sub(r'style=".*?"', '', line)


def strip_class(line):
    """Remove class attributes from HTML line."""
    if 'class=' not in line:
        return line
    return line.replace(' class="myclass"', '')


in_files = [
    'input/docs.html',
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
        cleaned = strip_class(cleaned)
        cleaned = cleaned.strip()
        if cleaned:
            clean_lines.append(cleaned)

    outfile = file.replace('input/', 'output/')
    with open(outfile, 'w') as f:
        f.write('\n'.join(clean_lines))
    print(f"Stripped {file} to {outfile}")
