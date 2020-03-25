import numpy as np
import pickle
import os
import re

from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, TimeDistributed, Bidirectional, Input, BatchNormalization
from keras.layers import Conv2D, MaxPooling2D, Reshape, Conv1D, MaxPool1D
from keras_contrib.layers import CRF
from keras.utils.np_utils import to_categorical

from gensim.models import FastText

from word_indexing import word_pred, entity_pred, input_size, vector_size


from configs import Configs


# CONFIG
config = Configs()
path = config.entity_model_path
folder = 'test1/'

traindataset_path = 'data\통합_1031(4).csv'   # 훈련데이터
# traindataset_path = 'data\테스트_1101.csv'   # 테스트

# → 훈련 데이터 불러오기
def train_data_load(path):
    sentenceList, entityList = [], []
    with open(path, 'r') as f:
        while True:
            line = f.readline()
            if not line: return sentenceList, entityList
            # 읽을 데이터가 없을 경우, 문장과 개체명 리스트 반환

            line = re.sub('\n', '', line)
            line = line.split('|') # 문장과 개채명 분리

            # 문장
            sentence = line[0]
            sentence = sentence.split(',')
            sentenceList.append(sentence)

            # 개체명
            entity = line[1]
            entity = entity.split(',')
            entityList.append(entity)

#────────────────────────────────────────────────────────────────────
sentenceList, entityList = train_data_load(traindataset_path) # 훈련 데이터

print('start', len(sentenceList), path + folder)
if not os.path.exists(path + folder): os.makedirs(path + folder) # 풀더 생성
#────────────────────────────────────────────────────────────────────

# → 워드 임베딩
print("\n### Fasttext bulid model ###", end="\n")
w2vModel = FastText(size = vector_size, window= 3, workers= 8, min_count = 1)
w2vModel.build_vocab(sentenceList)
print('\n### Fasttext build complete ###', end="\n")

print('\n### Fasttext trian start ###', end="\n")
w2vModel.train( sentenceList, total_examples= w2vModel.corpus_count, epochs= w2vModel.epochs, compute_loss = True, verbose = 1)
print('\n### Fasttext train complete ###', end="\n")


w2vModel.save(path + folder + 'fasttext') # 저장
print('\n### Fasttext model save ###', end="\n")

# w2vModel = FastText.load('model/entity/통합_1031/fasttext')

# → fasttext가 적응된 단어 목록들
w2vIndex = w2vModel.wv.index2word
print('＊단어의 개수:', len(w2vIndex))
#────────────────────────────────────────────────────────────────────

# → 개체명 인덱스 부여
entity_set = sum(entityList, []) # 배열의 차원 펼치기
entity_set = list(set(entity_set)) # 중복 제거

# → 개채명 인덱스 번호
entityIndex = {'#': 0}
for idx in range(len(entity_set)):
    entityIndex[entity_set[idx]] = idx + 1

# 저장
with open(path + folder +'/entityIndex.pickle', 'wb') as f:
    pickle.dump(entityIndex, f, pickle.HIGHEST_PROTOCOL)
print('＊개체명 :',entityIndex)
#────────────────────────────────────────────────────────────────────
print('훈련 데이터 생성')
# → x, y 훈련 데이터 생성
x_data = []
for item in sentenceList:
    item = word_pred(item, w2vModel.wv)
    x_data.append(item)
print('x 생성')
x_data = np.array(x_data)
x_data = x_data.reshape(len(sentenceList), input_size, vector_size)
print('＊X 데이터 :', x_data.shape)

y_data = []
for item in entityList:
    item = entity_pred(item, entityIndex)
    y_data.append(item)
print('y 생성')
y_data = to_categorical(y_data)
print('＊Y 데이터 :', y_data.shape)

#────────────────────────────────────────────────────────────────────

# → Keras Model
crf = CRF(len(entityIndex))

network = Sequential()
#Bi-LSTM Layer
network.add(Bidirectional(LSTM(600, return_sequences = True, recurrent_dropout = 0.2), input_shape = (input_size, vector_size)))
network.add(Reshape((input_size, 20, 60)))

#Fully Connected Layer
network.add(Conv2D(120, kernel_size=(2,2), strides=(1,1), padding="valid", activation="relu"))
network.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
network.add(Conv2D(120, kernel_size=(3,3), strides=(1,1), padding="valid", activation="relu"))
network.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
network.add(Conv2D(120, kernel_size=(4,4), strides=(1,1), padding="valid", activation="relu"))
network.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
network.add(Conv2D(120, kernel_size=(2,2), strides=(1,1), padding="valid", activation="relu"))
network.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
network.add(Conv2D(120, kernel_size=(3,3), strides=(1,1), padding="valid", activation="relu"))
network.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
network.add(Conv2D(120, kernel_size=(4,4), strides=(1,1), padding="valid", activation="relu"))
network.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
network.add(Conv2D(120, kernel_size=(3,3), strides=(1,1), padding="valid", activation="relu"))
network.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))

network.add(TimeDistributed(Dense(100, activation="relu")))
network.summary()

# Dropout Layer
network.add(BatchNormalization())
network.add(Reshape((input_size, 180))) # input_size = 20

# CRF Model
network.add(TimeDistributed(Dense(100, activation="relu")))
network.add(crf)

network.summary()

network.compile(optimizer="rmsprop", loss=crf.loss_function, metrics=[crf.accuracy])
network.fit(x_data, y_data, batch_size=10, epochs=30)

#  → 훈련 모델 저장
network.save(path + folder + 'model.h5')
network.save_weights(path + folder + 'weight.h5')
print('＊케라스 모델 저장', path + folder)


'''
_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
bidirectional_1 (Bidirection (None, 20, 1200)          4324800
_________________________________________________________________
reshape_1 (Reshape)          (None, 20, 20, 60)        0
_________________________________________________________________
conv2d_1 (Conv2D)            (None, 19, 19, 120)       28920
_________________________________________________________________
max_pooling2d_1 (MaxPooling2 (None, 19, 19, 120)       0
_________________________________________________________________
conv2d_2 (Conv2D)            (None, 17, 17, 120)       129720
_________________________________________________________________
max_pooling2d_2 (MaxPooling2 (None, 17, 17, 120)       0
_________________________________________________________________
conv2d_3 (Conv2D)            (None, 14, 14, 120)       230520
_________________________________________________________________
max_pooling2d_3 (MaxPooling2 (None, 14, 14, 120)       0
_________________________________________________________________
conv2d_4 (Conv2D)            (None, 13, 13, 120)       57720
_________________________________________________________________
max_pooling2d_4 (MaxPooling2 (None, 13, 13, 120)       0
_________________________________________________________________
conv2d_5 (Conv2D)            (None, 11, 11, 120)       129720
_________________________________________________________________
max_pooling2d_5 (MaxPooling2 (None, 11, 11, 120)       0
_________________________________________________________________
conv2d_6 (Conv2D)            (None, 8, 8, 120)         230520
_________________________________________________________________
max_pooling2d_6 (MaxPooling2 (None, 8, 8, 120)         0
_________________________________________________________________
conv2d_7 (Conv2D)            (None, 6, 6, 120)         129720
_________________________________________________________________
max_pooling2d_7 (MaxPooling2 (None, 6, 6, 120)         0
_________________________________________________________________
time_distributed_1 (TimeDist (None, 6, 6, 100)         12100
_________________________________________________________________
batch_normalization_1 (Batch (None, 6, 6, 100)         400
_________________________________________________________________
reshape_2 (Reshape)          (None, 20, 180)           0
_________________________________________________________________
time_distributed_2 (TimeDist (None, 20, 100)           18100
_________________________________________________________________
crf_1 (CRF)                  (None, 20, 11)            1254
=================================================================
Total params: 5,293,494
Trainable params: 5,293,294
Non-trainable params: 200
'''