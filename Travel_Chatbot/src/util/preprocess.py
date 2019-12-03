from tokenizer import tokenize
from configs import Configs
from spell_checker import fix

# CONFIG
config = Configs()
df = config.df


def preprocess_data(tokenizing):
    if tokenizing:
        encode = []
        for i in df['question']:
            q = tokenize(i)
            q = fix(q)
            print("[DEBUG1-0]preprocess_data (result) >> ", q)
            encode.append(q)

    return encode