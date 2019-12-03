import string, re

def parsing_data(text):

    new_name=[]

    for c in text:
        # print(c)
        name = re.sub('[a-zA-Z/\{\}[\]\t|<>"-=^0-9]', "", c)
        if name == "":
            pass
        else:
            new_name.append(name)
        
    # print(new_name)
    new_name = ''.join(new_name)
    # print(new_name)

    
    return new_name


def parsing_data2(text):
    
    new_name=[]

    for c in text:
        name = re.sub('[a-zA-Z/\{\}[\]\t_|<>"=^]', "", c)
        if name == "":
            pass
        else:
            new_name.append(name)
        
    new_name = ''.join(new_name)
    
    return new_name