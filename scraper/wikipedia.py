import requests

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

print(get_article("wertghj"))