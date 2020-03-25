import time
from datetime import datetime
import random, sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from crawler_configs import Crawlerconfigs



config = Crawlerconfigs()



def season_recommand():
    # 계절별 여행지 추천 (가을 여행지만 구현)
    now = datetime.now()
    current_month = now.month
    
    for season, i in config.seasons.items():
        if current_month in i:
            break
    
    if season == "가을":
        recommand_at = []
        while True:
            if not len(recommand_at) == 2:
                recommand_at.append(random.choice(list(config.re_autumn)))

            recommand_at = list(set(recommand_at))
            if len(recommand_at) == 2:
                break

        # print(recommand_at, end="\n\n\n") # ['산', '드라이브']
    
    msg = season + "에는 "+ recommand_at[0] +" 또는 " + recommand_at[1] + " 여행은 어떠세요?  😃" + "\n\n\n"


    re_travel1 = []
    re_travel2 = []
    for i in range(2):
        re_travel1.append(random.choice(list(config.re_autumn[recommand_at[0]].items())))
    for i in range(2):
        re_travel2.append(random.choice(list(config.re_autumn[recommand_at[1]].items())))

    # print(re_travel1)   # list
    # print(re_travel2, end="\n\n\n")


    # 첫번째 추천 리스트
    msg += "<" + season + recommand_at[0] + ">" + " 추천 여행지로는 [" +str(re_travel1[0][0]) +", " +str(re_travel1[0][1]) + "], [" + str(re_travel1[1][0]) + ", " +str(re_travel1[1][1]) +"]" + "\n\n"
    msg += "<" + season + recommand_at[1] + ">" + " 추천 여행지로는 [" +str(re_travel2[0][0]) +", " +str(re_travel2[0][1]) + "], [" + str(re_travel2[1][0]) + ", " +str(re_travel2[1][1]) +"]" + "\n\n\n"


    return msg





# print(season_recommand())