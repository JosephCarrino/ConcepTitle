# Given two newspapers check the number of news similar
import multiprocessing
from multiprocessing import Process
from utils import extract_articles, calculate_nlp, calculate_similarity
from multiprocessing import Pool

DAY = "2024-04-20"
START_TIME = "08:00:00"
END_TIME = "12:59:59"

BASE_DIR = "../Newscraping/collectedNews/flow"
NEWSPAPER_A = "EN/RioTimes"
NEWSPAPER_B = "EN/NewsComAu"
COSINE_THRESHOLD = 0.95


def main():
    queue = multiprocessing.Queue()
    pa = Process(target=extract_articles, args=(BASE_DIR, NEWSPAPER_A, DAY, START_TIME, END_TIME, queue, "A"))
    pb = Process(target=extract_articles, args=(BASE_DIR, NEWSPAPER_B, DAY, START_TIME, END_TIME, queue, "B"))
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
    no_processor = multiprocessing.cpu_count()
    no_processor = max(no_processor - 2, 1)

    with Pool(no_processor) as p:
        articles_a = p.map(calculate_nlp, articles_a)

    with Pool(no_processor) as p:
        articles_b = p.map(calculate_nlp, articles_b)


    simils = []
    for article_a in articles_a:
        for article_b in articles_b:
            (similarity, percentage) = calculate_similarity(article_a["cont_nlp"], article_b["cont_nlp"], COSINE_THRESHOLD)
            if similarity:
                simils.append((article_a, article_b, percentage))

    print(len(simils))


if __name__ == '__main__':
    main()
