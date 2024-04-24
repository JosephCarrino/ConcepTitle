# Given two newspapers returns the simils articles with name and links in Scraping time

import multiprocessing
from multiprocessing import Process
from utils import calculate_nlp, calculate_similarity, extract_articles_scraping_time

# python3 -m spacy download en_core_web_trf

DAY = "2024-04-20"
START_TIME = "08:00:00"
END_TIME = "20:00:00"

BASE_DIR = "../../Newscraping/collectedNews/flow"

NEWSPAPER_A = "IT/ANSA_Esteri"
NEWSPAPER_B = "EN/SowetanLive"

COSINE_THRESHOLD = 0.97


def main():
    queue = multiprocessing.Queue()
    pa = Process(target=extract_articles_scraping_time, args=(BASE_DIR, NEWSPAPER_A, DAY, START_TIME, END_TIME, queue, "A"))
    pb = Process(target=extract_articles_scraping_time, args=(BASE_DIR, NEWSPAPER_B, DAY, START_TIME, END_TIME, queue, "B"))
    pa.start()
    pb.start()
    articles_a = None
    articles_b = None
    (label, articles) = queue.get()
    if label == "A":
        articles_a = articles
    elif label == "B":
        articles_b = articles

    (label, articles) = queue.get()
    if articles_b is None:
        articles_b = articles
    else:
        articles_a = articles

    del label
    del articles

    new_a = []
    new_b = []

    for article in articles_a:
        article = calculate_nlp(article)
        new_a.append(article)

    del articles_a

    for article in articles_b:
        article = calculate_nlp(article)
        new_b.append(article)

    del articles_b


    simils = []
    for article_a in new_a:
        for article_b in new_b:
            (similarity, percentage) = calculate_similarity(article_a["cont_nlp"], article_b["cont_nlp"], COSINE_THRESHOLD)
            if similarity:
                simils.append((article_a, article_b, percentage))

    for simil_triple in simils:
        at = simil_triple[0]["title"]
        an = simil_triple[0]["news_url"]
        bt = simil_triple[1]["title"]
        bn = simil_triple[1]["news_url"]
        print(f"{at} - {an} - {bt} - {bn} - {simil_triple[2]}")


if __name__ == '__main__':
    main()
