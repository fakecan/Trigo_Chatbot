import random
import re
import urllib
from urllib.request import urlopen, Request
import requests

import bs4

from . import parsing_test as ps
# import parsing_test as ps   # 테스트 경로


def jeju_cr(city, info):
    # url = 'http://info.hanatour.com/dest/content/know/7?ctype=1000010089&contentID=1000043115101'
    url = 'http://info.hanatour.com/dest/content/know/' + city +'?ctype=1000010089&contentID=' + info

    req = Request(url)
    page = urlopen(req)
    html = page.read()

    soup = bs4.BeautifulSoup(html, 'html.parser')


    # print("_____________________________________________________________________________________________________________")
    ## 제주의 지역
    data = soup.find('div', class_="new_des_content")
    # print(data, end="\n\n")

    title = list(data.select('h2'))
    title1 = ps.parsing_data(str(title[1]))
    msg = "["+title1+"]" + "\n\n"

    info = list(data)

    text = info[2]
    text = list(text[6:])
    pinfo =''.join(text)
    
    msg += pinfo + "\n\n\n"


    # print("_____________________________________________________________________________________________________________")
    ## 계절별 날씨
    title2 = ps.parsing_data(str(title[3]))
    msg += "["+title2+"]" + "\n\n"

    text = info[52]
    text = list(text[6:])
    pinfo = ''.join(text)

    msg += pinfo + "\n\n\n"


    # print("_____________________________________________________________________________________________________________")
    ## 제주의 축제
    title3 = ps.parsing_data(str(title[4]))
    msg += "["+title3+"]" + "\n\n"

    text = info[61]
    text = list(text[6:])
    pinfo = ''.join(text)
    
    msg += pinfo + "\n\n"

    text = ps.parsing_data(str(info[64]))
    text = list(text[15:])
    sub_title1 = ''.join(text[:5])
    data1 = ''.join(text[6:19])
    sub_title2 = ''.join(text[20:23])
    data2 = ''.join(text[23:48])
    sub_title3 = ''.join(text[49:52])
    data3 = ''.join(text[52:67])
    sub_title4 = ''.join(text[67:70])
    data4 = ''.join(text[70:])


    msg += sub_title1 + " : " + data1 + "\n\n" + sub_title2 + ": " + data2 + "\n\n" + sub_title3 + ": " + data3 + "\n" + sub_title4 + " :" + data4


    return msg


# print(jeonju_cr('7', '1000043115101'))
