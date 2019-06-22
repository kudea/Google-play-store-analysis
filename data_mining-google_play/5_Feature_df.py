import numpy as np
import pandas as pd
import jieba
import json

review_raw=pd.read_csv('new_test.csv',encoding='utf-8')
review_1=pd.DataFrame()
review_1["Star"]=review_raw["Date"]
print(review_raw)
with open("polarity.json",'r') as load_f:
    lexicon =json.load(load_f)
    #print(lexicon)
for lex in lexicon:
    review_1[lex]=0
    #print(lex)
stopWords = []
remainderWords=[]

# 處理 Stopwords
stopWords.append(" ")
with open('stopWords.txt', 'r', encoding='UTF-8') as file:
    for data in file.readlines():
        data = data.strip()
        stopWords.append(data)

# 讀入 Reviews
Review = np.array(review_raw)   # [(Index, Name, Date, Star, Review), (Index, Name, Date, Star, Review) ...]
#print(Review)

# 進行中文斷詞,去除stopwords
for (index, star, name, date, review) in Review:
    #print(index)
    seg = jieba.cut(review, cut_all=False)
    remainderWords = list(filter(lambda a: a not in stopWords and a != '\n', seg))
    for word in remainderWords:
        if word in lexicon:
            review_1.ix[index,word]= 1
            print(index,"   ",word)
            #print(review_1.ix[index,word])
        #print(word)
    #print("-----------------------")

review_1.to_csv("Feature_Test.csv",encoding="utf-8")


