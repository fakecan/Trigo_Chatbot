from keras.models import load_model
import numpy as np



class Load_Seq2Seq:
    root_path = "Travel_Chatbot/"
    seq2seq_path = root_path+"model/seq2seq/"


    def __init__(self):
        # Seq2Seq 모델
        self.encoder_model = load_model(self.seq2seq_path+"seq2seq_encoded_model_with_weights.h5")
        self.decoder_model = load_model(self.seq2seq_path+"seq2seq_decoded_model_with_weights.h5")

        ## Seq2Seq 태크
        self.seq2words = np.load(self.seq2seq_path+"seq2seq_words.npy")

        print("######################## Success Seq2Seq Model load ########################\n\n\n")