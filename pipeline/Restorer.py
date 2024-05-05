#!/usr/bin/env python
#FILE PERICOLOSO - NON USATELO - RICHIEDE TROPPO SPAZIO SU DISCO

import json
import sys
import os

import spacy

# The scraped news base directory
BASE_DIR = f"../../Newscraping/collectedNews/flow"

def main():
    if len(sys.argv) < 2:
        for lang in os.scandir(BASE_DIR):
            if lang.name == 'PT':
                for newspaper in os.scandir(f"{BASE_DIR}/{lang.name}"):
                    for snapshot in os.scandir(f"{BASE_DIR}/{lang.name}/{newspaper.name}"):
                        print(f"I'm going to restore from {lang.name}/{newspaper.name}/{snapshot.name}")
                        restore(f"{BASE_DIR}/{lang.name}/{newspaper.name}/{snapshot.name}", f"{BASE_DIR}/{lang.name}/{newspaper.name}")


def removeKey(dictionary, key):
    result = dict(dictionary)
    del result[key]
    return result

def restore(filename: str, dir: str):
    output = []

    old = filename
    with open(filename, "r", encoding="utf-8") as f:
        snapshot = json.load(f)
    for article in snapshot:
        if "en_title" in article:
            article = removeKey(article, "en_title")
        if "en_content" in article:
            article = removeKey(article, "en_content")
        if "en_subtitle" in article:
            article = removeKey(article, "en_subtitle")
        if "title_NER" in article:
            article = removeKey(article, "title_NER")
        if "subtitle_NER" in article:
            article = removeKey(article, "subtitle_NER")
        if "content_NER" in article:
            article = removeKey(article, "content_NER")
        output.append(article)

    filename = filename.replace(dir, '')
    filename = filename.replace("ner_", "")
    filename = filename.replace("en_", "")
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
