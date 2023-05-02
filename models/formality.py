#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, render_template, json, jsonify, request
from MySQLdb import _mysql

def is_formal(sentence):
    if len(sentence.split()) > 10 and re.search(r'\b(?:therefore|moreover|nevertheless)\b', sentence):
        return True
    else:
        return False

con = _mysql.connect("localhost", "test", "test", "test")

app = Flask(__name__)
api = Api(app)
app.config['Debug'] = True

@app.route('/formalitycheck', methods['POST'])
def formality():
    if request.method == 'POST':
        text = request.json['speakingId']
        
        if is_formal(text):
            return "Formal"
        else:
            return "Informal"
        
        """
        cur = mysql.connection.cursor() 
        cur.execute("INSERT INTO speakingId(formality) VALUES(%s)", [formality])
        mysql.connection.commit()
        cur.close()
        """
    
if __name__ == '__main__':
    app.run()


# In[ ]:




