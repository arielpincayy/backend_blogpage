import re
import unicodedata
from enum import Enum
import json

class BlogStatus(Enum):
    PUBLISHED = "PUBLISHED"
    WAITING = "WAITING"
    REFUSED = "REFUSED"

def slugify(text: str) -> str:
    """
    Converts a string into a URL-friendly slug.
    """
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text).strip('-')
    return text


def convertToMDX(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    header = data['header']
    content = data['content']

    keywords = ', '.join([f'"{k}"' for k in header['keywords']])
    frontmatter = f'''---
title: "{header["title"]}"
---
**keywords**: {keywords}
'''
    body = []
    for section in content:
        type_content = section.get('typeContent')
        value = section.get('content', '')
        if type_content in ('image', 'pdf'):
            if type_content == 'image':
                body.append(f'![imagen]({value})')
            elif type_content == 'pdf':
                body.append(f'<PDF src="{value}" />')
        else:
            if type_content == 'subtitle':
                body.append(f'## {value}')
            elif type_content == 'text':
                body.append(value)
            elif type_content == 'code':
                body.append(f'```py\n{value}\n```')
            elif type_content == 'latex':
                body.append(f'$$\n{value}\n$$')
            else:
                body.append('')
    mdx_content = frontmatter + '\n\n' + '\n\n'.join(body)
    return mdx_content

