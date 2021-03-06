#!/usr/bin/env python

import os
import json
from collections import defaultdict
from yattag import Doc
from yattag import indent

BASE_DIR = f"./compared/"

def main():
    my_subdirs = get_dirs()
    for my_files in my_subdirs:
        for my_file in my_files:
            print(my_file)
            htmlify(my_file)


#a util function which gets all the comparison file names in a given directory of comparison files
def get_paths(subdir):
    to_ret = []
    for my_compare in os.scandir(subdir):
        if my_compare.name[len(my_compare.name)-5:] == ".json":
            to_ret.append(subdir + my_compare.name)
    return to_ret

#a util function which, in my filesystem, gets the path of all comparison subdirs
def get_dirs():
    to_ret= []
    for source_a in os.scandir(BASE_DIR):
        if source_a.name != "date_comparison":
            subdir_a = f"{BASE_DIR}{source_a.name}/"
            for source_b in os.scandir(subdir_a):
                subdir_b = f"{subdir_a}{source_b.name}/"
                to_ret.append(get_paths(subdir_b))
    return to_ret

#a function which, given the path of a json comparing file, visualize its html table of comparison
def htmlify(path):
    print(len(path))
    with open(path, "r+") as f:
        compared = json.load(f)
    to_visual_name = path.split("/")
    to_visual_name = to_visual_name[len(to_visual_name)-1] + ".html"
    simils, simil_concs = get_simils(compared)
    print_table(compared, to_visual_name, simils, simil_concs)

def get_simils(compared):
    compared= compared['simils_concepts']
    simm_list= []
    simm_table= defaultdict(list)
    for similar in compared:
        simm_name= similar['news'][0]['en_title'] + "----" + similar['news'][1]['en_title']
        simm_list.append(simm_name)
        for concept in similar['concepts']['concepts_found']:
            simm_table[simm_name].append(concept['word'])
    return simm_list, simm_table

def print_table(to_visual, to_visual_name, simils, simil_table):
    header_a = []
    header_b = []
    for new in to_visual['edition_a']:
        header_a.append(new)
    for new in to_visual['edition_b']:
        header_b.append(new)
    doc, tag, text = Doc().tagtext()
    doc.asis('<!DOCTYPE html>')
    doc.asis('<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">')
    with tag('html'):
        with tag('body'):
            with tag('table', klass= 'table table-bordered'):
                with tag('thead'):
                    with tag('tr', id= "colhead"):
                        with tag('th', id="head"):
                            text("")
                        for header in header_a:
                            with tag('th', ('scope', 'col'), id="col_"+header['en_title']):
                                text(header['en_title'])
                for header in header_b:
                        with tag('tr', id="rowhead"):
                            with tag('th', ('scope', 'row'), id="row_"+header['en_title']):
                                text(header['en_title'])
                            for header_th in header_a:
                                if header_th['en_title'] + "----" + header['en_title'] in simils:
                                    with tag('td', klass='table-success', id=header_th['en_title']+"----"+header['en_title']):
                                        with tag('div', klass="row"):
                                            with tag('div', klass="col"):
                                                for concept in header_th['concepts']:
                                                    if concept['word'] in simil_table[header_th['en_title'] + "----" + header['en_title']]:
                                                        with tag('span', klass="text-success"):
                                                            text(concept['word'])
                                                            doc.asis('<br>')
                                                    else:                 
                                                        with tag('span', klass="text-danger"):
                                                            text(concept['word'])
                                                            doc.asis('<br>')
                                            doc.asis('<br>')
                                            with tag('div', klass="col"):
                                                for concept in header['concepts']:
                                                    if concept['word'] in simil_table[header_th['en_title'] + "----" + header['en_title']]:
                                                        with tag('span', klass="text-success"):
                                                            text(concept['word'])
                                                            doc.asis('<br>')
                                                    else:
                                                        with tag('span', klass="text-danger"):
                                                            text(concept['word'])
                                                            doc.asis('<br>')
                                else:
                                    with tag('td', klass="table-danger", id=header_th['en_title']+"----"+header['en_title']):
                                        with tag('div', klass="row"):
                                            with tag('div', klass="col"):
                                                for concept in header_th['concepts']:
                                                    with tag('span', klass="text-danger"):
                                                        text(concept['word'])
                                                        doc.asis('<br>')
                                            doc.asis('<br>')
                                            with tag('div', klass="col"):
                                                for concept in header['concepts']:
                                                    with tag('span', klass="text-danger"):
                                                        text(concept['word'])
                                                        doc.asis('<br>')
    
    html_filepath = f"{BASE_DIR}{header_a[0]['source']}/{header_b[0]['source']}/{to_visual_name}"
    with open(html_filepath, 'w') as f:
        f.write(indent(doc.getvalue()))
        f.write("\n")
                                        
                    

if __name__ == "__main__":
    main()