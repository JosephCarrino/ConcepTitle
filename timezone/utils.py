import os, json
from datetime import datetime

import spacy

nlp = spacy.load("en_core_web_lg")


def get_newspaper_time_articles(newspaper_dir: str, date: str, start_time: str, end_time: str,
                                time: str = "local_time") -> list:
    output = []
    titles_captured = []

    start_time = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M:%S")

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
            # time_obj = time.strptime()
            try:
                local_time = article[time]
            except:
                continue

            local_time = local_time.replace("T", " ")
            local_time = local_time.replace(".", ":")
            local_time = datetime.strptime(local_time, "%Y-%m-%d %H:%M:%S")
            if not start_time <= local_time <= end_time:
                continue
            en_title = article["en_title"]
            if en_title not in titles_captured:
                titles_captured.append(en_title)
                output.append(article)
    return output


def extract_articles(base_dir: str, news_paper: str, day: str, start_time: str, end_time: str, queue=None,
                     process_label=""):
    full_path = f"{base_dir}/{news_paper}"
    articles = get_newspaper_time_articles(full_path, day, start_time, end_time)
    if queue != None:
        queue.put((process_label, articles))
        return
    return articles

def extract_articles_scraping_time(base_dir: str, news_paper: str, day: str, start_time: str, end_time: str, queue=None,
                     process_label=""):
    full_path = f"{base_dir}/{news_paper}"
    articles = get_newspaper_time_articles(full_path, day, start_time, end_time, "scraping_time")
    if queue != None:
        queue.put((process_label, articles))
        return
    return articles


def calculate_nlp(article: dict) -> dict:
    article["cont_nlp"] = nlp(article["en_content"])
    return article


def calculate_similarity(art_a, art_b, threshold):
    similarity = art_a.similarity(art_b)
    if similarity >= threshold:
        return (True, similarity)
    else:
        return (False, similarity)
