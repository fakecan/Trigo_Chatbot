import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
import pickle

from gensim.models import FastText
from konlpy.tag import Okt

# from tokenizer import tokenize
from preprocess import preprocess_data


from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, LSTM, BatchNormalization, Dropout, Conv2D, MaxPooling2D, Flatten
from keras.callbacks import EarlyStopping

from configs import Configs



def main():
    # global encode_length, vector_size

    ## 1. intent 데이터셋 불러오기
    config = Configs()
    okt = Okt()

    question = preprocess_data(True)
    joinStr = ' '.join(question)

    morphs = okt.morphs(joinStr)
    joinString = ' '.join(morphs)
    pos1 = okt.pos(joinString)
    pos2 = ' '.join(list(map(lambda x: '\n' if x[1] in ['Punctuation'] else x[0], pos1))).split('\n')
    morphs = list(map(lambda x: okt.morphs(x), pos2))


    ## 2. 워드 임베딩
    print("\n### Fasttext bulid model ###", end="\n")
    word2vec_model = FastText(size=config.vector_size, window=3, workers=8, min_count= 1)
    # word2vec_model = FastText(size=config.vector_size, window=2, workers=8, min_count= 1)
    word2vec_model.build_vocab(morphs)
    print('\n### Fasttext build complete ###', end="\n")

    print('\n### Fasttext trian start ###', end="\n")
    word2vec_model.train(morphs, total_examples= word2vec_model.corpus_count, epochs= word2vec_model.epochs, compute_loss=True, verbose=1)
    print('\n### Fasttext train complete ###', end="\n")

    word2vec_model.save(config.fasttext_model_path+"intent_fasttextmodel")
    print('\n### Fasttext model save ###', end="\n")
    
    w2c_index = word2vec_model.wv.index2word # fasttext가 적용된 단어 목록들
    print("[DEBUG1-1]############ FastText representation ############", end="\n\n")
    print(w2c_index, end="\n\n\n")
    print('\n\n[DEBUG1-1]word_index 단어 개수 >> ', len(w2c_index)) # <class 'list'>

    ### intentIndex 저장
    with open(config.fasttext_model_path+'/intentIndex.pickle', 'wb') as f:
        pickle.dump(w2c_index, f, pickle.HIGHEST_PROTOCOL)

    print("_________________________________________________________________________________________________________________\n")



    # # y_data 생성
    y_data = config.df['intent']
    y_data = y_data.map(config.intent_mapping)
    y_data = to_categorical(y_data)

    
    # x_data 생성
    # encode_length = 15
    x_data = []
    for q_raw in question:
        q_raw = okt.morphs(q_raw) # 문장 형태소별로 분리(단어 분리). str > list
        q_raw = list(map(lambda x: q_raw[x] if x < len(q_raw) else '#', range(config.encode_length)))
        q_raw = list(map(lambda x: word2vec_model[x] if x in w2c_index else np.zeros(config.vector_size, dtype=float), q_raw))
        q_raw = np.array(q_raw)
        x_data.append(q_raw)
        
    x_data = np.array(x_data)   # (None, 15, 300)
    x_data = x_data.reshape(len(config.df), config.encode_length, config.vector_size, 1)
    print(x_data.shape)

    ## vector numpy array save
    # np.save("fasttext_vector.npy", x_data)
    print("_________________________________________________________________________________________________________________\n")



    ## 3. 모델 생성 및 훈련
    print("shape >>", x_data.shape, y_data.shape)   # (None, 15 ,300, 1) / (None, 5)

    model = Sequential()
    model.add(Conv2D(12, kernel_size=(2,2), input_shape=(config.encode_length, config.vector_size, 1), strides=(1,1), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
    model.add(Conv2D(12, kernel_size=(3,3), strides=(1,1), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
    model.add(Conv2D(12, kernel_size=(4,4), strides=(1,1), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
    
    model.add(Conv2D(12, kernel_size=(2,2), strides=(1,1), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
    model.add(Conv2D(12, kernel_size=(3,3), strides=(1,1), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
    model.add(Conv2D(12, kernel_size=(4,4), strides=(1,1), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))

    model.add(Conv2D(12, kernel_size=(2,2), strides=(1,1), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
    model.add(Conv2D(12, kernel_size=(3,3), strides=(1,1), padding="valid", activation="relu", data_format='channels_first'))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
    model.add(Conv2D(12, kernel_size=(4,4), strides=(1,1), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))

    model.add(Conv2D(12, kernel_size=(2,2), strides=(1,1), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
    model.add(Conv2D(12, kernel_size=(3,3), strides=(1,1), padding="valid", activation="relu", data_format='channels_first'))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))
    model.add(Conv2D(12, kernel_size=(4,4), strides=(1,1), padding="valid", activation="relu"))
    model.add(MaxPooling2D(pool_size=(1,1), strides=(1,1)))

    model.add(Flatten())
    model.add(BatchNormalization())
    # model.add(Dropout(1.0))
    model.add(Dense(128, activation="relu"))
    # model.add(Dropout(0.1))
    model.add(Dense(5, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # stop = EarlyStopping(monitor="loss", patience=20, mode="auto")


    model.summary()
    
    model.fit(x_data, y_data, batch_size=64, epochs=500)
    # model.fit(x_data, y_data, batch_size=64, epochs=500, callbacks=[stop])
    print("_________________________________________________________________________________________________________________")
    loss, acc = model.evaluate(x_data, y_data)
    print("loss >> ", loss)
    print("acc >>", acc, end="\n")



    ## 4. 모델 저장
    path = config.intent_model_path
    file_list = os.listdir(path)

    new_num = 0
    if os.path.exists(path):    # 파일 있을경우
        for i in file_list:
            num = int(i.split(".")[0].split("-")[-1])

            if new_num <= num:
                new_num = num + 100
            else:
                pass

        
        model_name = "intent_model-"+str(new_num)+".h5"
        weights_name = "intent_weights-"+str(new_num)+".h5"
        print("\n\nFile name >>",model_name)
        model.save(path+model_name)
        model.save_weights(path+weights_name)
            
    else:
        model.save(path+"intent_model-100.h5")
        model.save_weights(path+"intent_weights-100.h5")

    print("\n#### MODEL SAVE ####", end='\n')
        

################################### start ###################################


if __name__ == "__main__":
    main()




'''
_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
conv2d_1 (Conv2D)            (None, 14, 299, 12)       60
_________________________________________________________________
max_pooling2d_1 (MaxPooling2 (None, 14, 299, 12)       0
_________________________________________________________________
conv2d_2 (Conv2D)            (None, 12, 297, 12)       1308
_________________________________________________________________
max_pooling2d_2 (MaxPooling2 (None, 12, 297, 12)       0
_________________________________________________________________
conv2d_3 (Conv2D)            (None, 9, 294, 12)        2316
_________________________________________________________________
max_pooling2d_3 (MaxPooling2 (None, 9, 294, 12)        0
_________________________________________________________________
conv2d_4 (Conv2D)            (None, 8, 293, 12)        588
_________________________________________________________________
max_pooling2d_4 (MaxPooling2 (None, 8, 293, 12)        0
_________________________________________________________________
conv2d_5 (Conv2D)            (None, 6, 291, 12)        1308
_________________________________________________________________
max_pooling2d_5 (MaxPooling2 (None, 6, 291, 12)        0
_________________________________________________________________
conv2d_6 (Conv2D)            (None, 3, 288, 12)        2316
_________________________________________________________________
max_pooling2d_6 (MaxPooling2 (None, 3, 288, 12)        0
_________________________________________________________________
conv2d_7 (Conv2D)            (None, 2, 287, 12)        588
_________________________________________________________________
max_pooling2d_7 (MaxPooling2 (None, 2, 287, 12)        0
_________________________________________________________________
conv2d_8 (Conv2D)            (None, 12, 285, 10)       228
_________________________________________________________________
max_pooling2d_8 (MaxPooling2 (None, 12, 285, 10)       0
_________________________________________________________________
conv2d_9 (Conv2D)            (None, 9, 282, 12)        1932
_________________________________________________________________
max_pooling2d_9 (MaxPooling2 (None, 9, 282, 12)        0
_________________________________________________________________
flatten_1 (Flatten)          (None, 30456)             0
_________________________________________________________________
batch_normalization_1 (Batch (None, 30456)             121824
_________________________________________________________________
dense_1 (Dense)              (None, 128)               3898496
_________________________________________________________________
dense_2 (Dense)              (None, 5)                 645
=================================================================
Total params: 4,031,609
Trainable params: 3,970,697
Non-trainable params: 60,912

_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
conv2d_1 (Conv2D)            (None, 14, 299, 12)       60
_________________________________________________________________
max_pooling2d_1 (MaxPooling2 (None, 14, 299, 12)       0
_________________________________________________________________
conv2d_2 (Conv2D)            (None, 12, 297, 12)       1308
_________________________________________________________________
max_pooling2d_2 (MaxPooling2 (None, 12, 297, 12)       0
_________________________________________________________________
conv2d_3 (Conv2D)            (None, 9, 294, 12)        2316
_________________________________________________________________
max_pooling2d_3 (MaxPooling2 (None, 9, 294, 12)        0
_________________________________________________________________
conv2d_4 (Conv2D)            (None, 8, 293, 12)        588
_________________________________________________________________
max_pooling2d_4 (MaxPooling2 (None, 8, 293, 12)        0
_________________________________________________________________
conv2d_5 (Conv2D)            (None, 6, 291, 12)        1308
_________________________________________________________________
max_pooling2d_5 (MaxPooling2 (None, 6, 291, 12)        0
_________________________________________________________________
conv2d_6 (Conv2D)            (None, 3, 288, 12)        2316
_________________________________________________________________
max_pooling2d_6 (MaxPooling2 (None, 3, 288, 12)        0
_________________________________________________________________
conv2d_7 (Conv2D)            (None, 2, 287, 12)        588
_________________________________________________________________
max_pooling2d_7 (MaxPooling2 (None, 2, 287, 12)        0
_________________________________________________________________
conv2d_8 (Conv2D)            (None, 12, 285, 10)       228
_________________________________________________________________
max_pooling2d_8 (MaxPooling2 (None, 12, 285, 10)       0
_________________________________________________________________
conv2d_9 (Conv2D)            (None, 9, 282, 12)        1932
_________________________________________________________________
max_pooling2d_9 (MaxPooling2 (None, 9, 282, 12)        0
_________________________________________________________________
conv2d_10 (Conv2D)           (None, 8, 281, 12)        588
_________________________________________________________________
max_pooling2d_10 (MaxPooling (None, 8, 281, 12)        0
_________________________________________________________________
conv2d_11 (Conv2D)           (None, 12, 279, 10)       876
_________________________________________________________________
max_pooling2d_11 (MaxPooling (None, 12, 279, 10)       0
_________________________________________________________________
conv2d_12 (Conv2D)           (None, 9, 276, 12)        1932
_________________________________________________________________
max_pooling2d_12 (MaxPooling (None, 9, 276, 12)        0
_________________________________________________________________
flatten_1 (Flatten)          (None, 29808)             0
_________________________________________________________________
batch_normalization_1 (Batch (None, 29808)             119232
_________________________________________________________________
dense_1 (Dense)              (None, 128)               3815552
_________________________________________________________________
dense_2 (Dense)              (None, 5)                 645
=================================================================
Total params: 3,949,469
Trainable params: 3,889,853
Non-trainable params: 59,616
'''