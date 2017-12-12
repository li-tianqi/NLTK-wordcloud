#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 16:42:03 2017

@author: victor
"""
#import chardet
import re
import nltk
#from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
import operator
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np



def read_text(file):
    with open(file, "r", encoding='ISO-8859-1') as f:
        return f.read()
    
def get_pos(tag):
    if tag.startswith('J'):
        return 'a'
    elif tag.startswith('V'):
        return 'v'
    elif tag.startswith('N'):
        return 'n'
    elif tag.startswith('R'):
        return 'r'
    else:
        return 'n'
    
        

def word_cloud(text, image):
    #text = read_text('THE LITTLE PRINCE.txt')
    text = read_text(text)
    
    patten = re.compile("\W")
    text_W = patten.sub(' ', text)
    text_low = text_W.strip().lower()
    
    raw_word_list = text_low.split()
    
    tag = nltk.pos_tag(raw_word_list)
    
    lmtzr = WordNetLemmatizer()
    
    word_list = [lmtzr.lemmatize(i[0], get_pos(i[1])) for i in tag]        

    with open('stopwords.txt', 'r') as fr:
        stopwords = fr.read()
    
    stopwords = patten.sub(' ', stopwords).strip().split()
    
    new_word_list = [w for w in word_list if w not in stopwords]

    #text_list = text[:100].split()
    
    word_count = {}
    for w in new_word_list:
        word_count[w] = word_count.get(w, 0) + 1

    sortde_word_count = sorted(word_count.items(), 
                               key=operator.itemgetter(1), 
                               reverse=True)
    img = np.asarray(Image.open(image))

    color = ImageColorGenerator(img)
    
    wc = WordCloud(background_color=None, 
                   mask=img, 
                   max_words=100, 
                   max_font_size=80,
                   random_state=None, 
                   color_func=color)
    
    
    
    wc.generate_from_frequencies(word_count)
    #.recolor(color)
    plt.axis("off")
    plt.imshow(wc)
    
if __name__ == "__main__":    
    text = 'The Little prince.txt'
    image = '03.png'
    word_cloud(text, image)