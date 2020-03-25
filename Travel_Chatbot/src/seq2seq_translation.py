from keras import models
from keras import layers
from keras import optimizers, losses, metrics
from keras import preprocessing
from keras.models import model_from_json, load_model
from sklearn.model_selection import train_test_split

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import re

from konlpy.tag import Okt

import keras

from models.Seq2SeqModel import Load_Seq2Seq


''' 데이터 로드 '''
# 태그 단어
PAD = "<PADDING>"   # 패딩
STA = "<START>"     # 시작
END = "<END>"       # 끝
OOV = "<OOV>"       # 없는 단어(Out of Vocabulary)

# 태그 인덱스
PAD_INDEX = 0
STA_INDEX = 1
END_INDEX = 2
OOV_INDEX = 3

# 데이터 타입
ENCODER_INPUT  = 0
DECODER_INPUT  = 1
DECODER_TARGET = 2

# 한 문장에서 단어 시퀀스의 최대 개수
max_sequences = 30

# 임베딩 벡터 차원
embedding_dim = 100

# LSTM 히든레이어 차원
lstm_hidden_dim = 128

epochs = 5

# 정규 표현식 필터
RE_FILTER = re.compile("[.,!?\"':;~()]")


# Load Model
mconfig = Load_Seq2Seq()

end_flag = True



class get_seq2seq:

    def __init__(self):
        global mconfig

        self.words = mconfig.seq2words

        # 단어와 인덱스의 딕셔너리 생성
        self.word_to_index = {word: index for index, word in enumerate(self.words)}
        self.index_to_word = {index: word for index, word in enumerate(self.words)}

        self.encoder_model = mconfig.encoder_model
        self.decoder_model = mconfig.decoder_model


    ''' 띄어쓰기 구분자 치환 '''
    def space_replace(self, sentences):
        sentences_pos = []

        for sentence in sentences:
            sentence = sentence.replace(' ', '^')
            sentences_pos.append(sentence)

        return sentences_pos

    ''' 문장 결합하기 '''
    def space_join(self, sentence, mark='^'):
        space_join_sentence = sentence.replace(' ', '')
        mark_replace_sentence = space_join_sentence.replace(mark, ' ')

        return mark_replace_sentence


    ''' 단어 사전 생성 '''
    # 형태소분석 함수
    def pos_tag(self, sentences):
        
        # KoNLPy 형태소분석기 설정
        tagger = Okt()
        
        # 문장 품사 변수 초기화
        sentences_pos = []
        
        # 모든 문장 반복
        for sentence in sentences:
            # 특수기호 제거
            sentence = re.sub(RE_FILTER, "", sentence)
            
            # 배열인 형태소분석의 출력을 띄어쓰기로 구분하여 붙임
            sentence = " ".join(tagger.morphs(sentence))
            sentences_pos.append(sentence)
            
        return sentences_pos

    # 문장을 인덱스로 변환
    def convert_text_to_index(self, sentences, vocabulary, type): 
        
        sentences_index = []
        
        # 모든 문장에 대해서 반복
        for sentence in sentences:
            sentence_index = []
            
            # 디코더 입력일 경우 맨 앞에 START 태그 추가
            if type == DECODER_INPUT:
                sentence_index.extend([vocabulary[STA]])
            
            # 문장의 단어들을 띄어쓰기로 분리
            for word in sentence.split():
                if vocabulary.get(word) is not None:
                    # 사전에 있는 단어면 해당 인덱스를 추가
                    sentence_index.extend([vocabulary[word]])
                else:
                    # 사전에 없는 단어면 OOV 인덱스를 추가
                    sentence_index.extend([vocabulary[OOV]])

            # 최대 길이 검사
            if type == DECODER_TARGET:
                # 디코더 목표일 경우 맨 뒤에 END 태그 추가
                if len(sentence_index) >= max_sequences:        # 최대 길이 초과시
                    sentence_index = sentence_index[:max_sequences-1] + [vocabulary[END]]    # 마지막 자르고 END의 Index 추가   
                else:
                    sentence_index += [vocabulary[END]]
            else:
                if len(sentence_index) > max_sequences:
                    sentence_index = sentence_index[:max_sequences]
                
            # 최대 길이에 없는 공간은 패딩 인덱스로 채움
            sentence_index += (max_sequences - len(sentence_index)) * [vocabulary[PAD]]
            
            # 문장의 인덱스 배열을 추가
            sentences_index.append(sentence_index)

        return np.asarray(sentences_index)

    def convert_index_to_text(self, indexs, vocabulary): 
        
        sentence = ''
        
        # 모든 문장에 대해서 반복
        for index in indexs:
            if index == END_INDEX:
                # 종료 인덱스면 중지
                break;
            if vocabulary.get(index) is not None:
                # 사전에 있는 인덱스면 해당 단어를 추가
                sentence += vocabulary[index]
            else:
                # 사전에 없는 인덱스면 OOV 단어를 추가
                sentence.extend([vocabulary[OOV_INDEX]])
                
            # 빈칸 추가
            sentence += ' '

        return sentence

    def make_predict_input(self, sentence):

        sentences = []
        sentences.append(sentence)
        sentences = self.pos_tag(sentences)
        input_seq = self.convert_text_to_index(sentences, self.word_to_index, ENCODER_INPUT)
        
        return input_seq


    # 텍스트 생성
    def generate_text(self, input_seq):
        
        # 입력을 인코더에 넣어 마지막 상태 구함
        states = self.encoder_model.predict(input_seq)

        # 목표 시퀀스 초기화
        target_seq = np.zeros((1, 1))
        
        # 목표 시퀀스의 첫 번째에 <START> 태그 추가
        target_seq[0, 0] = STA_INDEX
        
        # 인덱스 초기화
        indexs = []
        
        # 디코더 타임 스텝 반복
        while 1:
            # 디코더로 현재 타임 스텝 출력 구함
            # 처음에는 인코더 상태를, 다음부터 이전 디코더 상태로 초기화
            decoder_outputs, state_h, state_c = self.decoder_model.predict(
                                                    [target_seq] + states)

            # print("decoder_output :", decoder_outputs)
            # 결과의 원핫인코딩 형식을 인덱스로 변환
            index = np.argmax(decoder_outputs[0, 0, :])
            indexs.append(index)
            
            # 종료 검사
            if index == END_INDEX or len(indexs) >= max_sequences:  
                break

            # 목표 시퀀스를 바로 이전의 출력으로 설정
            target_seq = np.zeros((1, 1))
            target_seq[0, 0] = index
            
            # 디코더의 이전 상태를 다음 디코더 예측에 사용
            states = [state_h, state_c]

        # 인덱스를 문장으로 변환
        sentence = self.convert_index_to_text(indexs, self.index_to_word)
            
        return sentence


    def seq2seq_run(self, message):

        # 길이가 0인 단어는 삭제
        # words = [word for word in words if len(word) > 0]

        # # 중복된 단어 삭제
        # words = list(set(words))

        # # 제일 앞에 태그 단어 삽입
        # words[:0] = [PAD, STA, END, OOV]

        # # 단어 개수
        # print(len(words))

        # # 단어 출력
        # print(words[:20])


        # 단어 -> 인덱스
        # 문장을 인덱스로 변환하여 모델 입력으로 사용
        print("word to index :", dict(list(self.word_to_index.items())[:20]))


        # 인덱스 -> 단어
        # 모델의 예측 결과인 인덱스를 문장으로 변환시 사용
        print("index to word :", dict(list(self.index_to_word.items())[:20]))

        ''' 훈련 및 테스트 '''
        # 인덱스를 문장으로 변환
    


        ''' 문장 생성 '''
        # 예측을 위한 입력 생성
    
        
        # 문장을 인덱스로 변환

        with keras.backend.get_session().graph.as_default():

            input_seq = self.make_predict_input(message)
            print("sentence to index : ", input_seq)

            # 예측 모델로 텍스트 생성
            sentence = self.generate_text(input_seq)
            sentence = self.space_join(sentence, mark='^')
            print("predicted sentence :", sentence)

            return sentence, None, None, None, (None, None, None), end_flag