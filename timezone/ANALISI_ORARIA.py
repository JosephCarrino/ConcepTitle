# Given a Day returns the not unique news vs the captured news in 1 hour belts

from utils import calculate_similarity, extract_articles, array_nlp_cache, extract_homepage_articles, \
    extract_articles_scraping_time
import matplotlib.pyplot as plt
# matplotlib.use('Agg')
import numpy as np

DAY = "2024-05-20"
HOURS = 1
COSINE_THRESHOLD = 0.9875

BASE_DIR = "../../Newscraping/collectedNews/flow"

NEWS_PAPERS = [
    "PT/ExpressoPt",
    "IT/ANSA",
    "IT/AGI",
    "EN/SowetanLive",
    "PT/Brasil247",
    "EN/LosAngelesTimes",
    "EN/9News",
]

FUSI_ORARI = [
    "PT/ExpressoPt \n WEST (+1)",
    "IT/ANSA \n CEST (+2)",
    "IT/AGI \n CEST (+2)",
    "EN/SowetanLive \n SAST (+2) ",
    "PT/Brasil247 \n BRT (-3)",
    "EN/LosAngelesTimes \n PDT (-7)",
    "EN/9News \n AEST (+10)",
]


home_pages = [
    "https://www.latimes.com",
    "https://www.news.com.au",
    "https://www.riotimesonline.com",
    "https://www.sowetanlive.co.za",
    "https://www.agi.it",
    "https://www.ansa.it",
    "https://expresso.pt",
    "https://www.9news.com.au",
    "https://www.brasil247.com"
]

def draw_graph_2(nome_giornali_data_all: list, min_value: int, max_value: int, j, HOURS):
    no_graph = 4
    for i in range(0, len(nome_giornali_data_all)):
        if i % no_graph == no_graph - 1:
            continue

        fig, axs = plt.subplots(2, 2, figsize=(25, 15))
        for LINE in range(0, 2):
            for COL in range(0, 2):
                index_hr = LINE * 2 + COL
                nome_giornali_data = nome_giornali_data_all[index_hr]
                # nome_giornali_data_nd_line = nome_giornali_data_all[i + 1]

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

                bar_width = 0.25
                br1 = np.arange(len(giornali) // 2)
                br2 = [x + (bar_width / 2) for x in br1]
                br3 = [x + bar_width + 0.05 for x in br2]
                br4 = [x + (bar_width / 2) for x in br3]

                fig.suptitle(f"Numero di notizie TZ Taro vs Classic Taro.")
                b2 = axs[LINE][COL].bar(br2, notizie_totali, color='#0377fc', width=bar_width,
                                   edgecolor='grey', label="Notizie in Home page")
                b1 = axs[LINE][COL].bar(br1, notizie_uguali, color='r', width=bar_width,
                                   edgecolor='grey', label="Notizie non uniche")
                b4 = axs[LINE][COL].bar(br4, notizie_totali_st, color='y', width=bar_width,
                                   edgecolor='grey', label="Notizie in Home page (Classic Taro)")
                b3 = axs[LINE][COL].bar(br3, notizie_uguali_st, color='g', width=bar_width,
                                   edgecolor='grey', label="Notizie non uniche (Classic Taro)")
                axs[LINE][COL].bar_label(b2, fmt='%.0f')
                axs[LINE][COL].bar_label(b1, fmt='%.0f')
                axs[LINE][COL].bar_label(b4, fmt='%.0f')
                axs[LINE][COL].bar_label(b3, fmt='%.0f')
                axs[LINE][COL].legend()
                axs[LINE][COL].set_xlabel("Testate Giornalistiche")
                axs[LINE][COL].set_ylabel("Numero di notizie")
                axs[LINE][COL].title.set_text(f"Dalle ore {j - (no_graph - (index_hr + 1))}:00:00 alle ore {j - (no_graph - (index_hr + 1))}:59:59 DEL {DAY}")
                x_labels = [""]
                for label in giornali[0:len(giornali) // 2]:
                    x_labels.append(label)
                axs[LINE][COL].set_xticklabels(x_labels, fontsize=12, rotation=15)


        plt.savefig(f"ANALISI_ORARIA_{j - no_graph + 1}_{j}.png", dpi=100)
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

        for (label, path) in enumerate(FUSI_ORARI):
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

        for (label, path) in enumerate(FUSI_ORARI):
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
        if i % 4 == 3:
            draw_graph_2(nome_giornali_local_time[i - 3: i + 1], min_value, max_value, i, HOURS)


if __name__ == '__main__':
    main()
