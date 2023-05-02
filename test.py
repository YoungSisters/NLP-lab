#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, jsonify, request
from flask_restx import Resource, Api, reqparse
import sklearn
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

app = Flask(__name__)
api = Api(app)
app.config['Debug'] = True

@app.route('/check')
def index():
    return 'bp'

@app.route('/test')
class testAPI(Resource):
    def get(self):
        return jsonify({"result": "connection from flask"})
    
    def post(self):
        iris = load_iris()
        parsed_request = request.json.get('content')
        result = iris.feature_names
        print(parsed_request)
        return result
    
if __name__ == '__main__':
    app.run(debug=True)

