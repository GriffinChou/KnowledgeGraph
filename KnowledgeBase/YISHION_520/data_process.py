# -*- coding:utf-8 -*-
import jieba
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

datas = pd.read_csv("./datas/yishion.csv")
text = datas["评论内容"]
corpus = []
for i in text:
    corpus.append(" ".join(jieba.lcut(i)))

p = WordCloud(font_path="./fronts/msyh.ttc").generate(" ".join(corpus))
p.to_file("表白自己.jpg")