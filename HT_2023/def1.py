# 1. Given a news, who skipped it?
# 1. Data una notizia totalmente contenuta nel file indicato da news_snap
#    Quale giornale, di quelli dati riporta la stessa notizia?


import json
import random
from utils import snapped_news_by_source, has_similar_in_snapshot
import warnings
from typing import List
warnings.filterwarnings("ignore")

snap_dir = "ANSA_Politica"
news_snap = "ner_en_2024-04-05T10.00.23E1712311223.224481.json"
main_dir = "../../Newscraping/collectedNews/flow/IT"

skip_dirs = ["AGI_Politica"]
SENTIMENT_ANALYSIS = False

to_check_dir = f"{main_dir}/{snap_dir}/{news_snap}"

def main():
    to_check = main_news_getter(to_check_dir)
    skipped_by(to_check)

def skipped_by(to_check: dict) -> List[str]:
    skipping_sources = []
    for skip_dir in skip_dirs:
        snapped = snapped_news_by_source(f"{main_dir}/{skip_dir}", SENTIMENT_ANALYSIS)
        has_similar = has_similar_in_snapshot(to_check, snapped)
        if not has_similar: # Perché qui c'è un not?
            skipping_sources.append(skip_dir)
    print(f"Sources which skipped the given news: {skipping_sources}")
    return skipping_sources

def main_news_getter(dir: str) -> dict:
    with open(dir, "r") as f:
        news = json.load(f)
    n_new = random.randint(0, len(news)-1)
    single_news = news[n_new]
    return single_news




if __name__ == "__main__":
    main()

# Example output:
# Sources which skipped the given news: ['AGI_Politica']
# return: ['AGI_Politica']