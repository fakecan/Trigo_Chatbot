import re
from random import randint
from urllib.request import Request, urlopen
from urllib.parse import quote
from bs4 import BeautifulSoup

www = 'https://m.search.naver.com/search.naver?query='

# → 축제 게시물을 크롤링합니다.
def festival_cr(url, _list = False):

    if not _list:
        encText = quote(url)
        url = www + encText

    req = Request(url)
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    print('festival_cr',url)

    info = soup.find('div', class_ = 'festival_detail')
    if not info == None:
        festival_title = info.find('h3', class_ = 'festival_title')
        
        # 제목
        title = festival_title.find('a', class_ = '_text').text
        content = '이름 : '+ title

        # 홈페이지
        href = festival_title.find('a', class_ = '_text')['href']
        content += '\n홈페이지 : '+ href

        # 진행 상태
        try :
            state = festival_title.find('span', class_ = 'state ing').text
            content += '\n진행상태 : '+ state
        except: pass

        # 정보
        dlist = info.find('dl')
        dt = dlist.find_all('dt')
        dd = dlist.find_all('dd')
        
        for t, d in zip(dt, dd):
            content += '\n' + t.text + ' : ' + d.text

        return content
    else: return None



# → 검색된 축제 목록
def festival_list(str_):

    encText = quote(str_)
    url = www + encText
    req = Request(url)
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    print('festival_list',url)

    find_soup = soup.find('div', class_ = 'festival_list') # 명소들의 목록
    if not find_soup == None:

        # 목록
        festival_index = find_soup.find_all('a', class_ = 'festival_name')

        # 랜덤으로 고르기
        len_festival = len(festival_index)
        print(len_festival)
        pick = randint(0, len_festival - 1)
        url = festival_index[pick]['href']
        return festival_cr(url, True)

    else: return None