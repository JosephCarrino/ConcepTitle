#!/usr/bin/env python

import json
from argostranslate import package, translate
import sys
import os
import errno

# The scraped news base directory
BASE_DIR = f"../../Newscraping/collectedNews/flow"

# The translators indexes based on the source language
LANG_TO_TRANS = {'FR': 0,
                 'DE': 1,
                 'IT': 2,
                 'ES': 3,
                 'en': 0,
                 'EN': 0,
                 'pt': 4,
                 'PT': 4}


def main():
    if len(sys.argv) < 2:
        for lang in os.scandir(BASE_DIR):
            for newspaper in os.scandir(f"{BASE_DIR}/{lang.name}"):
                for snapshot in os.scandir(f"{BASE_DIR}/{lang.name}/{newspaper.name}"):
                    print(f"I'm going to translate {lang.name}/{newspaper.name}/{snapshot.name}")
                    full_translator(f"{lang.name}/{newspaper.name}/{snapshot.name}")
    else:
        full_translator(sys.argv[1])


def full_translator(subdir):
    translators = translators_setup()
    to_translate = news_getter(subdir)
    translated = news_translator(to_translate, translators)
    jsonizer(translated, subdir)


# Starting from the 1-st because of the 0-index english translator
def translators_setup():
    translators = [{}, {}, {}, {}]
    installed_languages = translate.get_installed_languages()
    for i in range(1, 5):
        translators[i - 1] = installed_languages[i].get_translation(installed_languages[0])
    return translators


def news_getter(subdir):
    to_get_dir = f"{BASE_DIR}/{subdir}"
    to_get = {}
    with open(to_get_dir, "r") as f:
        try:
            to_get = json.load(f)
        except:
            raise Exception("Could not read file from the given directory: " + to_get_dir + ".")
    return to_get


def news_translator(to_trans, translators):
    for article in to_trans:
        if article['title'] != None:
            try:
                article = article_translator(article, translators[LANG_TO_TRANS[article['language']]])
            except:
                article = article_translator(article, translators[LANG_TO_TRANS["EN"]], True)
    return to_trans


def article_translator(article, translator, isEn=False):

    if "en_title" in article:
        article['already_done'] = True #Skippa la traduzione
        return article

    if not isEn and article['language'] != "EN" and article['language'] != "en":
        article['en_title'] = translator.translate(article['title'])
        print(article['title'] + "   " + article['en_title'])

        try:
            article['en_content'] = translator.translate(article['content'])
        except:
            raise Exception("Could not translate content of an article.")

        try:
            article['en_subtitle'] = translator.translate(article['subtitle'])
        except:
            pass
    else:
        article['en_title'] = article['title']

        article['en_content'] = article['content']

        try:
            article['en_subtitle'] = article['subtitle']
        except:
            pass

    return article


def jsonizer(translated, subdir):
    output_file = f"{BASE_DIR}/{subdir}"
    old_file = f"{BASE_DIR}/{subdir}"
    output_file = output_file.split('/')
    output_file[-1] = 'en_' + output_file[-1]
    output_file = '/'.join(output_file)
    to_save = []
    for news in translated:
        if "already_done" not in news:
            to_save.append(news)

    if len(to_save) != 0:
        with open(output_file, "w") as f:
            json.dump(to_save, f, indent=4, ensure_ascii=False)
            f.write("\n")
        os.remove(old_file)
        print(f"File translated:{old_file}")

if __name__ == "__main__":
    main()
