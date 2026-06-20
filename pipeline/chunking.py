import re 
from scraper.wikipedia import get_article


def chunk_article_data(article_data: dict) -> list[dict]:
    
    pattern = r"^(={2,4})\s*(.+?)\s*\1\s*$"
    text_data = article_data["text"]

    for match in re.finditer(pattern, text_data, re.MULTILINE):
        print(match.group(1), "|", match.group(2))

print(chunk_article_data(get_article("Madrid")))


