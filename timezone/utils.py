import os, json


def get_newspaper_time_articles(newspaper_dir: str, date: str, start_time: str, end_time: str) -> list:
    output = []
    titles_captured = []
    for directory_entry in os.scandir(newspaper_dir):
        dir = f"{newspaper_dir}/{directory_entry.name}"
        with open(dir, "r", encoding="utf-8") as f:
            try:
                snapshot = json.load(f)
            except:
                pass
        if len(snapshot) == 0:
            pass
        first_article = snapshot[0]
        if "scraping_time" not in first_article or "timezone" not in first_article or "local_time" not in first_article or "en_title" not in first_article:
            continue

        for article in snapshot:
            en_title = article["en_title"]
            if en_title not in titles_captured:
                titles_captured.append(en_title)
                output.append(article)
    return output
