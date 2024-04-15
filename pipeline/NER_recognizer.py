#!/usr/bin/env python

import json
import os
import spacy

my_subdirs = ['edition/DE',
              'edition/FR',
              'edition/EN',
              'flow/DE',
              'flow/EN',
              'flow/IT',
              'flow/PT']

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
        pos_tagger(getting_news(my_subdir), my_subdir)

def pos_tagger(editions, my_subdir, sentiment = 0):
    to_ret = []
    for nat_ed in editions:
        for edition in nat_ed:
            recognized = news_recognizer(edition, nlp, sentiment)
            to_ret.append(recognized)
            if len(edition) > 0:
                prev_prefix_len = len(PREV_PREFIX)
                filepath = f"{BASE_DIR}{my_subdir}/{edition[0]['source']}/{NEXT_PREFIX}{edition[0]['filename'][len(NEXT_PREFIX) + prev_prefix_len:]}"
                old_filepath = f"{BASE_DIR}{my_subdir}/{edition[0]['source']}/{PREV_PREFIX}{edition[0]['filename'][len(NEXT_PREFIX) + prev_prefix_len:]}"
                print(filepath)
                os.remove(old_filepath)
                with open(filepath, "w") as f:
                    json.dump(edition, f, ensure_ascii=False, indent=4)
                    f.write("\n")
    return to_ret

def getting_news(my_subdir):
    directory = f"{BASE_DIR}{my_subdir}"
    nat_ed = []
    for subdir in os.scandir(directory):
        newspaper = subdir.name
        editions = []
        for news in os.scandir(subdir):
            if (news.name[0:len(PREV_PREFIX)] == PREV_PREFIX):
                filepath = f"{directory}/{newspaper}/{news.name}"
                with open(filepath, "r+") as f:
                    curr_news = json.load(f)
                edition = []
                for new in curr_news:
                    new['filename'] = NEXT_PREFIX + news.name
                    edition.append(new)
                editions.append(edition)
        nat_ed.append(editions)
    return nat_ed


def news_recognizer(to_reco, nlp, sentiment=0):
    for article in to_reco:
        if f"{ENGLISH_PREFIX}title" in article:
            article = article_recognizer(article, nlp, sentiment)
    return to_reco


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
