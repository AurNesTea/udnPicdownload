from collections import Counter
import jieba
import pylab as plt
from wordcloud import WordCloud
import numpy as np
import cv2


#載入停用詞
with open('stops.txt','r', encoding='utf-8') as f:
    stops = set(f.read().split('\n'))

#載入文章
with open("wc.txt",'r', encoding='utf-8') as f:
    txt=" ".join(f.read().split("\n"))#變成一整串的文字
txt=txt.replace(" ","").replace("/","").replace("\"","")

#載入結巴中文字典
jieba.set_dictionary('dict.txt')
terms=[t for t in jieba.cut(txt, cut_all=True) if t not in stops]

#print(Counter(terms))
mask =cv2.imdecode(np.fromfile('heart.png',dtype=np.uint8),
                   cv2.IMREAD_UNCHANGED)
wordcloud=WordCloud(font_path='simsun.ttc', background_color="white", mask=mask)
img=wordcloud.generate_from_frequencies(frequencies=Counter(terms))
plt.figure(figsize=(4,4))

#bilinear 雙線性插值法，讓文字不會有鋸齒狀
plt.imshow(img, interpolation="bilinear")
plt.axis("off")
plt.show()