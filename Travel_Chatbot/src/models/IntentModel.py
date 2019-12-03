# from gensim.models.word2vec import Word2Vec
from gensim.models import FastText
from  keras.models import load_model



class Load_Intent:
    root_path = "Travel_Chatbot/"
    intent_model_path = root_path+"model/intent/"
    fasttext_model_path = root_path+"model/fasttext/"

    def __init__(self):
        # 의도파악 모델
        self.word2vec_model = FastText.load(self.fasttext_model_path+"model")
        self.intent_model = load_model(self.intent_model_path+'intent_model-'+str(5400)+'.h5')
        
        print("######################## Success Intent Model load ########################\n\n\n")