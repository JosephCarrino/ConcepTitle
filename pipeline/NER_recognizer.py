#!/usr/bin/env python

import json
import os
import sys

import spacy

my_subdirs = ['edition/DE',
              'edition/FR',
              'edition/EN',
              'flow/DE',
              'flow/EN',
              'flow/IT',
              'flow/PT',
              'flow/FR',
              'flow/ES']

nlp = spacy.load("../en_core_web_sm")

BASE_DIR = "../../Newscraping/collectedNews/"

PREV_PREFIX = 'en_'
NEXT_PREFIX = 'ner_'
ENGLISH_PREFIX = 'en_'
FIELDS_TO_NLP = ['title',
                 'subtitle',
                 'content'
                 ]


def main():
    for my_subdir in my_subdirs:
        for newspaper in os.scandir(BASE_DIR + my_subdir):
            for edition in os.scandir(BASE_DIR + my_subdir + "/" + newspaper.name):
                old_file = BASE_DIR + my_subdir + "/" + newspaper.name + "/" + edition.name
                print(f"NER:{old_file}")
                new_file = BASE_DIR + my_subdir + "/" + newspaper.name + "/" + NEXT_PREFIX + edition.name
                news = getting_news(old_file)
                if len(news) == 0:
                    print(f"Skipped (1):{old_file}")
                    continue
                news = news_recognizer(news, nlp)
                if len(news) == 0:
                    print(f"Skipped (2):{old_file}")
                    continue
                with open(new_file, "w") as f:
                    json.dump(news, f, indent=4, ensure_ascii=False)
                    f.write("\n")
                os.remove(old_file)
                print(f"Completed:{new_file}")


def getting_news(file: str):
    news = []
    with open(file, "r+") as f:
        curr_news = json.load(f)
        for new in curr_news:
            if "title_NER" in new:
                return []
            else:
                news.append(new)
    return news


def news_recognizer(to_reco, nlp, sentiment=0):
    out = []
    for article in to_reco:
        if f"{ENGLISH_PREFIX}title" in article:
            article = article_recognizer(article, nlp, sentiment)
            out.append(article)
        else:
            return []
    return out


def article_recognizer(article, nlp, sentiment=0):
    field_lang = ""

    if article['language'] != 'EN':
        field_lang = ENGLISH_PREFIX

    if sentiment:
        article['overall_polarity'] = 0
        article['overall_subjectivity'] = 0

    for field_to_nlp in FIELDS_TO_NLP:
        article = field_nlpier(article, f"{field_lang}{field_to_nlp}", nlp, sentiment)
        if sentiment:
            try:
                article['overall_polarity'] += article[sent_field_creator(f"{field_lang}{field_to_nlp}", "polarity")]
                article['overall_subjectivity'] += article[
                    sent_field_creator(f"{field_lang}{field_to_nlp}", "subjectivity")]
            except:
                pass
    if sentiment:
        article['overall_polarity'] /= len(FIELDS_TO_NLP)
        article['overall_subjectivity'] /= len(FIELDS_TO_NLP)

    return article


def field_nlpier(article, field, nlp, sentiment=0):
    try:
        nlpied = nlp(article[field])
        if sentiment:
            article[sent_field_creator(field, "polarity")] = nlpied._.blob.polarity
            article[sent_field_creator(field, "subjectivity")] = nlpied._.blob.subjectivity
        if nlpied.ents:
            article[ner_field_creator(field)] = []
            for ent in nlpied.ents:
                ner_object = ner_object_creator(ent)
                # It is possibile to add a control to avoid appending the same entities many times
                article[ner_field_creator(field)].append(ner_object)
    except:
        pass

    return article


def ner_field_creator(field):
    return (f"{field}_NER").replace(ENGLISH_PREFIX, "")


def sent_field_creator(field, type):
    return (f"{field}_{type}").replace(ENGLISH_PREFIX, "")


def ner_object_creator(info):
    to_ret = {}

    to_ret['word'] = info.text
    to_ret['start_char'] = info.start_char
    to_ret['end_char'] = info.end_char
    to_ret['label'] = info.label_
    to_ret['info'] = spacy.explain(info.label_)

    return to_ret


if __name__ == "__main__":
    main()
