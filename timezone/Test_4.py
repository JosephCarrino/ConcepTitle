# Given two newspapers returns the simils articles with name and links IN THEIR TIMEZONES

import multiprocessing
from datetime import datetime
from multiprocessing import Process
from utils import extract_articles, calculate_nlp, array_nlp, calculate_similarity

# python3 -m spacy download en_core_web_trf

DAY = "2024-05-01"
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

COSINE_THRESHOLD = 0.98


def main():
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    queue = multiprocessing.Queue()
    articles = []
    articles_new = []
    processes = []
    articles_nro = []
    articles_not_unique_title = []

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
        articles_nro.append(len(article_set))
        articles_not_unique_title.append([])

    for p in processes:
        p.start()

    for _ in processes:
        (articles_found, label) = queue.get()
        articles[label] = articles_found

    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    for (label_a, path_a) in enumerate(NEWS_PAPERS):
        for (label_b, path_b) in enumerate(NEWS_PAPERS):
            if label_a == label_b:
                continue

            for article_a in articles[label_a]:
                for article_b in articles[label_b]:
                    (similarity, percentage) = calculate_similarity(article_a["cont_nlp"], article_b["cont_nlp"],
                                                                    COSINE_THRESHOLD)
                    if similarity:
                        if article_a["en_title"] not in articles_not_unique_title[label_a]:
                            articles_not_unique_title[label_a].append(article_a["en_title"])
                        if article_b["en_title"] not in articles_not_unique_title[label_b]:
                            articles_not_unique_title[label_b].append(article_b["en_title"])
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    articles = []

if __name__ == '__main__':
    main()
