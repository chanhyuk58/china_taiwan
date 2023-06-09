import requests
import base64
import json
import csv
import time
import random

def peoplesDaily(keyword, limit, page):
    keyword = '台湾'
    # page = 350
    key_bytes = keyword.encode('utf8')
    key_base64 = base64.b64encode(key_bytes)
    key_base64_str = key_base64.decode('utf8')
    url = 'http://search.people.cn/search-platform/front/search'

    data = {
        "key":str(keyword),
        "page":int(page),
        # "limit":int(limit),
        "hasTitle":True,
        "hasContent":True,
        "isFuzzy":True,
        "type":0,
        "sortType":0,
        "startTime":0,
        "endTime":0
        }

    headers = {
        "Content-Type":"application/json",
        "Host":"search.people.cn",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
        "Referer":"http://search.people.cn/s/?keyword=" + key_base64_str + "&st=1&_=1677207568459"
        }

    res = requests.post(url, headers=headers, data=json.dumps(data)).json()
    res['data']

    total = res['data']['size']
    res_list = [['index', 'origin', 'title', 'inputime', 'summary', 'link']]
    for i in range(0,int(total)):
        single_list = []
        single = res['data']['records'][i]
        single_list.extend(
            [
                int(i+1),
                single['originName'],
                single['title'],
                single['inputTime'],
                # single['editor'],
                single['content'],
                single['url']
            ]
        )
        res_list.append(single_list)

    return res_list
# 省
for j in range(75, 350):
    res1 = peoplesDaily("台湾", 2965, j)

    with open(f'./pd{j}.csv', 'w', encoding='utf-8-sig') as f:
        write = csv.writer(f, dialect='excel')
        write.writerows(res1)
    print(f'page{j} is done!')
    time.sleep(random.randrange(0,10))

