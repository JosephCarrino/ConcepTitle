import os, json
from datetime import datetime, timedelta

import spacy

nlp = spacy.load("en_core_web_lg")


def get_newspaper_time_articles(newspaper_dir: str, date: str, start_time: str, end_time: str,
                                time: str = "local_time") -> list:
    output = []
    titles_captured = []

    start_time = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M:%S")
    current_date = datetime.strptime(date, "%Y-%m-%d")
    check_days = [
        (current_date - timedelta(days=1)).strftime('%Y-%m-%d'),
        date,
        (current_date + timedelta(days=1)).strftime('%Y-%m-%d')
    ]

    for directory_entry in os.scandir(newspaper_dir):
        dir = f"{newspaper_dir}/{directory_entry.name}"
        should_check = False
        for tmp_d in check_days:
            if tmp_d in directory_entry.name:
                should_check = True

        if not should_check:
            continue
        with open(dir, "r", encoding="utf-8") as f:
            try:
                snapshot = json.load(f)
                if len(snapshot) == 0:
                    continue
                first_article = snapshot[0]
            except:
                continue

        if "scraping_time" not in first_article or "timezone" not in first_article or "local_time" not in first_article or "en_title" not in first_article or "content_NER" not in first_article:
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

            try:
                en_title = article["en_title"]
                if en_title not in titles_captured:
                    titles_captured.append(en_title)
                    output.append(article)
            except:
                continue
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


def array_nlp(article_set: list, label, queue=None):
    output = []
    for new in article_set:
        output.append(calculate_nlp(new))
    queue.put((output, label))

def array_nlp_cache(article_set: list, label, cache_titles: list, cache_content: list):
    output = []
    for new in article_set:
        if new["en_title"] in cache_titles[label]:
            i = cache_titles[label].index(new["en_title"])
            content = cache_content[label][i]
            output.append(content)
        else:
            new_calculated = calculate_nlp(new)
            cache_titles[label].append(new["en_title"])
            cache_content[label].append(new_calculated)
            output.append(new_calculated)
    return output


def calculate_similarity(art_a, art_b, threshold):
    similarity = art_a.similarity(art_b)
    if similarity >= threshold:
        return (True, similarity)
    else:
        return (False, similarity)


def remove_slashes(link: str):
    if len(link) == 0:
        return link
    if link[-1] == '/':
        return remove_slashes(link[0:-1])
    else:
        return link


def extract_homepage_articles(articles: list, home_page_links: list):
    out = []

    for article in articles:
        if remove_slashes(article["url"]) in home_page_links:
            out.append(article)

    return out


def get_unique_articles(articles: list) -> list:
    titles = []
    out = []
    for article in articles:
        if article["en_title"] not in titles:
            titles.append(article["en_title"])
            out.append(article)
    return out
