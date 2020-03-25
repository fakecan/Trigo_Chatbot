from intent_classification import get_intent
from entity_classification import get_entity
from seq2seq_translation import get_seq2seq
from image_analysis import get_image

from scenario import dust
from scenario import weather
from scenario import restaurant
from scenario import travel
from scenario import attraction

from util.tokenizer import tokenize
from util.spell_checker import fix
from util.intentdb import addIntent
from util.chatdb import addChat



#CONFIG
# get_entity = get_entity()
get_seq2seq = get_seq2seq()

print("###### application.py ######")



def run(pdata, state, type, uid):
    
    if type == "nlp":
        print('\n\nInput Questuon', end='\n')
        speech = preprocess(pdata)
        print("\n\nPreprocessed >> " + speech, sep="", end="\n\n")
        
        intent = get_intent(speech)
        print("Intent >> " + intent, sep="", end="\n\n")
        if intent != 'fallback' : addIntent(intent)
        
        # entity = get_entity.predict(speech.split(' '))
        entity = get_entity(speech.split(' '))
        print("Entity >> " + str(entity), sep="", end="\n\n")

        answer = scenario(intent, entity, state, speech, uid)
        
        # 유저ID, Question, Answer DB에 저장
        addChat(uid, speech, answer[0])
            
    else:
        answer = get_image(pdata)

    return answer



def preprocess(speech):
    speech = fix(speech)
    speech = tokenize(speech)
    speech = fix(speech)

    return speech



def scenario(intent, entity, state, speech, uid):
    if intent == "먼지":
        return dust(entity, state, None, uid)
    
    elif intent == "날씨":
        return weather(entity, state, None, uid)

    elif intent == "맛집":
        return restaurant(entity, state, None, uid)
    
    elif intent == "여행지":
        return travel(entity, state, None, uid)
    
    elif intent == "관광지":
        return attraction(entity, state, None, uid)
    
    else:
        return get_seq2seq.seq2seq_run(speech)



# 테스트
# run('바다가 유명한 여행지 알려주라')
# a = ['분위기', '좋은', '카페'], ['O', 'O', 'LOCATION']
# entity = tuple(a)
# test = scenario("맛집", entity)
# print(test)