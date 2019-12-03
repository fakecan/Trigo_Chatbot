import random
import re
import urllib
from urllib.request import urlopen, Request
import requests

import bs4

from . import parsing_test as ps
# import parsing_test as ps   # 테스트 경로


def gangwon_cr(city, info):
    # url = 'http://info.hanatour.com/dest/content/know/37?ctype=1000010089&contentID=1000060540101'
    url = 'http://info.hanatour.com/dest/content/know/' + city +'?ctype=1000010089&contentID=' + info

    req = Request(url)
    page = urlopen(req)
    html = page.read()

    soup = bs4.BeautifulSoup(html, 'html.parser')


    # print("_____________________________________________________________________________________________________________")
    ## 강원도의 지리
    data = soup.find('div', class_="new_des_content")
    # print(data, end="\n\n")

    title = list(data.select('h2'))
    title1 = ps.parsing_data(str(title[0]))
    msg = "["+title1+"]" + "\n"

    info = list(data)
    
    msg += info[4] + info[6] + "\n\n"

    text = ps.parsing_data(str(info[11]))
    sub_title1 = text[1:3]
    data1 = text[4:21]
    sub_title2 = text[22:27]
    data2 = text[28:48] + "\n"
    sub_title3 = text[49:53]
    data3 = text[54:82]
    sub_title4 = text[82:87]
    data4 = text[88:116]
    sub_title5 = text[116:120]
    data5 = text[121:] + "\n"

    msg += sub_title1 + " :" + data1 + sub_title2 + " :" + data2 + sub_title3 + " :" + data3 + sub_title4 + " :" + data4 + sub_title5 + " :" + data5


    table = soup.find('div', class_="nd-table-wrap").find_all('td')

    for i in range(3,55):
        if i % 3 == 0:
            msg += ps.parsing_data(str(table[i])) + " : " + ps.parsing_data(str(table[i+1])) + "\n"


    # print("\n\n_____________________________________________________________________________________________________________")
    ## 강원도의 기후
    title = list(data.select('h3'))
    title2 = ps.parsing_data(str(title[1]))
    msg += "\n\n["+title2+"]" + "\n"

    msg += info[36] + info[38] + "\n\n\n"


    # print("\n\n_____________________________________________________________________________________________________________")
    ## 강원도의 축제
    title = list(data.select('h3'))
    title3 = ps.parsing_data(str(title[2]))
    msg += "["+title3+"]" + "\n\n"

    table2 = soup.find('div', class_="new_des_content").find_all('td')
    table2 = table2[89:145]
    

    for i in range(0, 56):
        if i == 0:
            msg += ps.parsing_data(str(table2[i])) + "(" + ps.parsing_data(str(table2[i+1])) + ") : " + ps.parsing_data(str(table2[i+3])) + "\n"
        elif i % 4 == 0:
            msg += ps.parsing_data(str(table2[i])) + "(" + ps.parsing_data(str(table2[i+1])) + ") : " + ps.parsing_data(str(table2[i+3])) + "\n"


    return msg



# gangwon_cr('37', '1000060540101')
# print(gangwon_cr('37', '1000060540101'))
