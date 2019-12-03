import numpy as np

input_size = 20 # 사용자 질문의 벡터 크기
vector_size = 300 # 입력 데이터의 벡터 크기

zero = np.zeros( (vector_size,) )

def word_pred(raw, index):
    pre = []

    pre = list(map(lambda word : index[word], raw))
    pre = list(map(lambda idx : pre[idx] if idx < len(pre) else zero, range(input_size)))
    pre = np.array(pre) # (input_size,)
    return pre
    

# → 개체명, 인덱스 번호 매핑및 패딩 추가
def entity_pred(raw, index):
    result = []
    for tag in raw: result.append(index[tag]) # 태그값(인덱스 번호)
    for i in range(input_size - len(raw)): result.append(index['#']) # 패딩 추가
    return result