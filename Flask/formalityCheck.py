#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, request
from http import HTTPStatus
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)

@app.route('/formality', methods=['POST'])
def formality_check():
    data = request.json['data']
    formality = is_formal(data)
    return jsonify({'formality': formality})

def is_formal(sentence):
    if len(sentence.split()) > 10 and re.search(r'\b(?:therefore|moreover|nevertheless)\b', sentence):
        return "Formal"
    else:
        return "Informal"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)


# In[ ]:





# In[ ]:




