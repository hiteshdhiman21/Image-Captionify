# -*- coding: utf-8 -*-
"""Caption_it.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TMtDkg3xS2zZhByDucNFeAsKOT9xIMv0
"""

#importing modules and libraries
import pandas as pd
import numpy as np
import re
import json
from time import time
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from keras.models import Model, load_model
from tensorflow.keras.preprocessing import image
from keras.layers import add
from keras.layers import Input, Dense, Dropout, Embedding, LSTM
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences

import pickle

model = load_model("C:\\Caption-it\\Model\\model_9.h5")

model_temp = ResNet50(weights = "imagenet", input_shape = (224, 224, 3))

model_resnet = Model(model_temp.input, model_temp.layers[-2].output)

def preprocess_img(img):
  img = image.load_img(img, target_size = (224, 224))
  img = image.img_to_array(img)
  img = np.expand_dims(img, axis = 0)
  img = preprocess_input(img)
  return img

def encode_img(img):
  img = preprocess_img(img)
  feature_vector = model_resnet.predict(img)
  feature_vector = feature_vector.reshape((1, -1))
  return feature_vector

with open("C:\\Caption-it\\Model\\word_to_idx.pkl", "rb") as w2i:
  word_to_idx = pickle.load(w2i)

with open("C:\\Caption-it\\Model\\idx_to_word.pkl", "rb") as i2w:
  idx_to_word = pickle.load(i2w)

idx_to_word[4]

word_to_idx["is"]

def predict_caption(photo):
    max_len = 35
    in_text = "<s>"
    for i in range(max_len):
        sequence = [word_to_idx[w] for w in in_text.split() if w in word_to_idx]
        sequence = pad_sequences([sequence],maxlen=max_len,padding='post')

        ypred = model.predict([photo,sequence])
        ypred = ypred.argmax() #WOrd with max prob always - Greedy Sampling
        word = idx_to_word[ypred]
        in_text += (' ' + word)

        if word == "<e>":
            break

    final_caption = in_text.split()[1:-1]
    final_caption = ' '.join(final_caption)
    return final_caption

#predict_caption(enc)

def caption_this_image(img):
  enc = encode_img(img)
  caption = predict_caption(enc)
  return caption

#caption_this_image(IMG_PATH+"1110208841_5bb6806afe"+".jpg")
