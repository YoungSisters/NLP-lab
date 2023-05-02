# -*- coding: utf-8 -*-

import numpy as np
from keras.models import Model
from keras.layers import Input, LSTM, Dense, Embedding

from google.colab import drive
drive.mount('/content/drive')

# 201967 parallel corpus
"""
with open("/content/drive/MyDrive/speaKing/Family_Relationships_informal.txt", "r") as f:
    informal_sentences = f.readlines()
with open("/content/drive/MyDrive/speaKing/Family_Relationships_formal.txt", "r") as f:
    formal_sentences = f.readlines()
"""

with open("/content/drive/MyDrive/speaKing/informal_1549.txt", "r") as f:
    informal_sentences = f.readlines()
with open("/content/drive/MyDrive/speaKing/formal_1549.txt", "r") as f:
    formal_sentences = f.readlines()

input_texts = []
target_texts = []
input_vocab = set()
target_vocab = set()
for i in range(len(informal_sentences)):
    input_text = informal_sentences[i].strip().lower()
    target_text = formal_sentences[i].strip().lower()
    input_texts.append(input_text)
    target_texts.append(target_text)
    for char in input_text:
        if char not in input_vocab:
            input_vocab.add(char)
    for char in target_text:
        if char not in target_vocab:
            target_vocab.add(char)
input_vocab = sorted(list(input_vocab))
target_vocab = sorted(list(target_vocab))
num_encoder_tokens = len(input_vocab)
num_decoder_tokens = len(target_vocab)
max_encoder_seq_length = max([len(txt) for txt in input_texts])
max_decoder_seq_length = max([len(txt) for txt in target_texts])
input_token_index = dict([(char, i) for i, char in enumerate(input_vocab)])
target_token_index = dict([(char, i) for i, char in enumerate(target_vocab)])
encoder_input_data = np.zeros((len(input_texts), max_encoder_seq_length, num_encoder_tokens), dtype="float32")
decoder_input_data = np.zeros((len(target_texts), max_decoder_seq_length, num_decoder_tokens), dtype="float32")
decoder_target_data = np.zeros((len(target_texts), max_decoder_seq_length, num_decoder_tokens), dtype="float32")
for i in range(len(input_texts)):
    for j, char in enumerate(input_texts[i]):
        encoder_input_data[i, j, input_token_index[char]] = 1.0
    for j, char in enumerate(target_texts[i]):
        decoder_input_data[i, j, target_token_index[char]] = 1.0
        if j > 0:
            decoder_target_data[i, j-1, target_token_index[char]] = 1.0

encoder_inputs = Input(shape=(None, num_encoder_tokens))
encoder = LSTM(256, return_state=True)
encoder_outputs, state_h, state_c = encoder(encoder_inputs)
encoder_states = [state_h, state_c]
decoder_inputs = Input(shape=(None, num_decoder_tokens))
decoder_lstm = LSTM(256, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)
decoder_dense = Dense(num_decoder_tokens, activation="softmax")
decoder_outputs = decoder_dense(decoder_outputs)
model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

model.compile(optimizer="rmsprop", loss="categorical_crossentropy")
model.fit([encoder_input_data, decoder_input_data], decoder_target_data, batch_size=64, epochs=10, validation_split=0.2)

model.save("informal_to_formal.h5") #path/to/location

from keras.models import load_model

loaded_model = load_model('informal_to_formal.h5')

from keras.models import load_model
import numpy as np

model = load_model('informal_to_formal.h5')

input_sentence = "The quick brown fox jumps over the lazy dog."

max_words = 10000
max_len = 50

tokenizer = Tokenizer(num_words=max_words)

tokenizer.fit_on_texts([input_sentence])

sequence = tokenizer.texts_to_sequences([input_sentence])[0]

padded_sequence = pad_sequences([sequence], maxlen=max_len)
preprocessed_input_data = padded_sequence

input_data = np.array(preprocessed_input_data)

input_data = np.reshape(input_data, (1, input_data.shape[0], input_data.shape[1]))

predictions = loaded_model.predict(input_data, input_data)
