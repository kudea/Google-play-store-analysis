# Social-media-mining
Data mining from google play's comments

## Introduction
For the experimental data, we not only increase the number of it to 30000 in hope of higher precision 
but also choose comments only from games.As for the classifier, I use Decision Tree and Random Forest 
and they are all tree-like models, which is much better to compare. 
According to the result, Random Forest gets higher precision.
## Flow
![image](https://github.com/kudea/Google-play-store-analysis/blob/master/data_mining-google_play/Flow/Diagram.png)
## Methods
### A. Web crawler:
a. Find html tag
b. Realize the relationship between these tags
c. Construct the architecture of the dataset
d. Exclude the ads’ interference
e. Predata work(To make the data be used easily)

### B. Word2vec:
a. Skip-gram
b. Hierarchical Softmax

### C. “Area” method:
a. Uesd to predict polarity of sentiment words
b. According to the frequency of sentiment words in positive and negative
comments
c. When the frequency of the sentiment word in positive comments is greater
than in negative ones, the word is considered positive, if not, the word is
negative

### D. Classifier:
a. Decision Tree
b. Random Forest

### E. K-fold Cross Validation
we use 10-fold cross validation to validate our training data


### F. Optimal cutoff
Cutoff is a threshold value for classifier to classify. Where scores above this value
will classified as positive, those below as negative. (We’ll be using the term cutoff
throughout the rest of the documentation.) The default cutoff value is 0.5, but
we use optimal cutoff to find the best threshold value for the classifier.
 
### G. Feature Selection Algorithm
Process selecting a subset of relevant features(Variables,Predictors) for use in
model construction. 

## Dataset
Users’ comments of Google play TOP 10 grossing games
Garena 急速領域、天堂Ｍ、萬國覺醒、不休的烏拉拉、神魔之塔、叫我官老
爺、老子有錢(麻將)、Garena 傳說對決、新三國志手遊、 失落的龍絆

## Preprocessing
### Dataset collecting:
Web crawler (details in Methods part)
### Construction of Sentiment Lexicon Using word2vec
After tokenizing using Jieba, transform words to vectors
Manually add some most-frequent words in corpus to seeds
Calculate the cosine values between all words and sentiment seeds, and choose the top 20 to join sentiment seeds.
If the seeds get balanced, then the sentiment lexicon is completed; otherwise, jump to iii.
### Predicting the Polarity of Sentiment Words
“Area” method (details in Methods part)
### Classifier using
Decision Tree & Random Forest (details in Methods part)

# Result
<img width="479" alt="1" src="https://user-images.githubusercontent.com/51981236/59960508-d6071000-94fb-11e9-8182-a5b1e51125a9.PNG">
<img width="499" alt="2" src="https://user-images.githubusercontent.com/51981236/59960509-d99a9700-94fb-11e9-8e6e-e6a4fdb3e90f.PNG">

