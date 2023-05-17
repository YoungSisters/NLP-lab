#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, request
from flask import Flask, jsonify, redirect, render_template, request, url_for

import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from collections import Counter
from nltk.corpus import stopwords

app = Flask(__name__)

@app.route('/frequency', methods=['POST'])
def process_data():
    data = request.json['data']
    frequency = word_frequency(data)
    return jsonify(frequency)

def word_frequency(data): 
    data_low = data.lower()
    text = data_low.split()
    
    #불용어
    stop_word_eng = ['i', 'it','me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'You', 'your', 'Your', 'yours', 'yourself', 'yourselves', 'he', 'He', 'him', 'his', 'himself', 'she', 'She', 'her', 'hers', 'herself', 'it', 'Its', 'its', 'itself', 'they', 'They','them', 'their', 'theirs', 'themselves', 'what', 'What', 'which', 'who', 'Who', 'whom', 'this', 'This', 'That', 'that', 'these', 'those', 'am', 'is','Is', 'are', 'Are', 'Was', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

    # 표제어 추출
    lemmatizer = WordNetLemmatizer()
    token = RegexpTokenizer('[\w]+')
    result_pre_lem = [token.tokenize(i) for i in text]
    middle_pre_lem= [r for i in result_pre_lem for r in i]
    final_lem = [lemmatizer.lemmatize(i) for i in middle_pre_lem if not i in stop_word_eng]
    
    # 5개 단어
    c = Counter(final_lem)
    result= c.most_common(5)
    
    top5_dic = [
        {
            'word': result[0][0],
            'count': result[0][1]     
        },
        {
            'word': result[1][0],
            'count': result[1][1]     
        },
        {
            'word': result[2][0],
            'count': result[2][1]     
        },
        {
            'word': result[3][0],
            'count': result[3][1]     
        },
        {
            'word': result[4][0],
            'count': result[4][1]     
        }
    ]
    
    return top5_dic
    
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)


