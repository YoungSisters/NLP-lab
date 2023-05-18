#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from nltk import tokenize
from joblib import load
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)
from http import HTTPStatus
from flask import Flask, jsonify, redirect, render_template, request, url_for
import re

app = Flask(__name__)

@app.route('/formality', methods=['POST'])
def formality_check():
    text = request.json['data']
    pipeline_validated = load("/home/ubuntu/NLP-lab/Flask/raw_nb.jbl")
    formality_bool = pipeline_validated.predict(text)
    if formality_bool==0:
        formality = 'Formal'
    else:
        formality = 'Informal'
    return jsonify({'formality': formality})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002)


# In[ ]:





# In[ ]:




