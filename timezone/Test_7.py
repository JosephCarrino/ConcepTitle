# Given a day, a start time and an end time returns all news on HomePage of the various journals

from utils import calculate_similarity, extract_articles, extract_homepage_articles, calculate_nlp, get_unique_articles
import matplotlib.pyplot as plt
import numpy as np

DAY = "2024-05-04"
START_TIME = "09:00:00"
END_TIME = "12:00:00"
COSINE_THRESHOLD = 0.9875

BASE_DIR = "../../Newscraping/collectedNews/flow"

NEWS_PAPERS = [
    "IT/ANSA",
    "IT/AGI",
    "PT/ExpressoPt",
    "EN/LosAngelesTimes",
    "EN/NewsComAu",
    "EN/RioTimes",
    "EN/SowetanLive",
]

home_pages = [
    "https://www.latimes.com",
    "https://www.news.com.au",
    "https://www.riotimesonline.com",
    "https://www.sowetanlive.co.za",
    "https://www.agi.it",
    "https://www.ansa.it",
    "https://expresso.pt"
]

def draw_graph(nome_giornali_data: dict, min_value: int, max_value: int):
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
    ax.set_title(f"Notizie ritenute non uniche e Notizie Totali a confronto - TZ Taro")
    ax.set_xticks(x_arange + width, x_groups)
    ax.legend(loc='upper left', ncols=len(x_groups))
    ax.set_ylim(max(min_value - 5, 0), max_value)
    # plt.savefig(f"TEST 6 - {i}", dpi=500)
    plt.show(block=True)


def main():
    news_papers_articles = []
    articles_not_unique_title = []
    articles_nro = []

    for news_paper in NEWS_PAPERS:
        articles = extract_articles(BASE_DIR, news_paper, DAY, START_TIME, END_TIME)
        articles = extract_homepage_articles(articles, home_pages)
        mapped = []
        for article in articles:
            mapped.append(calculate_nlp(article))
        news_papers_articles.append(mapped)
        articles_not_unique_title.append([])
        articles_nro.append(len(articles))


    for (label_a, path_a) in enumerate(NEWS_PAPERS):
        for (label_b, path_b) in enumerate(NEWS_PAPERS):
            if label_a <= label_b:
                continue

            for article_a in news_papers_articles[label_a]:
                for article_b in news_papers_articles[label_b]:
                    (similarity, percentage) = calculate_similarity(article_a["cont_nlp"], article_b["cont_nlp"],
                                                                        COSINE_THRESHOLD)
                    if similarity:
                        if article_a["en_title"] not in articles_not_unique_title[label_a]:
                            articles_not_unique_title[label_a].append(article_a["en_title"])
                        if article_b["en_title"] not in articles_not_unique_title[label_b]:
                            articles_not_unique_title[label_b].append(article_b["en_title"])

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

    draw_graph(nome_giornali, min_value, max_value)

if __name__ == '__main__':
    main()
