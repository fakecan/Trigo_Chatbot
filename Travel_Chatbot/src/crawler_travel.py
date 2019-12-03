import random
import re
import urllib
from urllib.request import urlopen, Request

import bs4

from crawler_configs import Crawlerconfigs
from util.traveldb import load_travelinfo

import crawler.parsing_test



state = None
slot_data = None
imgurl = None
positions = (None, None, None)
end_flag = True
config = Crawlerconfigs()



def check_purpose(entity):
    print("\n\n[DEBUG1-0]check_purpose (entity) >>", entity)
    info = config.info

    if entity in config.p_beach:
        # 하나투어
        city = config.beach
        select_city = random.choice(list(city.items()))

        info_index = info[str(select_city[1])]
        result = [select_city, info_index]

    elif entity in config.p_mountain:
        # 하나투어
        city = config.mountain
        select_city = random.choice(list(city.items()))

        info_index = info[str(select_city[1])]
        result = [select_city, info_index]
    
    elif entity == "온천" or entity == "스파":
        # 네이버
        city = config.spa
        select_city = random.choice(list(city.items()))

        info_index = info[str(select_city[1])]
        result = [select_city, info_index]

    elif entity == "캠핑":
        # 네이버
        city = config.camping
        select_city = random.choice(list(city.items()))

        info_index = info[str(select_city[1])]
        result = [select_city, info_index]

    elif entity in config.p_Nlandscape:
        # 하나투어
        city = config.Nlandscape
        select_city = random.choice(list(city.items()))

        info_index = info[str(select_city[1])]
        result = [select_city, info_index]

    elif entity == "역사" or entity == "유적지":
        # 하나투어
        city = config.historic
        select_city = random.choice(list(city.items()))

        info_index = info[str(select_city[1])]
        result = [select_city, info_index]

    elif entity == "체험" or entity == "관광":
        # 하나투어
        city = config.sightseeing
        select_city = random.choice(list(city.items()))

        info_index = info[str(select_city[1])]
        result = [select_city, info_index]

    elif entity == "시장" or entity == "시장 구경":
        # 하나투어
        city = config.market
        select_city = random.choice(list(city.items()))

        info_index = info[str(select_city[1])]
        result = [select_city, info_index]

    elif entity == "놀이동산" or entity == "놀이 공원":
        # 네이버
        city = config.amusement_park
        select_city = random.choice(list(city.items()))

        info_index = info[str(select_city[1])]
        result = [select_city, info_index]

    elif entity in config.p_stadium:
        # 네이버
        city = config.stadium
        select_city = random.choice(list(city.items()))

        info_index = info[str(select_city[1])]
        result = [select_city, info_index]

    elif entity == "거리":
        # 하나투어
        city = config.load
        select_city = random.choice(list(city.items()))

        info_index = info[str(select_city[1])]
        result = [select_city, info_index]
    
    elif entity == "쇼핑" or entity == "백화점":
        # 하나투어
        city = config.shopping
        select_city = random.choice(list(city.items()))

        info_index = info[str(select_city[1])]
        result = [select_city, info_index]

    elif entity in config.p_museum:
        # 네이버
        city = config.city
        select_city = random.choice(list(city.items()))

        info_index = info[str(select_city[1])]
        result = [select_city, info_index]

    elif entity == "테마 파크":
        # 네이버
        city = config.theme_park
        select_city = random.choice(list(city.items()))

        info_index = info[str(select_city[1])]
        result = [select_city, info_index]

    elif entity in config.p_amusement_park:
        # 네이버
        city = config.zoo
        select_city = random.choice(list(city.items()))

        info_index = info[str(select_city[1])]
        result = [select_city, info_index]

    elif entity in config.p_sports:
        # 네이버
        city = config.stadium
        select_city = random.choice(list(city.items()))

        info_index = info[str(select_city[1])]
        result = [select_city, info_index]

    elif entity in config.p_valley:
        city = config.valley
        select_city = random.choice(list(city.items()))

        info_index = info[str(select_city[1])]
        result = [select_city, info_index]
    
    elif entity in config.p_mountain_leisure:
        city = config.m_leisure
        select_city = random.choice(list(city.items()))
        
        info_index = info[str(select_city[1])]
        result = [select_city, info_index]

    elif entity == "리조트":
        city = config.resort
        select_city = random.choice(list(city.items()))

        info_index = info[str(select_city[1])]
        result = [select_city, info_index]

    elif entity in config.p_season:
        if entity == "봄":
            city = config.spring
            select_city = random.choice(list(city.items()))
        elif entity == "여름":
            city = config.summer
            select_city = random.choice(list(city.items()))
        elif entity == "가을":
            city = config.autumn
            select_city = random.choice(list(city.items()))
        elif entity == "겨울":
            city = config.winter
            select_city = random.choice(list(city.items()))
        
        info_index = info[str(select_city[1])]
        result = [select_city, info_index]

    else:
        print("\n[DEBUG1-0]check_purpose (99)", end="\n")
        result = [("",99), ""]
        return result
    
    return result



def recommand_travelCity(entity):
    global state, slot_data, imgurl, positions, end_flag
    
    try:
        # 추천도시 선택 >> [('도시','index'), 'info_index']
        purpose = check_purpose(entity) 
        print("\n[DEBUG1-1]recommand_travelCity (purpose) >>", purpose, end="\n\n\n")


        # 도시정보 크롤링
        if purpose[0][1] != None and purpose[0][1] != None:
            # city = purpose[0][1]    # 도시 인덱스
            city = purpose[0][0]    # 도시 이름
            info = purpose[1]       # 도시 정보 인덱스

            msg = entity +"(으)로 유명한~!  " + purpose[0][0] +"에 가보는 건 어떠세요?  " +"\n" + "제가 " + purpose[0][0]+ "에 대해 알려드릴게요!!  😃\n\n\n"

            info, imgurl = load_travelinfo(city)

            msg += info

        else:
            msg = "죄송해요, " + entity + "에 대한 여행지" +purpose[0][0] + "정보는 준비중이에요.  😥 " + "\n\n" + "더 많은 정보를 제공할 수 있도록 노력할게요."
            
    
    except:
        print("############################")
        print("#  TRAVEL CRAWLER ERROR    #")
        print("############################")

        msg = "죄송해요, " + entity + "에 대한 여행지 " +purpose[0][0] + "에 대한 정보는 아직 준비중이에요.  😥 " + "\n\n" + "더 많은 정보를 제공할 수 있도록 노력할게요."

    print("\n\n[DEBUG1-2]recommand_travelCity (msg) >>\n", msg)
    return msg, state, slot_data, imgurl, positions, end_flag



# recommand_travelCity('스파')