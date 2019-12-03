import random
import re
import urllib
from urllib.request import urlopen, Request
import requests

import bs4

from . import parsing_test as ps
# import parsing_test as ps   # 테스트 경로


def ganghwa_cr(city, info):
    # url = 'http://info.hanatour.com/dest/content/know/51?ctype=1000010089&contentID=1000078061101'
    url = 'http://info.hanatour.com/dest/content/know/' + city +'?ctype=1000010089&contentID=' + info

    req = Request(url)
    page = urlopen(req)
    html = page.read()

    soup = bs4.BeautifulSoup(html, 'html.parser')


    # print("_____________________________________________________________________________________________________________")
    ## 강화 일반 정보
    data = soup.find('div', class_="new_des_content")
    # print(data, end="\n\n")

    title = list(data.select('h2'))
    title1 = ps.parsing_data(str(title[0]))
    msg = "["+title1+"]" + "\n\n"

    info = list(data)
    
    msg += ps.parsing_data(str(info[7])) + info[8] + info[12] + "\n\n\n\n"


    # print("\n\n_____________________________________________________________________________________________________________")
    ## 강화의 주요 축제
    title = list(data.select('h3'))
    title2 = ps.parsing_data(str(title[2]))
    msg += "["+title2+"]" + "\n\n"

    sub_title1 = ps.parsing_data2(str(info[53])) + "\n"
    sub_data1 = info[55] + info[57] + ps.parsing_data2(str(info[60])) + "\n\n"
    sub_title2 = ps.parsing_data2(str(info[64])) + "\n"
    sub_data2 = info[66] + info[68] + ps.parsing_data2(str(info[71])) + "\n\n"
    sub_title3 = ps.parsing_data2(str(info[75])) + "\n"
    sub_data3 = info[77] + info[79] + ps.parsing_data2(str(info[82])) + "\n\n"
    sub_title4 = ps.parsing_data2(str(info[86])) + "\n"
    sub_data4 = info[88] + info[90] + ps.parsing_data2(str(info[93])) + "\n\n"
    sub_title5 = ps.parsing_data2(str(info[97])) + "\n"    
    sub_data5 = info[99] + info[101] + ps.parsing_data2(str(info[104])) + "\n\n"

    
    msg += sub_title1 + sub_data1 + sub_title2 + sub_data2 + sub_title3 + sub_data3 + sub_title4 + sub_data4 + sub_title5 + sub_data5


    return msg



# ganghwa_cr('51', '1000078061101')
# print(ganghwa_cr('51', '1000078061101'))