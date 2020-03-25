from keras.models import load_model
from keras.utils import CustomObjectScope
from keras_contrib.layers import CRF    # pip install git+https://www.github.com/keras-team/keras-contrib.git
from gensim.models import FastText

import numpy as np
import pickle



class Load_Entity:
    root_path = "Travel_Chatbot/"
    entity_model_path = root_path+"model/entity/"
    

    def __init__(self):
        # 개체명인식 모델
        ## 불러오기 Keras+CRF save, load 시 custom_objects 구문 필요
        ## https://keras.io/getting-started/faq/#handling-custom-layers-or-other-custom-objects-in-saved-models

        # Fasttext
        # index number.dictionary
        self.word_index = FastText.load(self.entity_model_path + "fasttext") # FastText 문장 데이터
        with open(self.entity_model_path +'entityIndex.pickle', 'rb') as f:
            self.entity_index = pickle.load(f)

        # Keras Model.h5
        crf = CRF(len(self.entity_index))
        with CustomObjectScope({'CRF': crf, 'crf_loss': crf.loss_function, 'crf_viterbi_accuracy': crf.accuracy}):
            self.entity_model = load_model(self.entity_model_path+"model.h5")
            self.entity_weight = self.entity_model.load_weights(self.entity_model_path+"weight.h5")
        
        print("######################## Success Entity Model load ########################\n\n\n")