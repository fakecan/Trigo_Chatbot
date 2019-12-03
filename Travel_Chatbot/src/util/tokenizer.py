from konlpy.tag import Okt

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



def tokenize(sentence):
    stop_word = []
    josa = [
        '이구나', '이네', '이야', '에', '에서', '의', '할', '수', '있는', '에는', '엔',
        '은', '는', '이', '가', '을', '를', '로서', '로', '으로', '이야', '야', '냐', '니']

    tokenizer = Okt()
    word_bag = []
    pos = tokenizer.pos(sentence)

    print("\n[DEBUG4-1]tokenize pos >>", pos)
    for word, tag in pos:
        if word in stop_word:
            continue
        elif (tag == 'Josa' and word in josa) or tag == 'Punctuation' or (tag == 'Adjective' and word in josa):
            continue
        else:
            if word == "바다로":
                word = "바다"
            word_bag.append(word)
            print("[DEBUG4-2]tokenize word_bag >>", word_bag)
    result = ' '.join(word_bag)

    return result