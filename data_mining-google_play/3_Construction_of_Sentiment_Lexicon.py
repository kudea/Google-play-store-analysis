# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 13:06:20 2019

@author: user
"""

from gensim.models import Word2Vec
import warnings
import synonyms
from langconv import Converter


warnings.filterwarnings("ignore")
model = Word2Vec.load("word2vec.model")

# 繁體轉簡體
def tradition2simple(word):
    return Converter('zh-hans').convert(word)
# 簡體轉繁體
def simple2tradition(word):
    return Converter('zh-hant').convert(word)


def expand_seeds(seeds):
    prior_seeds = []
    while(not (seeds == prior_seeds)): # when each converges and closes to balance
        prior_seeds = seeds[:] # copy list
        similarity = dict()
        # expand seeds
        for seed in seeds:
            top10 = model.most_similar(seed, topn = 20)  # [('term1', similarity1), ('term2', similarity2), ...]
            for term, simi in top10:
                if term in similarity:
                    similarity[term] += simi
                else:
                    similarity[term] = simi
        # sort candidate terms by their similarity to seeds
        sorted_similarity = sorted(similarity.items(), key=lambda x:x[1], reverse=True) 
        for i in range(0, 20):
            term, simi = sorted_similarity[i]
            if term not in seeds:
                seeds.append(term)
        
    
    return(seeds)


pos_seeds = ['好玩', '不錯', '棒', '讚', '喜歡','希望', '玩家', '佛心', '時間', '好好玩', '好棒', '很好', '很棒'] # add the element by manual where comes the higher frequency
neg_seeds = ['爛', '更新', '問題', '卡', '外掛', '不能', '無法', '閃退', '垃圾', '差'] # maybe here comes some mistake or causes some bugs
final_pos_seeds = expand_seeds(pos_seeds)
final_neg_seeds = expand_seeds(neg_seeds)

# 根據synonyms, 再加入與擴增後的seeds同義的詞(10個)
for term in final_pos_seeds:
    print('term:', term)
    synonyms_words = synonyms.nearby(tradition2simple(term)) # ([相似詞1, 相似詞2,...],[相似度1, 相似度2,...])
    # 若找的到同義詞(相似度>0.8)，把簡體字轉回繁體再加入到final_pos_seeds
    index=0
    if synonyms_words[0]:
        for i in range(0,10):
            if synonyms_words[1][i] > 0.79:
                word = simple2tradition(synonyms_words[0][i])
                if word not in final_pos_seeds:
                    final_pos_seeds.append(word)
                    print(word, 'has been added to final_pos_seeds')
    
for term in final_neg_seeds:
    print('term:', term)
    synonyms_words = synonyms.nearby(tradition2simple(term)) # ([相似詞1, 相似詞2,...],[相似度1, 相似度2,...])
    # 若找的到同義詞(相似度>0.8)，把簡體字轉回繁體再加入到final_pos_seeds
    if synonyms_words[0]:
        for i in range(0,10):
            if synonyms_words[1][i] > 0.79:
                word = simple2tradition(synonyms_words[0][i])
                if word not in final_neg_seeds:
                    final_neg_seeds.append(word)
                    print(word, 'has been added to final_neg_seeds')
    
    
# output to .txt
with open('pos_seeds.txt', 'w', encoding='utf-8') as f:
    for i in final_pos_seeds:
        f.write(i+'\n')
        
       
with open('neg_seeds.txt', 'w', encoding='utf-8') as f:
    for i in final_neg_seeds:
        f.write(i+'\n')

