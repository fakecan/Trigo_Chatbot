import numpy as np

import keras

from configs import Configs
from models.IntentModel import Load_Intent

from util.tokenizer import tokenize
from util.spell_checker import fix


# CONFIG
config = Configs()
mconfig = Load_Intent()

cnt = 0

word2vec_model = mconfig.word2vec_model
w2c_index = word2vec_model.wv.index2word # fasttext가 적용된 단어 목록들



# 입력받은 문자열(테스트 데이터) 임베딩&차원변경
def interface_embed(text):  
    global word2vec_model
    global w2c_index

    q_raw = tokenize(text)
    q_raw = fix(q_raw)
    q_raw = list(q_raw.split(" "))

    q_raw = list(map(lambda word : word2vec_model[word], q_raw))
    # print("[DEBUG5-2]pred (q_raw) >>\n", q_raw)   # 입력 문자열 백터값 확인
    q_raw = list(map(lambda idx : q_raw[idx] if idx < len(q_raw) else np.zeros(config.vector_size, dtype=float), range(config.encode_length)))
    q_raw = np.array(q_raw)
    q_raw = q_raw.reshape(1, config.encode_length, config.vector_size, 1)

    return q_raw
    


# 의도파악
def get_intent(speech):
    
    # fallback 상태 변수
    global cnt

    # 입력 문자열 Embedding & Predict
    speech = interface_embed(speech)

    model = mconfig.intent_model
    
    
    with keras.backend.get_session().graph.as_default():

        intent = model.predict(speech)
        intent_chk = len(intent[0]) # 5
        index = np.argmax(intent)

        
        # fallback check
        for i in intent[0]:
            if i == 0:
                cnt += 1
        
        if cnt != 4:
            result = "fallback"
            cnt = 0
            print("____________________________________________________________________________________________________________________________", end="\n")

            return result
            
            
        elif cnt == 4:
            for result, num in config.intent_mapping.items():
                if index == num:
                    print(str(config.intent_mapping))
                    print("\nIntent : %s, index : %d"% (result, index), end="\n")
                    cnt = 0
                    print("____________________________________________________________________________________________________________________________", end="\n")

                    return result