import random
import re
import urllib
from urllib.request import urlopen, Request
import requests

import bs4

from . import parsing_test as ps
# import parsing_test as ps   # 테스트 경로


def incheon_cr(city, info):
    # url = 'http://info.hanatour.com/dest/content/know/45?ctype=1000010089&contentID=1000072355101'
    url = 'http://info.hanatour.com/dest/content/know/' + city +'?ctype=1000010089&contentID=' + info

    req = Request(url)
    page = urlopen(req)
    html = page.read()

    soup = bs4.BeautifulSoup(html, 'html.parser')


    # print("_____________________________________________________________________________________________________________")
    ## 인천
    data = soup.find('div', class_="new_des_content")

    title = list(data.select('h4'))
    title1 = ps.parsing_data(str(title[1]))
    msg = "["+title1+"]" + "\n"

    info = list(data)
    
    msg += info[8] + "\n\n\n\n"


    # print("\n\n_____________________________________________________________________________________________________________")
    ## 과거로의 시간 여행, 인천 중구
    title2 = ps.parsing_data(str(title[2]))    
    msg += "["+title2+"]" + "\n"

    msg += info[22] + info[24] + info[26] + "\n" + info[28] +"\n" + info[30] + "\n\n\n"


    # print("\n\n_____________________________________________________________________________________________________________")
    ## 인천 중구의 주요 축제
    title3 = ps.parsing_data(str(title[5]))
    msg += "["+title3+"]" + "\n\n"


    sub_title1 = "4월 - 자유공원 문화관광축제\n"
    data1 = info[65] + info[67] + "\n\n"
    sub_title2 = "5월 - 동화마을(어린이)축제\n"
    data2 = info[74] + info[76] + "\n\n"
    sub_title3 = "5월 ~ 8월 - 월미관광특구 불꽃축제\n"
    data3 = info[83] + info[85] + "\n\n"
    sub_title4 = "8월 - 무의 춤 축제\n"
    data4 = info[92] + info[94] + "\n\n"
    sub_title5 = "9월 - 인천상륙작전 월미축제\n"
    data5 = info[101] + info[103] + "\n\n"
    sub_title6 = "10월 - 연안부두축제\n"
    data6 = info[110] + info[112] + "\n\n"
    sub_title7 = "11월 - 크리스마스 트리문화 축제"
    data7 = info[119] + info[121] + "\n\n"
    
    msg += sub_title1 + data1 + sub_title2 + data2 + sub_title3 + data3 + sub_title4 + data4 + sub_title5 + data5 + sub_title6 + data6 + sub_title7 + data7

    return msg



# incheon_cr('45', '1000072355101')
# print(incheon_cr('45', '1000072355101'))
