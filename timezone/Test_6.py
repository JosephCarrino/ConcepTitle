# Given a Day returns the not unique news vs the captured news in 3 hour belts

import multiprocessing
from datetime import datetime
from multiprocessing import Process
from utils import array_nlp, calculate_similarity, extract_articles
import matplotlib.pyplot as plt
import numpy as np

DAY = "2024-05-01"

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

COSINE_THRESHOLD = 0.9875


def draw_graph(nome_giornali_data: dict, min_value: int, max_value: int, i, HOURS):
    x_groups = ("Notizie ritenute non uniche", "Totale Notizie")
    x_arange = np.arange(len(x_groups))
    width = 0.90 / len(NEWS_PAPERS)
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')
    for attribute, measurement in nome_giornali_data.items():
        offset = width * multiplier
        rects = ax.bar(x_arange + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Numero di Notizie')
    ax.set_title(f"Notizie ritenute non uniche e Notizie Totali a confronto - TZ Taro - DALLE ORE {i}:00:00 ALLE ORE {i + HOURS - 1}:59:59")
    ax.set_xticks(x_arange + width, x_groups)
    ax.legend(loc='upper left', ncols=len(x_groups))
    ax.set_ylim(max(min_value - 5, 0), max_value)
    # plt.savefig(f"TEST 6 - {i}", dpi=500)
    plt.show()


def main():
    HOURS = 3
    for i in range(0, 24):
        if i % HOURS != 0:
            continue
        if i + HOURS - 1 >= 24:
            continue

        print(f"DALLE ORE {i}:00:00 ALLE ORE {i + HOURS - 1}:59:59 ")

        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        queue = multiprocessing.Queue()
        articles = []
        articles_new = []
        processes = []
        articles_nro = []
        articles_not_unique_title = []

        for (label, path) in enumerate(NEWS_PAPERS):
            tmp = Process(target=extract_articles,
                          args=(BASE_DIR, path, DAY, f"{i}:00:00", f"{i + HOURS - 1}:59:59", queue, label))
            processes.append(tmp)
            articles.append(None)
            articles_new.append([])

        for p in processes:
            p.start()

        for _ in processes:
            (label, articles_found) = queue.get()
            articles[label] = articles_found

        for p in processes:
            p.join()
            p.close()

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

        for p in processes:
            p.join()
            p.close()

        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        for (label_a, path_a) in enumerate(NEWS_PAPERS):
            for (label_b, path_b) in enumerate(NEWS_PAPERS):
                if label_a <= label_b:
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

        min_value = -1
        max_value = -1
        nome_giornali = {}

        for (label, path) in enumerate(NEWS_PAPERS):
            if min_value == -1:
                min_value = len(articles_not_unique_title[label])
            else:
                min_value = min(min_value, len(articles_not_unique_title[label]))

            if max_value == -1:
                max_value = articles_nro[label]
            else:
                max_value = max(max_value, articles_nro[label])

            nome_giornali[path] = (
                len(articles_not_unique_title[label]),
                articles_nro[label],
            )

        draw_graph(nome_giornali, min_value, max_value, i, HOURS)


if __name__ == '__main__':
    main()
