import re
from random import randint
from urllib.request import Request, urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup

www = 'https://m.search.naver.com/search.naver?query='

# → 플레이스(관광지)게시물을 크롤링합니다.
def place_cr(url):
    req = Request(url)
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    print('place_cr >>', url, end="\n\n")

    # 제목
    title = soup.find('span', class_ = '_3XamXurMr_').text
    # print("\n\n[DEBUG1-1] place_cr (title) >>", title, end="\n\n")
    content = title + "\n"

    # 정보
    info = soup.find('ul', class_ = '_6aUG7snIOF')
    info = info.find_all('li', class_ = '_1M_IzKd2N_')

    for item in info:
        label = ''
        item_class = item['class'][1]

        # 패스시킬 정보
        if item_class in ['_38kvCjMhn9', '_3XI4vbbwyp']: # 키워드, 안내
            continue

        # 주소 **** (태그 변경됨 >> item_class 변경됨)
        # elif item_class == '_1aj6--puXw':
        elif item_class == '_1h3B_0FxjX':
            address = item.find('p', class_='_2yqUQrcZuk').text
            print("\n\n[DEBUG1-1] place_cr (address) >>", address, end="\n\n")
            content += '\n📬 주소\n' + item.find('p', class_ = '_2yqUQrcZuk').text + "\n"
        
        # 영업시간
        elif item_class == '_2KHqke0mcE':
            biztime = item.find_all('div', class_ = '_2ZP3jVU_Mp')
            content += '\n⏰ 영업시간\n'
            for i in biztime:
                content += i.text + "\n"
        
        # 요금
        elif item_class == '_1nfcXq8-cV':
            price = item.find_all('div', class_ = '_20Y9lBU_Mw')
            content += '\n💲 요금'
            for i in price:
                content += '\n'+ i.find('div', class_ = '_2O0eVpLc6z').text
                content += i.find('div', class_ = '_3QTFMQGyTu').text

        # 홈페이지
        elif item_class == '_2iN9byczr4':
            content += '\n\n🏠 홈페이지\n' + item.find('a', class_ = '_1RUzg6c8aj').text + "\n\n"

        # 설명
        elif item_class == '_3__3iVrZzf':
            content += '\n🔎 정보\n'
            try: content += item.find('span', class_ = 'WoYOwsMl8Q').text
            except: content += item.find('p', class_ = '_20Y9lBU_Mw').text
        
        # 그 외
        # else:
        #     if item_class == 'undefined':
        #         content += '\n\n\n[주차]\n'

        #     elif item_class == '_3QIuPg9fjo':
        #         content += '\n[제공]\n'

        #     else:
        #         label = item_class

        #     content += ' : '+ item.text + "\n\n"

    # 이미지
    try:
        img = soup.find('meta', property = 'og:image')
        if not soup.find('meta', property = 'og:image') == None:
            imgurl = img['content']
    except:
        print("[DEBUG1-1]attraction_crawler place_cr (ERROR)")

    print("\n[DEBUG1-2] attraction_crawler (msg) >>\n", content)
    print("\n[DEBUG1-2] attraction_crawler (imgurl) >>\n", imgurl)
    print("\n[DEBUG1-2] attraction_crawler (url) >>\n", url)
    
    return content, imgurl, url



# 검색된 플레이스
def place_link(str_):

    encText = quote(str_)
    url = www + encText
    req = Request(url)
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    print('place_link >>',url, end="\n")
    
    find_soup = soup.find('a', class_ = '_1_hm24bR6B') # 명소
    
    if not find_soup == None:
        url = find_soup['href']
        
        msg, imgurl, info = place_cr(url)

        print('\n\n[DEBUG1-3]place_list (url)\n', info)
        return msg, imgurl, info

    else:
        return None, None, None



# 검색된 축제 목록
def place_list(str_):
    encText = quote(str_)
    url = 'https://m.search.naver.com/search.naver?query=' + encText
    req = Request(url)
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    print('place_list >>',url)
    
    find_soup = soup.find('div', class_ = '_3VuqCwEqtL') # 명소들의 목록
    
    if not find_soup == None:

        # 목록
        travel_index = soup.find_all('a', class_ = 'EWKS6nD6CP')
        if len(travel_index) <= 0:
            travel_index = soup.find_all('a', class_ = '_2aE-_9qmC8')

        if len(travel_index) <= 0:
            travel_index = soup.find_all('a', class_ = '_3F_-wxxna5')

        # 랜덤으로 고르기
        len_travel = len(travel_index)
        print(len_travel)
        pick = randint(0, len_travel - 1)
        url = travel_index[pick]['href']

        msg, imgurl, info = place_cr(url)

        print('\n\n[DEBUG1-3]place_list (url)\n', info)
        return msg, imgurl, info

    else:
        return None, None, None