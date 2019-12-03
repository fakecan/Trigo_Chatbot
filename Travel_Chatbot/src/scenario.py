from crawler_restaurant import recommend_restaurant
from crawler_weather import today_weather
from crawler_weather import tomorrow_weather
from crawler_weather import this_week_weather
from crawler_weather import specific_weather
from crawler_weather import after_tomorrow_weather
from crawler_dust import today_dust
from crawler_dust import tomorrow_dust
from crawler_dust import after_tomorrow_dust
from crawler_travel import recommand_travelCity
from crawler_attraction import recommand_attraction


from crawler_configs import Crawlerconfigs
from recommand.season_travel import season_recommand

from util.chatdb import addChat


config = Crawlerconfigs()
positions = (None, None, None)
tmp = None
end_flag = False



def restaurant(named_entity, state, slot, uid):    # keyword_group, entity_group
    print("[DEBUG1-1]scenario restaurant (named_entity) >>", named_entity, end="\n\n")
    keyword_group = named_entity[0]
    print("[DEBUG1-2]scenario restaurant (keyword) >> ", keyword_group, end="\n")
    entity_group = named_entity[1]
    print("[DEBUG1-2]scenario restaurant (entity) >> ", entity_group, end="\n\n")
    location = []
    restaurants = []

    for k in zip(keyword_group, entity_group):
        if 'LOCATION' in k[1]:
            location.append(k[0])
        elif 'RESTAURANT' in k[1]:
            restaurants.append(k[0])

    print("[DEBUG1-3]scenario restaurant (location) >>", location, end="\n")
    print("[DEBUG1-3]scenario restaurant (restaurants) >>", restaurants, end="\n\n")

    # request slot(without location info)
    if len(location) == 0:
        # if you receive a slot
        if slot is not None:
            lo = slot
            location.append(lo)
            slot = None

            # without restaurant info
            if len(restaurants) == 0:
                if slot is not None:
                    restaurants.append(slot)
                    result = location + restaurants
                    print("\n[DEBUG1-5]restaurant (slot added result) >>", result, end="\n\n\n")

                    answer = recommend_restaurant(' '.join(result))
                    addChat(uid, lo, answer[0])
                    return answer
                
                else:
                    state = "restaurant"
            
                    msg = '어떤 음식으로 알려드릴까요?'
                    print("[DEBUG1-3]scenario restaurant (state1) >>", state, end="\n\n")
                    print("[DEBUG1-3]scenario restaurant (location1) >>", location, end="\n")
                    print("[DEBUG1-3]scenario restaurant (restaurants1) >>", restaurants, end="\n\n\n")
                    print(msg, end="\n\n")

                    print('Input Question \n', end='', sep='')
                    keyword_group.insert(0, location[0])
                    print("[DEBUG1-4]scenario restaurant (keyword_group) >>", keyword_group, end="\n")
                    entity_group.insert(0, "LOCATION")
                    print("[DEBUG1-4]scenario restaurant (entity_group) >>", entity_group, end="\n")

                    return msg, state, named_entity, None, positions, end_flag

            else:
                result = location + restaurants
                print("\n[DEBUG1-5]restaurant (slot added result) >>", result, end="\n\n")
                answer = recommend_restaurant(' '.join(result))
                addChat(uid, lo, answer[0])
                # return recommend_restaurant(' '.join(result))
                return answer
        
        # without slot
        else:
            state = "restaurant"
            
            msg = '어떤 지역으로 알려드릴까요?'
            print("[DEBUG1-3]scenario restaurant (state) >>", state, end="\n\n\n")
            print(msg, end="\n\n")

            print('Input Question \n', end='', sep='')
            return msg, state, named_entity, None, positions, end_flag
    

    # if you have location info but no restaurant info
    if len(location) != 0 and len(restaurants) == 0:
        if slot is not None:
            restaurants.append(slot)
            result = location + restaurants
            print("\n[DEBUG1-5]restaurant (slot added result) >>", result, end="\n\n")
            answer = recommend_restaurant(' '.join(result))
            addChat(uid, slot, answer[0])

            return answer
        
        else:
            state = "restaurant"
            
            msg = '어떤 음식으로 알려드릴까요?'
            print("[DEBUG1-3]scenario restaurant (state2) >>", state, end="\n")
            print("[DEBUG1-3]scenario restaurant (location2) >>", location, end="\n")
            print("[DEBUG1-3]scenario restaurant (restaurants2) >>", restaurants, end="\n\n\n")
            print(msg, end="\n\n")

            print('Input Question \n', end='', sep='')
            return msg, state, named_entity, None, positions, end_flag

    else:
        result = location + restaurants
        print("\n[DEBUG1-5]restaurant (result) >>", result)
        
        return recommend_restaurant(' '.join(result))



def weather(named_entity, state, slot, uid):
    print("[DEBUG1-1]scenario weather (named_entity) >>", named_entity, end="\n\n")
    keyword_group = named_entity[0]
    print("[DEBUG1-2]scenario weather (keyword) >>", keyword_group, end="\n")
    entity_group = named_entity[1]
    print("[DEBUG1-2]scenario weather (entity) >>", entity_group, end="\n\n")
    date = []
    location = []

    for k in zip(keyword_group, entity_group):
        if 'DATE' in k[1]:
            date.append(k[0])
        elif 'LOCATION' in k[1]:
            location.append(k[0])
    
    print("[DEBUG1-3]scenario weather (date) >> ", date, end="\n")
    print("[DEBUG1-3]scenario weather (location) >> ", location, end="\n\n")

    if len(date) == 0:
        date.append('오늘')

    # request slot
    if len(location) == 0:
        # if you receive a slot
        if slot is not None:
            location.append(slot)
            print("[DEBUG1-4]scenario weather (slot added location) >> ", location, end="\n\n\n")

            if '오늘' in date:
                answer = today_weather(' '.join(location))
                addChat(uid, slot, answer[0])
                return answer
            elif date[0] == '내일':
                answer = tomorrow_weather(' '.join(location))
                addChat(uid, slot, answer[0])
                return answer
            elif '모레' in date or '내일모레' in date:
                answer = after_tomorrow_weather(' '.join(location))
                addChat(uid, slot, answer[0])
                return answer
            elif '이번' in date and '주' in date:
                answer = this_week_weather(' '.join(location))
                addChat(uid, slot, answer[0])
                return answer
            else:
                answer = specific_weather(' '.join(location), ' '.join(date))
                addChat(uid, slot, answer[0])
                return answer
        
        else:
            state = "weather"
            
            msg = "어떤 지역의 날씨를 알려드릴까요?"
            print("[DEBUG1-4]scenario weather (state) >>", state, end="\n\n")
            print("[DEBUG1-3]scenario weather (date) >> ", date, end="\n")
            print("[DEBUG1-3]scenario weather (location) >> ", location, end="\n\n\n")
            print(msg, end="\n\n")

            print('Input Question \n', end='', sep='')
            
            return msg, state, named_entity, None, positions, end_flag


    if '오늘' in date:
        return today_weather(' '.join(location))
    elif date[0] == '내일':
        return tomorrow_weather(' '.join(location))
    elif '모레' in date or '내일모레' in date:
        return after_tomorrow_weather(' '.join(location))
    elif '이번' in date and '주' in date:
        return this_week_weather(' '.join(location))
    else:
        return specific_weather(' '.join(location), ' '.join(date))



def dust(named_entity, state, slot, uid):
    print("[DEBUG1-1]scenario dust (named_entity) >>", named_entity, end="\n\n")
    keyword_group = named_entity[0]
    print("[DEBUG1-2]scenario dust (keyword) >>", keyword_group, end="\n")
    entity_group = named_entity[1]
    print("[DEBUG1-2]scenario dust (entity) >>", entity_group, end="\n\n")
    date = []
    location = []

    for k in zip(keyword_group, entity_group):
        if 'DATE' in k[1]:
            date.append(k[0])
        elif 'LOCATION' in k[1]:
            location.append(k[0])

    print("[DEBUG1-3]scenario dust (data) >> ", date, end="\n")
    print("[DEBUG1-3]scenario dust (location) >> ", location, end="\n\n")

    if len(date) == 0:
        date.append('오늘')

    # request slot
    if len(location) == 0:
        # if you receive a slot
        if slot is not None:
            location.append(slot)
            print("[DEBUG1-4]scenario dust (slot added location) >> ", location, end="\n\n\n")
            
            if '오늘' in date:
                answer = today_dust(' '.join(location))
                addChat(uid, slot, answer[0])
                return answer
            elif date[0] == '내일':
                print("####### dust (tmp) #######\n", tmp, end="\n\n\n")
                answer = tomorrow_dust(' '.join(location))
                addChat(uid, slot, answer[0])
                return answer
            elif '모레' in date or '내일모레' in date:
                answer = after_tomorrow_dust(' '.join(location))
                addChat(uid, slot, answer[0])
                return answer
            else:
                msg = '오늘, 내일, 모레의 미세먼지 상태만 알 수 있어요'
                addChat(uid, slot, msg)
                
                return msg, None, None, None, positions, end_flag
            
        else:
            state = "dust"

            msg = "어떤 지역의 미세먼지를 알려드릴까요?"
            print("[DEBUG1-3]scenario dust (state) >>", state, end="\n\n")
            print("[DEBUG1-3]scenario dust (data) >> ", date, end="\n")
            print("[DEBUG1-3]scenario dust (location) >> ", location, end="\n\n\n")
            print(msg, end="\n\n")

            print('Input Question \n', end='', sep='')

            return msg, state, named_entity, None, positions, end_flag

    if len(date) != 0:
        if '오늘' in date:
            return today_dust(' '.join(location))
        elif date[0] == '내일':
            return tomorrow_dust(' '.join(location))
        elif '모레' in date or '내일모레' in date:
            return after_tomorrow_dust(' '.join(location))
        else:
            msg = '오늘, 내일, 모레의 미세먼지 상태만 알 수 있어요'
            
            return msg, None, None, None, positions, end_flag



def travel(named_entity, state, slot, uid):
    print("[DEBUG1-1]scenario travel (named_entity) >>", named_entity, end="\n\n")
    keyword_group = named_entity[0]
    print("[DEBUG1-2]scenario travel (keyword) >>", keyword_group, end="\n")
    entity_group = named_entity[1]
    print("[DEBUG1-2]scenario travel (entity) >>", entity_group, end="\n")
    purpose = []

    for k in zip(keyword_group, entity_group):
        if 'PURPOSE' in k[1]:
            purpose.append(k[0])
        elif 'TRAVEL' in k[1]:
            purpose.append(k[0])

    print("[DEBUG1-3]scenario travel (purpose) >>", purpose, end="\n\n")

    # request slot
    if len(purpose) == 0:
        
        msg = season_recommand()

        # if you receive a slot
        if slot is not None:
            purpose.append(slot)
            print("[DEBUG1-3]scenario travel (slot added purpose) >>", purpose, end="\n\n\n")
            answer = recommand_travelCity(' '.join(purpose))
            addChat(uid, slot, answer[0])
            
            return answer

        else:
            state = "travel"

            msg += "아니면 어떤 여행을 하고싶으세요?  🔍 " +"\n\n" + "키워드 >> [해수욕, 계곡, 관광, 온천, 레져, 계절]"
            print("[DEBUG1-3]scenario travel (state) >>", state, end="\n\n")
            print("[DEBUG1-3]scenario travel (purpose) >>", purpose, end="\n\n\n")
            print(msg, end="\n\n")

            print('Input Question \n', end='', sep='')
            
            return msg, state, named_entity, None, positions, end_flag


    print("[DEBUG1-3]scenario travel (purpose) >>", purpose)
    return recommand_travelCity(' '.join(purpose))



def attraction(named_entity, state, slot, uid):
    print("[DEBUG1-1]scenario attraction (named_entity) >>", named_entity, end="\n\n")
    keyword_group = named_entity[0]
    print("[DEBUG1-2]scenario attraction (keyword) >>", keyword_group, end="\n")
    entity_group = named_entity[1]
    print("[DEBUG1-2]scenario attraction (entity) >>", entity_group, end="\n\n")
    location = []
    attraction = []

    for k in zip(keyword_group, entity_group):
        if 'LOCATION' in k[1]:
            location.append(k[0])
        elif 'TRAVEL' in k[1]:
            attraction.append(k[0])
    
    print("[DEBUG1-3]scenario attraction (location) >>", location, end="\n")
    print("[DEBUG1-3]scenario attraction (attraction) >>", attraction, end="\n\n")


    if len(attraction) == 0:
        if slot is not None:
            attraction.append(slot)
            print("[DEBUG1-3]scenario attraction (slot added attraction) >>", attraction, end="\n")
            answer = recommand_attraction(' '.join(location), ' '.join(attraction))
            addChat(uid, slot, answer[0])

            return answer

        else:
            state = "attraction"

            msg = "어떤 여행지를 알려드릴까요?"
            print("[DEBUG1-3]scenario attraction (state) >>", state, end="\n\n")
            print("[DEBUG1-3]scenario attraction (location) >>", location, end="\n")
            print("[DEBUG1-3]scenario attraction (attraction) >>", attraction, end="\n\n")
            print(msg, end="\n\n")

            print('Input Question \n', end='', sep='')
            
            return msg, state, named_entity, None, positions, end_flag


    print("[DEBUG1-3]scenario attraction (attraction) >>", attraction, end="\n")
    return recommand_attraction(' '.join(location), ' '.join(attraction))