import random
import re
import urllib
from urllib.request import urlopen, Request
import requests

import bs4

from . import parsing_test as ps
# import parsing_test as ps   # 테스트 경로


def busan_cr(city, info):
    url = 'http://info.hanatour.com/dest/content/know/35?ctype=1000010089&contentID=1000060452101'
    # url = 'http://info.hanatour.com/dest/content/know/' + city +'?ctype=1000010089&contentID=' + info

    req = Request(url)
    page = urlopen(req)
    html = page.read()

    soup = bs4.BeautifulSoup(html, 'html.parser')


    # print("_____________________________________________________________________________________________________________")
    ## 부산 소개
    data = soup.find('div', class_="new_des_content")
    # print(data, end="\n\n")

    title = list(data.select('h4'))
    title1 = ps.parsing_data(str(title[0]))
    # print(title1)
    msg = "["+title1+"]" + "\n"

    info = list(data)
    msg += info[4] + info[6] + "\n\n\n\n"

    # #print("\n\n_____________________________________________________________________________________________________________")
    # ## 부산의 주요 축제
    title = list(data.select('h2'))
    title2 = ps.parsing_data(str(title[1]))
    msg += "["+title2+"]" + "\n\n\n"


    sub_title = ps.parsing_data(str(info[49]))  # 해운대 모래 축제 <봄>
    msg += sub_title + "\n"
    msg += info[52] + info[54] + "\n"
    location = ps.parsing_data(str(info[57]))
    msg += location + "\n\n\n"

    sub_title = ps.parsing_data(str(info[63]))  # 부산 바다 축제 <여름>
    msg += sub_title + "\n"
    msg += info[66] + "\n"
    location = ps.parsing_data(str(info[69]))
    msg += location + "\n\n\n"

    sub_title = ps.parsing_data(str(info[75]))  # 센텀 맥주 축제 <여름>
    msg += sub_title + "\n"
    msg += info[78] + info[80] + "\n"
    location = ps.parsing_data(str(info[83]))
    msg += location + "\n\n\n"

    sub_title = ps.parsing_data(str(info[89]))  # 부산 불꽃축제 <가을>
    msg += sub_title + "\n"
    msg += info[92] + "\n"
    location = ps.parsing_data(str(info[95]))
    msg += location + "\n\n\n"

    sub_title = ps.parsing_data(str(info[101]))
    msg += sub_title + "\n"
    msg += info[104] + info[106] + "\n"
    location = ps.parsing_data(str(info[109]))
    msg += location

    return msg



# print(busan_cr('35', '1000060452101'))
# busan_cr('35', '1000060452101')