import re
import unicodedata
from enum import Enum

class BlogStatus(Enum):
    DRAFT = "DRAFT"
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