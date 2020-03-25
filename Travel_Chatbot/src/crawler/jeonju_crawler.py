import random
import re
import urllib
from urllib.request import urlopen, Request
import requests

import bs4

from . import parsing_test as ps
# import parsing_test as ps   # 테스트 경로


def jeonju_cr(city, info):
    # url = 'http://info.hanatour.com/dest/content/know/28?ctype=1000010089&contentID=1000043129101'
    url = 'http://info.hanatour.com/dest/content/know/' + city +'?ctype=1000010089&contentID=' + info

    req = Request(url)
    page = urlopen(req)
    html = page.read()

    soup = bs4.BeautifulSoup(html, 'html.parser')


    # print("_____________________________________________________________________________________________________________")
    ## 전주의 문화
    data = soup.find('div', class_="new_des_content")

    title = list(data.select('h2'))
    title1 = ps.parsing_data(str(title[1]))
    msg = "["+title1+"]" + "\n"

    info = list(data)
    msg += info[16] + "\n\n\n\n"

    # print("\n\n_____________________________________________________________________________________________________________")
    ## 전라북도, 그리고 전주
    title2 = ps.parsing_data(str(title[2]))
    msg += "["+title2+"]" + "\n"

    msg += info[26] + "\n\n" + info[30] + "\n" + info[34] + "\n" + info[38] + "\n"


    return msg



# jeonju_cr('28', '1000043129101')
# print(jeonju_cr('28', '1000043129101'))
