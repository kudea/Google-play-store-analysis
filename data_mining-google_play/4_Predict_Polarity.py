# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 14:52:30 2019

@author: user
"""

import pandas as pd
import numpy as np
from argparse import ArgumentParser
import json

parser = ArgumentParser()
parser.add_argument("-c", "--corpus_file", default='Lexicons.csv', dest = "corpus_file", help = "Pass in a .csv file.")

args = parser.parse_args()
corpus = np.array(pd.read_csv(args.corpus_file)) # [(Index, Name, Date, Star, Review), (Index, Name, Date, Star, Review) ...]


polarity = dict()
def predict_polarity(seeds):
    for term in seeds:
        # print('term:', term)
        # term in 4-star or 5-star comments -> count+=1, others -> count-=1
        # In the end, if count>0 -> positive, others -> negative
        count=0                 
        for (index, name, date, star, review) in corpus:
            if term in review:
                # print('index:', index)
                # print('star:', int(star))
                if int(star) >= 4:
                    count += 1
                else:
                    count -= 1           
        
        if count>0:
            polarity[term] = 'positive'
        elif count<0:
            polarity[term] = 'negative'
        


# get positive and negative seeds
pos_seeds = []
neg_seeds = []
with open('pos_seeds.txt', 'r', encoding='utf-8') as f:
    for i in f.readlines():
        i = i.strip()
        pos_seeds.append(i)
        
with open('neg_seeds.txt', 'r', encoding='utf-8') as f:
    for i in f.readlines():
        i = i.strip()
        neg_seeds.append(i)
    

        
predict_polarity(pos_seeds)
predict_polarity(neg_seeds)
# print(polarity)
json_str = json.dumps(polarity, ensure_ascii=False, indent=4)
with open('polarity.json', 'w', encoding='utf-8') as output:
    output.write(json_str)
