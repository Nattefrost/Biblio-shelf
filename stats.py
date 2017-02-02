#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Nattefrost'


import db_access
from heapq import nlargest
from operator import itemgetter

def generate_authors_top_ten():
    data = db_access.get_popular_authors()
    dic = {}
    top_ten = []
    labels = []
    values = []
    for item in data:
        dic[item[1]] = item[0] 

    for name, nb in nlargest(10, dic.items(), key=itemgetter(1)):
        top_ten.append((name,nb))
        labels.append(name)
        values.append(nb)
        
    #graph = pygal.Bar(show_dots=False, rounded_bars=2, width=500, height=300, margin=10,
     #                   tooltip_border_radius=0,tooltip_font_size=20, print_zeroes=True, range=(0,30),
      #                  legend_font_size=5,y_labels_major=[0])
    #graph.x_labels=labels
    #graph.add("Number of books", values)
    #graph.render_to_file(filename="./stats/authors_top_ten.svg")
    return top_ten

    

