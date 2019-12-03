import random
import re
import urllib
from urllib.request import urlopen, Request
import requests

import bs4

from . import parsing_test as ps
# import parsing_test as ps   # 테스트 경로


def gyeongju_cr(city, info):
    # url = 'http://info.hanatour.com/dest/content/know/29?ctype=1000010089&contentID=1000043135101'
    url = 'http://info.hanatour.com/dest/content/know/' + city +'?ctype=1000010089&contentID=' + info

    req = Request(url)
    page = urlopen(req)
    html = page.read()

    soup = bs4.BeautifulSoup(html, 'html.parser')


    # print("_____________________________________________________________________________________________________________")
    ## 경주의 역사
    data = soup.find('div', class_="new_des_content")

    title = list(data.select('h2'))
    title1 = ps.parsing_data(str(title[0]))
    msg = "["+title1+"]" + "\n"

    info = list(data)
    msg += info[18] + "\n"


    # print("\n\n_____________________________________________________________________________________________________________")
    ## 지역 안내
    title2 = ps.parsing_data(str(title[1]))
    msg += "\n\n\n["+title2+"]" + "\n"

    for i in range(26,37):
        if i % 2 == 0:
            msg += info[i]
    
    msg += info[38] + "\n\n\n\n"


    # print("\n\n_____________________________________________________________________________________________________________")
    ## 경주의 사계
    title3 = ps.parsing_data(str(title[2]))
    msg += "["+title3+"]" + "\n\n"

    sub_title1 = "# 4월 '경주 벚꽃 축제', '신라 도자기  축제'\n"
    info1 = info[48] + ps.parsing_data(str(info[51])) + "\n"
    sub_title2 = "# 6~7월 '경주 연꽃 축제'\n"
    info2 = info[56] + ps.parsing_data(str(info[59])) + "\n"
    sub_title3 = "# 10월 '신라 문화제'\n"
    info3 = info[64] + ps.parsing_data(str(info[67])) + "\n"
    sub_title4 = "# 12~2월 '천년의 빛 축제'\n"
    info4 = info[74] + ps.parsing_data(str(info[77])) + "\n\n\n"

    sub_title5 = "TIP! 언제 방문해도 볼 수 있는 공연은?!\n"
    info5 = info[83]

    msg += sub_title1 + info1 + sub_title2 + info2 + sub_title3 + info3 + sub_title4 + info4 + sub_title5 + info5


    return msg



# gyeongju_cr('29', '1000043135101')
# print(gyeongju_cr('29', '1000043135101'))