import re 
from scraper.wikipedia import get_article


def chunk_article_data(article_data: dict) -> list[dict]:
    
    regex_pattern = r"^(={2,4})\s*(.+?)\s*\1\s*$"
    text_data = article_data["text"]
    matches = list(re.finditer(regex_pattern, text_data, re.MULTILINE))

    chunks = []
    intro_text = text_data[:matches[0].start()] # .start() is a method on a regex match object - returns the index position (an integer) in the string where that match begins.
    chunks.append({
        "text" : intro_text.strip(),
        "article_title": article_data["title"],
        "section": "Intro",
        "subsection": None,
        "page_id": article_data["page_id"]
    })

    BOILERPLATE_HEADINGS = {"See also", "Notes", "References", "External links", "Citations", "Bibliography"}   # issue if wikipedia (language code) is not english

    '''
    Each time  hit a === subsection,  need to know which == section it belongs to. 
    # So  need to remember "the most recent == heading I saw" as you walk through the loop. 
    # That's current_section.
    '''

    current_section = None
    current_subsection = None

    for i, match in enumerate(matches):
        number_of_equal_signs = len(match.group(1))
        heading_name = match.group(2) #

        
        if i + 1 < len(matches):
            content = text_data[match.end():matches[i + 1].start()] #
        else:
            content = text_data[match.end():] #

        if heading_name in BOILERPLATE_HEADINGS:
            continue
        if not content.strip():
            continue

        if number_of_equal_signs == 2:
            current_section = heading_name
            current_subsection = None
            chunks.append({
                "text" : content.strip(),
                "article_title": article_data["title"],
                "section": current_section,
                "subsection": current_subsection,
                "page_id": article_data["page_id"]
            })
        
        elif number_of_equal_signs == 3:
            current_subsection = heading_name
            chunks.append({
                "text" : content.strip(),
                "article_title": article_data["title"],
                "section": current_section,
                "subsection": current_subsection,
                "page_id": article_data["page_id"]
            })       

        elif number_of_equal_signs == 4:    # merge to the heading of 3
            chunks[-1]["text"] = chunks[-1]["text"] + f" \n\n{heading_name}:" + content.strip()

    return chunks
        



