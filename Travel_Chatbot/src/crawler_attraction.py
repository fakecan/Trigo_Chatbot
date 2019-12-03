from crawler.hanatour_crawler import travel_search, city_search
from crawler.attraction_crawler import place_link, place_list
from crawler.festival_crawler import festival_list, festival_cr



# 네이버 검색
crawler = [place_link, place_list, festival_cr, festival_list]

state = None
slot_data = None
imgurl = None
positions = [None, None]
end_flag = True



def search_cr(str_):
    # https://developers.naver.com/docs/search/blog/ 참고

    for func in crawler:
        # print("[DEBUG11-0]search_cr (crawler) >>", func, end="\n\n")
        func, imgurl, info = func(str_)
        
        if not func == None:
            return func, imgurl, info
    
    return None



def recommand_attraction(local, travel):
    global state, slot_data, imgurl, positions
    
    try:
        city_idx = city_search(local)

        # 하나투어에 없는 지역(도시)일 경우
        if city_idx == None and len(local) > 1:
            # 네이버
            print('@네이버', end="\n")
            query = local + ' ' + travel
            print('네이버 검색어 :', query, end="\n\n")
            msg, imgurl, info = search_cr(query)
            if not msg == None:
                print("\n[DEBUG1-1]recommand_attraction (msg(naver-naver)) >>\n", msg)
                print("\n[DEBUG1-1]recommand_attraction (imgurl(naver-naver)) >>\n", imgurl)
                print("\n[DEBUG1-1]recommand_attraction (url(naver-naver)) >>\n", info)
                return msg, state, slot_data, imgurl, (None, None, info), end_flag

            # 하나 투어
            print('@하나투어', end="\n")
            msg, imgurl, info = travel_search(travel, city_idx)
            if not msg == None:
                print("\n[DEBUG1-2]recommand_attraction (msg(hana)) >>\n", msg)
                print("\n[DEBUG1-2]recommand_attraction (imgurl(hana)) >>\n", imgurl)
                print("\n[DEBUG1-2]recommand_attraction (url(hana)) >>\n", info)
                return msg, state, slot_data, imgurl, (None, None, info), end_flag
        else:
            # 하나 투어
            print('@하나투어 (in 하나투어)', end="\n")
            msg, imgurl, info = travel_search(travel, city_idx)
            if not msg == None:
                print("\n[DEBUG1-1] recommand_attraction (msg(hana)) >>\n", msg)
                print("\n[DEBUG1-1] recommand_attraction (imgurl(hana)) >>\n", imgurl)
                print("\n[DEBUG1-1] recommand_attraction (url(hana-naver)) >>\n", info)
                return msg, state, slot_data, imgurl, (None, None, info), end_flag


            # 네이버
            print('@네이버 (in 하나투어)', end="\n")
            query = local + ' ' + travel
            print('네이버 검색어 :', query, end="\n\n")
            msg, imgurl, info = search_cr(query)
            if not msg == None:
                print("\n[DEBUG1-2] recommand_attraction (msg(hana-naver)) >>\n", msg)
                print("\n[DEBUG1-2] recommand_attraction (imgurl(hana-naver)) >>\n", imgurl)
                print("\n[DEBUG1-2] recommand_attraction (url(hana-naver)) >>\n", info)
                return msg, state, slot_data, imgurl, (None, None, info), end_flag
    
    except:
        print("############################")
        print("# ATTRACTION CRAWLER ERROR #")
        print("############################")

        msg = "죄송해요, " + local + travel +" 관광지에 대한 정보는 아직 준비중이에요  :(" + "\n" + "더 많은 정보를 제공할 수 있도록 노력할게요."


    return msg, state, slot_data, imgurl, (None, None, None), end_flag


# TEST
# recommand_attraction('', '에버랜드')
# recommand_attraction('', '남산타워')
# recommand_attraction('', '박물관')
# recommand_attraction('', '남산')


# print(recommand_attraction('', '에버랜드'))