# Given a Day returns the not unique news vs the captured news in 1 hour belts

from utils import calculate_similarity, extract_articles, array_nlp_cache, extract_homepage_articles, \
    extract_articles_scraping_time
import matplotlib.pyplot as plt
# matplotlib.use('Agg')
import numpy as np

DAY = "2024-05-08"
HOURS = 1
COSINE_THRESHOLD = 0.9875

BASE_DIR = "../../Newscraping/collectedNews/flow"

NEWS_PAPERS = [
    "IT/ANSA",
    "IT/AGI",
    "PT/ExpressoPt",
    "EN/LosAngelesTimes",
    "EN/NewsComAu",  # TODO: CHANGE
    "EN/RioTimes",  # TODO: CHANGE
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


def draw_graph(nome_giornali_data: dict, min_value: int, max_value: int, i, HOURS):
    x_groups = ("Notizie ritenute non uniche", "Totale Notizie")
    x_arange = np.arange(len(x_groups))
    width = 0.90 / len(NEWS_PAPERS)
    multiplier = 0

    fig, ax = plt.subplots(2, 1)
    for attribute, measurement in nome_giornali_data.items():
        if "st" in attribute:
            continue
        offset = width * multiplier
        rects = ax.bar(x_arange + offset, measurement, width, label=attribute)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Numero di Notizie')
    ax.set_title(
        f"Notizie ritenute non uniche e Notizie Totali a confronto - TZ Taro - DALLE ORE {i}:00:00 ALLE ORE {i + HOURS - 1}:59:59")
    ax.set_xticks(x_arange + width, x_groups)
    ax.legend(loc='upper left', ncol=len(x_groups))
    ax.set_ylim(max(min_value - 5, 0), max_value)
    plt.show()


def draw_graph_2(nome_giornali_data_all: list, min_value: int, max_value: int, j, HOURS):
    for i in range(0, len(nome_giornali_data_all)):
        if i % 2 == 1:
            continue
        nome_giornali_data = nome_giornali_data_all[i]
        nome_giornali_data_nd_line = nome_giornali_data_all[i + 1]

        giornali = list(nome_giornali_data.keys())
        notizie_uguali = []
        notizie_totali = []
        notizie_uguali_st = []
        notizie_totali_st = []
        for index, data in enumerate(nome_giornali_data.values()):
            if "st_" in giornali[index]:
                notizie_uguali.append(data[0])
                notizie_totali.append(data[1])
            else:
                notizie_uguali_st.append(data[0])
                notizie_totali_st.append(data[1])

        bar_width = 0.3
        br1 = np.arange(len(giornali) // 2)
        br2 = [x + bar_width for x in br1]

        fig, axs = plt.subplots(2, 2, figsize=(25, 15))
        fig.suptitle(f"Numero di notizie TZ Taro vs Classic Taro.")
        axs[0][0].bar(br1, notizie_uguali, color='r', width=bar_width,
                      edgecolor='grey', label="Notizie non uniche")
        axs[0][0].bar(br2, notizie_totali, color='b', width=bar_width,
                      edgecolor='grey', label="Notizie in Home page")
        axs[0][0].legend()
        axs[0][0].set_xlabel("Timezone TARO")
        axs[0][0].set_ylabel("Numero di notizie")
        axs[0][0].title.set_text(f"TZ Taro - Dalle ore {j - 1}:00:00 alle ore {j - 1 + HOURS - 1}:59:59")
        x_labels = [""]
        for label in giornali[0:len(giornali) // 2]:
            x_labels.append(label)
        axs[0][0].set_xticklabels(x_labels, fontsize=7)
        axs[0][1].bar(br1, notizie_uguali_st, color='r', width=bar_width,
                      edgecolor='grey', label="Notizie non uniche")
        axs[0][1].bar(br2, notizie_totali_st, color='b', width=bar_width,
                      edgecolor='grey', label="Notizie in Home page")
        axs[0][1].legend()
        axs[0][1].set_xlabel("Classic TARO")
        axs[0][1].set_ylabel("Numero di notizie")
        axs[0][1].title.set_text(f"Classic Taro - Dalle ore {j - 1}:00:00 alle ore {j - 1 + HOURS - 1}:59:59")
        x_labels = [""]
        for label in giornali[0:len(giornali) // 2]:
            x_labels.append(label)
        axs[0][1].set_xticklabels(x_labels, fontsize=7)

        # GRAFICI SOTTO
        giornali = list(nome_giornali_data_nd_line.keys())
        notizie_uguali = []
        notizie_totali = []
        notizie_uguali_st = []
        notizie_totali_st = []
        for index, data in enumerate(nome_giornali_data_nd_line.values()):
            if "st_" in giornali[index]:
                notizie_uguali.append(data[0])
                notizie_totali.append(data[1])
            else:
                notizie_uguali_st.append(data[0])
                notizie_totali_st.append(data[1])

        bar_width = 0.3
        br1 = np.arange(len(giornali) // 2)
        br2 = [x + bar_width for x in br1]

        axs[1][0].bar(br1, notizie_uguali, color='r', width=bar_width,
                      edgecolor='grey', label="Notizie non uniche")
        axs[1][0].bar(br2, notizie_totali, color='b', width=bar_width,
                      edgecolor='grey', label="Notizie in Home page")
        axs[1][0].legend()
        axs[1][0].set_xlabel("Timezone TARO")
        axs[1][0].set_ylabel("Numero di notizie")
        axs[1][0].title.set_text(f"TZ Taro - Dalle ore {j}:00:00 alle ore {j + HOURS - 1}:59:59")
        x_labels = [""]
        for label in giornali[0:len(giornali) // 2]:
            x_labels.append(label)
        axs[1][0].set_xticklabels(x_labels, fontsize=7)
        axs[1][1].bar(br1, notizie_uguali_st, color='r', width=bar_width,
                      edgecolor='grey', label="Notizie non uniche")
        axs[1][1].bar(br2, notizie_totali_st, color='b', width=bar_width,
                      edgecolor='grey', label="Notizie in Home page")
        axs[1][1].legend()
        axs[1][1].set_xlabel("Classic TARO")
        axs[1][1].set_ylabel("Numero di notizie")
        axs[1][1].title.set_text(f"Classic Taro - Dalle ore {j}:00:00 alle ore {j + HOURS - 1}:59:59")
        x_labels = [""]
        for label in giornali[0:len(giornali) // 2]:
            x_labels.append(label)
        axs[1][1].set_xticklabels(x_labels, fontsize=7)

        plt.savefig(f"ANALISI_ORARIA_{j - 1}_{j}.png", dpi=100)
        # plt.show(block=True)
        plt.close()


def main():
    cache_articles_titles = []
    cache_articles_content = []
    nome_giornali_local_time = []

    for i in range(0, 24):
        if i % HOURS != 0:
            continue
        if i + HOURS - 1 >= 24:
            continue

        print(f"DALLE ORE {i}:00:00 ALLE ORE {i + HOURS - 1}:59:59 ")

        nome_giornali_local_time.append({})
        articles = []
        articles_st = []
        articles_nro = []
        articles_not_unique_title = []
        articles_nro_st = []
        articles_not_unique_title_st = []

        for (label, path) in enumerate(NEWS_PAPERS):
            extracted_articles = extract_articles(BASE_DIR, path, DAY, f"{i}:00:00", f"{i + HOURS - 1}:59:59")
            extracted_articles = extract_homepage_articles(extracted_articles, home_pages)
            extracted_articles_st = extract_articles_scraping_time(BASE_DIR, path, DAY, f"{i}:00:00",
                                                                   f"{i + HOURS - 1}:59:59")
            extracted_articles_st = extract_homepage_articles(extracted_articles_st, home_pages)
            articles.append(extracted_articles)
            articles_st.append(extracted_articles_st)
            cache_articles_titles.append([])
            cache_articles_content.append([])

        for (index, article_set) in enumerate(articles):
            articles[index] = array_nlp_cache(articles[index], index, cache_articles_titles, cache_articles_content)
            articles_st[index] = array_nlp_cache(articles_st[index], index, cache_articles_titles,
                                                 cache_articles_content)
            articles_nro.append(len(articles[index]))
            articles_not_unique_title.append([])
            articles_nro_st.append(len(articles_st[index]))
            articles_not_unique_title_st.append([])

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

        for (label_a, path_a) in enumerate(NEWS_PAPERS):
            for (label_b, path_b) in enumerate(NEWS_PAPERS):
                if label_a <= label_b:
                    continue

                for article_a in articles_st[label_a]:
                    for article_b in articles_st[label_b]:
                        (similarity, percentage) = calculate_similarity(article_a["cont_nlp"], article_b["cont_nlp"],
                                                                        COSINE_THRESHOLD)
                        if similarity:
                            if article_a["en_title"] not in articles_not_unique_title_st[label_a]:
                                articles_not_unique_title_st[label_a].append(article_a["en_title"])
                            if article_b["en_title"] not in articles_not_unique_title_st[label_b]:
                                articles_not_unique_title_st[label_b].append(article_b["en_title"])

        min_value = -1
        max_value = -1

        for (label, path) in enumerate(NEWS_PAPERS):
            if min_value == -1:
                min_value = len(articles_not_unique_title[label])
            else:
                min_value = min(min_value, len(articles_not_unique_title[label]))

            if max_value == -1:
                max_value = articles_nro[label]
            else:
                max_value = max(max_value, articles_nro[label])

            nome_giornali_local_time[i][path] = (
                len(articles_not_unique_title[label]),
                articles_nro[label],
            )

        min_value = -1
        max_value = -1

        for (label, path) in enumerate(NEWS_PAPERS):
            if min_value == -1:
                min_value = len(articles_not_unique_title_st[label])
            else:
                min_value = min(min_value, len(articles_not_unique_title_st[label]))

            if max_value == -1:
                max_value = articles_nro_st[label]
            else:
                max_value = max(max_value, articles_nro_st[label])

            nome_giornali_local_time[i][f"st_{path}"] = (
                len(articles_not_unique_title_st[label]),
                articles_nro_st[label],
            )

        del articles
        del articles_st
        del articles_nro
        del articles_nro_st
        del articles_not_unique_title
        del articles_not_unique_title_st
        if i % 2 == 1:
            draw_graph_2(nome_giornali_local_time[i - 1: i + 1], min_value, max_value, i, HOURS)


if __name__ == '__main__':
    main()
