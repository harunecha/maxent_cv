#python3.5
# coding: utf-8

import random
import re
import MeCab
from collections import Counter
import nltk
import numpy
import pandas as pd
import matplotlib as plt
import csv


#業界データ
#company_1.csv 製造業
#company_2.csv 情報
#company_3.csv サービス業
#company_123.csv 製造業・情報・サービス業

#Category
    #company_tag
        #20 上位20%
        #10 上位10%
    #president_tag
        #20 上位20%
        #10 上位10%
#message
    #message_top
    #message_stock

def format_text(text):
    '''
    MeCabに入れる前のテキスト整形
    '''
    text=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
    text=re.sub(r'[!-~]', "", text)#半角記号,数字,英字
    text=re.sub(r'[︰-＠]', "", text)#全角記号
    text=re.sub('\n', " ", text)#改行文字
    text=re.sub(r"(株)", "", text)#(株)
 
    return text



stoplist=['もの','こと','よう','より','の','さ','これ', 'それ','そこ']


#-Mecab/-Ochasen/mecabrc
def mecab_extract(text):
    #mecabで形態素解析・名詞のみ抽出
    mecab = MeCab.Tagger ("Ochasen")
    keywordslist =[]
    result= mecab.parse(text)[:-1]
    wordList = result.split("\n")

    for list in wordList:
        #print(list)
        if list != "EOS": #EOSを無視
            if list != "n/a": #n/aを無視
                word = list.lower().split("\t")
                hinshi = word[1].split(",")
            if word[0] not in stoplist:
                if hinshi[6] !="*":
                    if hinshi[0] == "名詞":
                        if hinshi[2] != "人名":
                            if hinshi[2] != "組織":
                                keywordslist.append(hinshi[6])
                    elif hinshi[0] == "形容詞":
                              keywordslist.append(hinshi[6])
                    elif hinshi[0] == "副詞":
                            keywordslist.append(hinshi[6])
    return keywordslist


# In[142]:

#csvの読み込み・テキスト処理
mes=[]
category = []
documents=[]
positivewords=[]
negativewords=[]
allwordscollected =[]
file =[]
def readcsv(filename, tag, mes):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = next(reader)
        for row in reader:
            if row[tag] =="" or row[mes] =="":
                next
            elif row[tag] =='good'and int(row['votes']) >= 5:
                text=format_text(row[mes])
                if len(text) >=200:
                    documents.append((mecab_extract(text),('good')))
                    for w in mecab_extract(text):
                        if w != format_text(row['companyname']):
                            allwordscollected.append(w)
                            positivewords.append(w)
            elif row[tag] =='bad'and int(row['votes']) >= 5:
                text=format_text(row[mes] )
                if len(text) >=200:
                    documents.append((mecab_extract(text),('bad')))
                    for w in mecab_extract(text):
                        if w != format_text(row['companyname']):
                            allwordscollected.append(w)
                            negativewords.append(w)
    file = filename
    return random.shuffle(documents)
    return random.shuffle(allwordscollected)
   
filename='company_1.csv'
readcsv(filename,'company_tag10', 'message_top')
#print(len(documents))


# In[143]:

fdist_n = nltk.FreqDist(negativewords)
fdist_p = nltk.FreqDist(positivewords)


# In[144]:

#all_words
all_words = nltk.FreqDist(allwordscollected)

#頻出単語を１０００語抽出
word_features=[]
vocab = all_words.most_common()
c = 0
for i in vocab:
    if c < 1000:
        word_features.append(i[0])
    c +=1  
random.shuffle(word_features)



def document_features(document):
    features = {}
    for w in word_features:
         features['contains(%s)' % w] = (w in document) #頻出ワードが、各メッセージに現れているかどうか
    return features


#分類器の訓練とテスト
featuresets = [(document_features(d),c) for (d,c) in documents]
random.shuffle(featuresets)

#cross-validation
def cv_maxent(filename, featuresets, cv):
    random.shuffle(featuresets)
    subset_size = int(len(featuresets) / cv)
    accuracy_ave =0
    print('# %s' % (filename))
    print(len(featuresets))
    for i in range(1, cv+1):
        if i == 1:
            print('1st round')
        elif i == 2:
            print('2nd round')
        elif i == 3:
            print('3rd round')
        else:
            print('%s th round' % (i))
        test_set_for_this_round =featuresets[i*subset_size:][:subset_size]
        train_set_for_this_round =featuresets[:i*subset_size] + featuresets[i*subset_size:][subset_size:]
        print('test_set_for_this_round: %s' % (len(test_set_for_this_round)))
        print('train_set_for_this_round: %s' % (len(train_set_for_this_round)))
        maxent = nltk.MaxentClassifier.train(train_set_for_this_round, max_iter=50)

        accuracy = nltk.classify.accuracy(maxent,test_set_for_this_round)
        print('accuracy for this round: %s' % (accuracy))
        accuracy_ave += accuracy
    print("AVERAGE:")
    print(accuracy_ave/cv)
    print(maxent.show_most_informative_features(500))
cv_maxent(filename,featuresets,10)

