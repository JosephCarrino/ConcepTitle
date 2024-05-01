# Given two newspapers returns the simils articles with name and links IN THEIR TIMEZONES

import multiprocessing
from datetime import datetime
from multiprocessing import Process
from utils import extract_articles, calculate_nlp, array_nlp

# python3 -m spacy download en_core_web_trf

DAY = "2024-04-30"
START_TIME = "12:00:00"
END_TIME = "15:00:00"

BASE_DIR = "../../Newscraping/collectedNews/flow"

NEWS_PAPERS = [
    "IT/ANSA_Politica",
    "IT/AGI_Politica",
    "IT/ANSA_Esteri",
    "IT/AGI_Esteri",
    "PT/ExpressoPt",
    "EN/LosAngelesTimes",
    "EN/NewsComAu",
    "EN/RioTimes",
    "EN/SowetanLive",
]

COSINE_THRESHOLD = 0.97


def main():
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    queue = multiprocessing.Queue()
    articles = []
    articles_new = []
    processes = []
    for (label, path) in enumerate(NEWS_PAPERS):
        tmp = Process(target=extract_articles, args=(BASE_DIR, path, DAY, START_TIME, END_TIME, queue, label))
        processes.append(tmp)
        articles.append(None)
        articles_new.append([])

    for p in processes:
        p.start()

    for _ in processes:
        (label, articles_found) = queue.get()
        articles[label] = articles_found
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    processes = []
    queue = multiprocessing.Queue()
    for (index, article_set) in enumerate(articles):
        tmp = Process(target=array_nlp, args=(article_set, index, queue))
        processes.append(tmp)

    for p in processes:
        p.start()

    for _ in processes:
        (articles_found, label) = queue.get()
        articles[label] = articles_found

    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    articles = []

    #TODO: CONTINUE HERE

    """
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
            (similarity, percentage) = calculate_similarity(article_a["cont_nlp"], article_b["cont_nlp"],
                                                            COSINE_THRESHOLD)
            if similarity:
                simils.append((article_a, article_b, percentage))

    for simil_triple in simils:
        at = simil_triple[0]["title"]
        an = simil_triple[0]["news_url"]
        bt = simil_triple[1]["title"]
        bn = simil_triple[1]["news_url"]
        print(f"{at} - {an} - {bt} - {bn} - {simil_triple[2]}")
    
    """


if __name__ == '__main__':
    main()
