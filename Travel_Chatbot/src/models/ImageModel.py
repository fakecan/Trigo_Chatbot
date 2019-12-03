from keras.models import load_model

import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.Session(config=config)

class Load_Image:
    root_path = "Travel_Chatbot/"
    image_model_path = root_path+"model/image/"


    def __init__(self):
        # Image 모델
        self.image_model = load_model(self.image_model_path+"image-model_700.h5")

        print("######################## Success Image Model load ########################\n\n\n")