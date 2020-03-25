import random
import re
import urllib
from urllib.request import urlopen, Request
import requests

import bs4

from . import parsing_test as ps
# import parsing_test as ps   # 테스트 경로


def seoul_cr(city, info):
    # url = 'http://info.hanatour.com/dest/content/know/36?ctype=1000010089&contentID=1000056139101'
    url = 'http://info.hanatour.com/dest/content/know/' + city +'?ctype=1000010089&contentID=' + info

    req = Request(url)
    page = urlopen(req)
    html = page.read()

    soup = bs4.BeautifulSoup(html, 'html.parser')

    # msg =""

    # print("_____________________________________________________________________________________________________________")
    ## 서울의 역사
    data = soup.find('div', class_="new_des_content")

    title = list(data.select('h2'))
    title1 = ps.parsing_data(str(title[0]))
    msg = "["+title1+"]" + "\n"

    info = list(data)
    msg += info[4] + "\n\n\n\n"

    #print("_____________________________________________________________________________________________________________")
    ## 도보관광코스
    title = list(data.select('h4'))
    title2 = ps.parsing_data(str(title[3]))
    msg += "["+title2+"]" + "\n\n"

    table = soup.find('div', class_="nd-table-wrap").find_all('td')


    for i in range(2, 16):
        if i % 2 == 0:
            msg += ps.parsing_data(str(table[i])) + " >> "
        else:
            msg += ps.parsing_data(str(table[i])) + "\n\n"


    return msg



# print(seoul_cr('35', '1000056139101'))