from crawler_configs import Crawlerconfigs
import re
import pandas as pd
from random import randint
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup



# CONFIG
config = Crawlerconfigs()
city_idx = config.hanatour_city
city_idx_item = city_idx.items()
attraction = config.attraction
attraction_key = attraction.keys()



# → id를 받고 게시판을 크롤링 합니다.
def content_cr(id_):
    url = 'http://info.hanatour.com/dest/content/all/' + id_
    print('url >>',url, end="\n")

    try:
        req = Request(url)
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
    
    except:
        return None

    # 제목, 부제목
    title = soup.find('h1', class_ = 'nd_spot_d_title').text
    sub = soup.find('h2', class_ = 'nd_spot_d_sub_title').text
    content = '이름 : ' + title
    content += ' - ' + sub + "\n\n"

    # 정보
    info = {}
    spot_info_wrap = soup.find('div', class_ = 'nd_spot_info_wrap')
    dts = spot_info_wrap.find('dl').select('dt') # 명칭
    dds = spot_info_wrap.find('dl').select('dd') # 값
    for d in range(len(dts)):
        dt = dts[d].text
        dd = dds[d].text
        dd = re.sub('\t','', dd)
        content += '\n'+ dt + ' : ' + dd + "\n"

    # 추천 이유
    cmt = soup.find('div', class_ = 'nd_spot_cmt').text
    content += '\n[정보]' + cmt

    # Tip
    try:
        tip = soup.find('p', class_ = 'nd_spot_cmt').text
        content += '\n\n[Tip]' + tip + "\n"
    except AttributeError: tip = None

    # 이미지
    try:
        img = soup.find('div', class_ = 'nd_spot_img_wrap').find('img')['src']
        imgurl = img
    except TypeError: img = None

    print("\n[DEBUG1-1] attraction_crawler (msg) >>\n", content, end="\n\n")
    print("\n[DEBUG1-1] attraction_crawler (url) >>\n", imgurl)


    return content, imgurl, url



# → 도시 이름을 인덱스 번호로 변환합니다.
def city_search(local):
    for city, idx in city_idx_item:
        check = city.find(local)
        if check >= 0 and len(local) > 1:
            return idx

    return None



# → 검색 단어로 관광지를 찾습니다.
def travel_search(str_, local = None):
    search = []

    # 검색된 도시가 없을 경우
    if local == None:
        for title in attraction_key:
            # title 검색
            check = title.find(str_)
            if check >= 0: search.append(title)

    # 도시가 검색된 경우
    else:
        for title in attraction_key:
            # title 검색
            check = title.find(str_)
            if check >= 0:
                #  city index 일치 여부
                id_ = attraction[title]
                id_ = re.sub('[?]contentID=[\w]*', '',id_)
                id_ = int(id_)
                if local == id_: search.append(title)
    
    # 관광지 게시글 반환
    len_search = len(search) # 검색된 관광지의 숫자
    print(search, end="\n")
    print('검색된 관광지 >>',str_, len_search, end="\n\n")

    # 검색된 관광지들 중 무작위로 하나를 선택.
    if len_search > 1:
        pick = randint(0, len_search-1)
        result = search[pick]
        result, imgurl, info = content_cr(attraction[result])
    
    # 검색된 관광지가 하나일 경우.
    elif len_search == 1:
        result = search[0]
        result, imgurl, info = content_cr(attraction[result])

    # 검색된 관광지가 없을 경우.
    else:
        result =  None
        imgurl = None
        info = None

    
    return result, imgurl, info