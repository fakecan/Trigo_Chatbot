import numpy as np

import keras

from models.EntityModel import Load_Entity



mconfig = Load_Entity()
input_size = 20 # 사용자 질문의 벡터 크기
# vector_size = 100 # 입력 데이터의 벡터 크기
vector_size = 300 # 입력 데이터의 벡터 크기

zero = np.zeros( (vector_size,) )



def word_pred(raw, index):
    pre = []

    print("DEBUG[1-1]word_pred (raw) >>", raw, end="\n\n")
    pre = list(map(lambda word : index[word], raw))
    pre = list(map(lambda idx : pre[idx] if idx < len(pre) else zero, range(input_size)))
    pre = np.array(pre) # (input_size,)
    
    return pre



def get_entity(speech):
    pred = word_pred(speech, mconfig.word_index.wv)
    pred = np.array(pred).reshape(1, input_size, vector_size)
    model = mconfig.entity_model

    with keras.backend.get_session().graph.as_default():
        
        entity = model.predict(pred)
        
        # print('[DEBUG1-2]get_entity (entity[0]) >>\n', entity[0], end="\n\n")

        result = []
        tag_index = mconfig.entity_index.items()
        # print('[DEBUG1-2]get_entity (tag_index) >>\n', tag_index, end="\n\n")

        for index in entity[0]:
            index = np.argmax(index)
            for tag, idx in tag_index:
                if index == idx:
                    result.append(tag)
                    # print('\n[DEBUG1-2]get_entity >> (result[tag]) >>\n', result)
                    break

        print("[DEBUG1-2]get_entity (predict) >>", result)  # ['tag', 'tag', ...]
        # print("[DEBUG1-3]predict (result) >>", len(result)) # 20
        result = result[:len(speech)]
        result = (speech, result)
        
        return result