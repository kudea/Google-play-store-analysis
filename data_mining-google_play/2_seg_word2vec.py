import pandas as pd
import numpy as np
from argparse import ArgumentParser
import jieba
from gensim.models import word2vec
import warnings


warnings.filterwarnings("ignore")
parser = ArgumentParser()
parser.add_argument("-c", "--corpus_file", default='Lexicons.csv', dest = "corpus_file", help = "Pass in a .csv file.")

args = parser.parse_args()

stopWords = []
remainderWords=[]

# 處理 Stopwords
stopWords.append(" ")
with open('stopWords.txt', 'r', encoding='UTF-8') as file:
    for data in file.readlines():
        data = data.strip()
        stopWords.append(data)

# 讀入 Reviews
Google = pd.read_csv(args.corpus_file)
Review = np.array(Google)   # [(Index, Name, Date, Star, Review), (Index, Name, Date, Star, Review) ...]
# print(Review)


# 進行中文斷詞,去除stopwords
with open('comment_seg.txt', 'w', encoding='utf-8') as output:
    for (index, name, date, star, review) in Review:
        print("Index: {}".format(review))
        review = review.strip('\n')
        seg = jieba.cut(review, cut_all=False)
        remainderWords = list(filter(lambda a: a not in stopWords and a != '\n', seg))
        for word in remainderWords:
            #print(word)
            output.write(word + ' ')
        output.write('\n')
        # print("-----------------------")


# word2vec
    # set training model
sentences = word2vec.LineSentence("comment_seg.txt")
model = word2vec.Word2Vec(sentences, alpha=0.025, window=5, min_count=3, iter=10, size=300, sg=0, hs=0)
model.save("word2vec.model")