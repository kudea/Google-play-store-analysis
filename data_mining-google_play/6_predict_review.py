import numpy as np
import pandas as pd
import jieba
import json
from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn.metrics import roc_auc_score,confusion_matrix

review_raw=pd.read_csv('Train.csv',encoding='utf-8')
review_1=pd.DataFrame()
review_1["Star"]=review_raw["Star"]


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
for (index, name, date, star, review) in Review:
    seg = jieba.cut(review, cut_all=False)
    remainderWords = list(filter(lambda a: a not in stopWords and a != '\n', seg))
    for word in remainderWords:
        if word in lexicon:
            ind=index-10000
            review_1.ix[ind][word]=1
        #print(word)
    #print("-----------------------")

    #print("-----------------------")

#print(review_1)
review_1.to_csv("xxx.csv",encoding="utf-8")

x=review_1.iloc[:,1:len(review_1.columns)+1]
y = review_1.iloc[:,0]
y=y.replace([1, 2, 3, 4, 5], [0, 0, 0, 1, 1])   #1.2.3星換成0(negative),4.5星換成1(positive)

x_train=[]
x_test=[]
y_train=[]
y_test=[]
kf = KFold(n_splits=10, shuffle=False, random_state=None)

for train_index , test_index in kf.split(x):
    x_train.append(x.iloc[train_index])
    x_test.append(y.iloc[train_index])
    y_train.append(x.iloc[test_index])
    y_test.append(y.iloc[test_index])

accuracy=[]
sensitivity=[]
specificity=[]
AUC=[]
clf = DecisionTreeClassifier(random_state=0)

def Find_Optimal_Cutoff(target, predicted):
    """ Find the optimal probability cutoff point for a classification model related to event rate
    Parameters
    ----------
    target : Matrix with dependent or target data, where rows are observations

    predicted : Matrix with predicted data, where rows are observations

    Returns
    -------
    list type, with optimal cutoff value

    """

    fpr, tpr, threshold = metrics.roc_curve(target, predicted)
    i = np.arange(len(tpr))
    roc = pd.DataFrame({'tf' : pd.Series(tpr-(1-fpr), index=i), 'threshold' : pd.Series(threshold, index=i)})
    roc_t = roc.loc[(roc.tf-0).abs().argsort()[:1]]
    print(roc_t)
    return (roc_t.iloc[0,1])

for i in range(10):

    clf.fit(x_train[i],x_test[i])

    # 根據測試的資料找到Optimal Cuttoff
    probability = clf.predict_proba(y_train[i])[:, 1]
    print(probability)
    opt_cut = Find_Optimal_Cutoff(y_test[i], probability)

    # 依找到的Optimal Cuttoff來預測類別，如果機率大於等於Optimal Cuttoff預測為1
    y_pred = (probability > opt_cut).astype(int)

    tn, fp, fn, tp = confusion_matrix(y_test[i], y_pred).ravel()

    accuracy.append((tp + tn) / (tp + tn + fp + fn))
    sensitivity.append(tp / (tp + fn))
    specificity.append(tn / (tn + fp))
    AUC.append(roc_auc_score(y_test[i], probability))

accuracy = pd.Series(accuracy)
sensitivity = pd.Series(sensitivity)
specificity = pd.Series(specificity)
AUC = pd.Series(AUC)

print(x.shape)
print(round(accuracy.mean(),3),'\t',round(accuracy.std(),3))
print(round(AUC.mean(),3),'\t',round(AUC.std(),3))
print(round(sensitivity.mean(),3),'\t',round(sensitivity.std(),3))
print(round(specificity.mean(),3),'\t',round(specificity.std(),3))

