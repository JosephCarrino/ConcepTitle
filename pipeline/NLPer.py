#!/usr/bin/env python

import json
import sys
import os

import spacy

# The scraped news base directory
BASE_DIR = f"../../Newscraping/collectedNews/flow"

PREV_PREFIX = 'ner_'
NEXT_PREFIX = 'nlp_'

nlp = spacy.load("../en_core_web_sm")

def main():
    if len(sys.argv) < 2:
        for lang in os.scandir(BASE_DIR):
            for newspaper in os.scandir(f"{BASE_DIR}/{lang.name}"):
                for snapshot in os.scandir(f"{BASE_DIR}/{lang.name}/{newspaper.name}"):
                    print(f"I'm going to make NLP {lang.name}/{newspaper.name}/{snapshot.name}")
                    make_nlp(f"{BASE_DIR}/{lang.name}/{newspaper.name}/{snapshot.name}", f"{BASE_DIR}/{lang.name}/{newspaper.name}")
                    print(f"Made NLP of {lang.name}/{newspaper.name}/{snapshot.name}")


def make_nlp(filename: str, dir: str):
    snapshot = []
    output = []

    old = filename
    with open(filename, "r", encoding="utf-8") as f:
        snapshot = json.load(f)
    for article in snapshot:
        if "cont_nlp" in article or "en_title" not in article or "title_NER" not in article:
            return output
        if "en_content" not in article or article["en_content"] is None:
            article['en_content'] = ""
        article['cont_nlp'] = nlp(article['en_content']).to_json()
        if "en_title" not in article or article["en_title"] is None:
            article['en_title'] = ""
        article['title_nlp'] = nlp(article['en_title']).to_json()
        if "en_subtitle" not in article or article["en_subtitle"] is None:
            article['en_subtitle'] = ""
        article['subtitle_nlp'] = nlp(article['en_subtitle']).to_json()
        output.append(article)

    filename = filename.replace(dir, '')
    filename = filename.replace(PREV_PREFIX, NEXT_PREFIX)
    new_file = f"{dir}{filename}"

    with open(new_file, "w") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    os.remove(old)
    exit()


if __name__ == "__main__":
    main()


#nlp(article['en_subtitle']).to_json()
# json.dump(nlp(article['en_subtitle']).to_json())

# nlp.make_doc()


# deserialized_doc = Doc(nlp.vocab).from_json(doc_json)
