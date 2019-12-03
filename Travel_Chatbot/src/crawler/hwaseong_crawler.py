import random
import re
import urllib
from urllib.request import urlopen, Request
import requests

import bs4

from . import parsing_test as ps
# import parsing_test as ps   # 테스트 경로


def hwaseong_cr(city, info):
    # url = 'http://info.hanatour.com//dest/content/know/31?ctype=1000010089&contentID=1000047881101'
    url = 'http://info.hanatour.com/dest/content/know/' + city +'?ctype=1000010089&contentID=' + info

    req = Request(url)
    page = urlopen(req)
    html = page.read()

    soup = bs4.BeautifulSoup(html, 'html.parser')


    # print("_____________________________________________________________________________________________________________")
    ## 내가 아는 화성
    data = soup.find('div', class_="new_des_content")

    title = list(data.select('h2'))
    title1 = ps.parsing_data(str(title[0]))
    msg = "["+title1+"]" + "\n"

    info = list(data)
    
    msg += info[6] + "\n"


    # print("\n\n_____________________________________________________________________________________________________________")
    ## 화성의 축제
    title2 = ps.parsing_data(str(title[2]))
    msg += "\n\n\n["+title2+"]" + "\n"

    data1 = ps.parsing_data(str(info[53])) + "\n"

    msg += data1 + info[55] + "\n\n\n"

    
    sub_title = list(data.select('h4'))
    
    sub_title1 = ps.parsing_data(str(sub_title[0])) + "\n"
    sub_data1 = info[67] + "\n" + ps.parsing_data2(str(info[72])) + "\n\n"
    sub_title2 = ps.parsing_data(str(sub_title[1])) + "\n"
    sub_data2 = info[77] + "\n" + ps.parsing_data2(str(info[82])) + "\n\n"
    sub_title3 = ps.parsing_data(str(sub_title[2])) + "\n"
    sub_data3 = info[89] + "\n" + ps.parsing_data2(str(info[94])) + "\n\n"
    sub_title4 = ps.parsing_data(str(sub_title[3])) + "\n"
    sub_data4 = info[101] + "\n\n"

    msg += "# " + sub_title1 + sub_data1 + "# " + sub_title2 + sub_data2 + "# " + sub_title3 + sub_data3 + "# " + sub_title4 + sub_data4


    return msg



# # hwaseong_cr('31', '1000047881101')
# print(hwaseong_cr('31', '1000047881101'))