#!/usr/bin/env python
#FILE PERICOLOSO - NON USATELO - RICHIEDE TROPPO SPAZIO SU DISCO
exit()

import json
import sys
import os

import spacy

# The scraped news base directory
BASE_DIR = f"../../Newscraping/collectedNews/flow"

PREV_PREFIX = 'nlp_'
NEXT_PREFIX = 'ner_'

def main():
    if len(sys.argv) < 2:
        for lang in os.scandir(BASE_DIR):
            for newspaper in os.scandir(f"{BASE_DIR}/{lang.name}"):
                for snapshot in os.scandir(f"{BASE_DIR}/{lang.name}/{newspaper.name}"):
                    print(f"I'm going to remove NLP from {lang.name}/{newspaper.name}/{snapshot.name}")
                    del_nlp(f"{BASE_DIR}/{lang.name}/{newspaper.name}/{snapshot.name}", f"{BASE_DIR}/{lang.name}/{newspaper.name}")


def removeKey(dictionary, key):
    result = dict(dictionary)
    del result[key]
    return result

def del_nlp(filename: str, dir: str):
    output = []

    old = filename
    with open(filename, "r", encoding="utf-8") as f:
        snapshot = json.load(f)
    for article in snapshot:
        # cont_nlp
        # title_nlp
        # subtitle_nlp
        if "cont_nlp" in article:
            article = removeKey(article, "cont_nlp")
        if "title_nlp" in article:
            article = removeKey(article, "title_nlp")
        if "subtitle_nlp" in article:
            article = removeKey(article, "subtitle_nlp")
        output.append(article)

    filename = filename.replace(dir, '')
    filename = filename.replace(PREV_PREFIX, NEXT_PREFIX)
    new_file = f"{dir}{filename}"

    with open(new_file, "w") as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    os.remove(old)
    print(f"Done {new_file}")


if __name__ == "__main__":
    main()


#nlp(article['en_subtitle']).to_json()
# json.dump(nlp(article['en_subtitle']).to_json())

# nlp.make_doc()


# deserialized_doc = Doc(nlp.vocab).from_json(doc_json)
