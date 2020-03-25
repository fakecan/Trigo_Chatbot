import random
import re
import urllib
from urllib.request import urlopen, Request
import requests

import bs4

from . import parsing_test as ps
# import parsing_test as ps   # 테스트 경로


def suwon_cr(city, info):
    # url = 'http://info.hanatour.com/dest/content/know/30?ctype=1000010089&contentID=1000043614101'
    url = 'http://info.hanatour.com/dest/content/know/' + city +'?ctype=1000010089&contentID=' + info

    req = Request(url)
    page = urlopen(req)
    html = page.read()

    soup = bs4.BeautifulSoup(html, 'html.parser')


    # print("_____________________________________________________________________________________________________________")
    ## 수원의 역사
    data = soup.find('div', class_="new_des_content")

    title = list(data.select('h3'))
    title1 = ps.parsing_data(str(title[0]))
    msg = "["+title1+"]" + "\n"

    info = list(data)
    
    msg += info[4] + info[6] + "\n"


    # print("\n\n_____________________________________________________________________________________________________________")
    ## 다양한 문화 예술 행사
    title = list(data.select('h4'))
    title2 = ps.parsing_data(str(title[7]))
    msg += "\n\n\n["+title2+"]" + "\n"

    msg += info[80] + "\n\n"

    sub_title1 = ps.parsing_data(str(info[85])) + "\n"
    sub_data1 = info[87] + "\n\n"
    sub_title2 = ps.parsing_data(str(info[96])) + "\n"
    sub_data2 = info[98] + "\n\n"
    sub_title3 = ps.parsing_data(str(info[116])) + "\n"
    sub_data3 = info[118] + "\n\n\n\n"
    
    msg +=  "# " + sub_title1 + sub_data1 + "# " + sub_title2 + sub_data2 + "# " + sub_title3 + sub_data3


    # print("\n\n_____________________________________________________________________________________________________________")
    ## 월별 축제 안내
    # title = list(data.select('h3'))
    title3 = ps.parsing_data(str(title[8]))
    msg += "["+title3+"]" + "\n\n"

    table = soup.find('div', class_="nd-table-wrap").find_all('td')
    

    for i in range(3, 23):
        if i % 3 == 0:
            msg += ps.parsing_data(str(table[i])) + "(" + ps.parsing_data2(str(table[i+1])) + ") : " + ps.parsing_data(str(table[i+2])) + "\n"


    return msg



# suwon_cr('30', '1000043614101')
# print(suwon_cr('30', '1000043614101'))
