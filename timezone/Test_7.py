# Given a day, a start time and an end time returns all news on HomePage of the various journals

import multiprocessing
from datetime import datetime
from multiprocessing import Process
from utils import array_nlp, calculate_similarity, extract_articles, extract_homepage_articles
import matplotlib.pyplot as plt
import numpy as np

DAY = "2024-05-04"
START_TIME = "09:00:00"
END_TIME = "12:00:00"

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


def main():
    for news_paper in NEWS_PAPERS:
        articles = extract_articles(BASE_DIR, news_paper, DAY, START_TIME, END_TIME)
        articles = extract_homepage_articles(articles, home_pages)
        articles = []

if __name__ == '__main__':
    main()
