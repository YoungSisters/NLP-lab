from flask import jsonify
from nltk.tokenize import sent_tokenize
import random
import nltk.data
import torch
import docx2txt
import PyPDF2
import os
import warnings
warnings.filterwarnings("ignore")
from flask import Flask, render_template, request, redirect, url_for, abort, \
    send_from_directory
from werkzeug.utils import secure_filename
import PyPDF2

from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from sentence_splitter import SentenceSplitter, split_text_into_sentences

app = Flask(__name__)
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
text=""

a=''
model_name = 'tuner007/pegasus_paraphrase'
torch_device = 'cpu'
tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)


#setting up the model
def get_response(input_text,num_return_sequences,num_beams=10):
  batch = tokenizer([input_text],truncation=True,padding='longest',max_length=60, return_tensors="pt").to(torch_device)
  translated = model.generate(**batch,max_length=60,num_beams=num_beams, num_return_sequences=num_return_sequences, temperature=1.5)
  tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)
  return tgt_text

def paraphrase(text):
    sentence_list = sent_tokenize(text)
    paraphrase = []
    output=""
    for i in sentence_list:
        a = get_response(i,1)
        paraphrase.append(a)
    for i in paraphrase:
        output=output+i[0]+" "
    return output

@app.route('/paraphrasing', methods=['POST'])
def phrase():
    sen = request.get_json()
    print(sen['data'])
    pem = sen['data']
    print (pem)
    text = paraphrase(pem)
    print (text)
    ata = {'name':text}
    return jsonify(ata)

if __name__ == '__main__':
   app.run(host="0.0.0.0", port=5002, debug=True)
