import requests
from urllib.parse import urlsplit, unquote

def get_article(title: str) -> dict | None:
    try:
        response = requests.get(
            "https://en.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "titles": title,
                "prop": "extracts",
                "format": "json",
                "explaintext": True,
            },
            headers={
                "User-Agent": "wiki-rag-learning-project/0.1 (zineb@nadak.ai)"
            },
        )
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch '{title}' from Wikipedia: {e}")

    parsed_json = response.json()
    pages = parsed_json["query"]["pages"]
    pages_values = list(pages.values())

    if "missing" in pages_values[0]:
        return None
    
    page_id = pages_values[0]["pageid"]
    page_title = pages_values[0]["title"]
    text = pages_values[0]["extract"]

    return {"page_id": page_id, "title": page_title, "text": text}



def extract_title_from_url(url: str) -> tuple[str, str] | None:
    parts = urlsplit(url)
    path_items = parts.path.split("/")

    try:
        wiki_index = path_items.index("wiki")
    except ValueError:
        return None

    title = unquote(path_items[wiki_index + 1]).replace("_", " ")
    lang = parts.netloc.split(".")[0]
    return title, lang


print(extract_title_from_url("https://en.wikipedia.org/wiki/Octopus"))



