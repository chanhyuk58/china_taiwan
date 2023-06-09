import pandas as pd
import requests
import csv
import json
import time
import random

def udn(startpage, endpage):
    res_list = [['index', 'title', 'date', 'summary', 'link']]
    index = 0

    filename = f'udn_{startpage}_{endpage}'

    endpage = endpage + 1

    for page in range(startpage, endpage):
        base_url = f'https://udn.com/api/more?page={page}&id=search:%E4%B8%AD%E5%9C%8B&channelId=2&type=searchword&last_page=4951'

        res = requests.get(base_url)
        if res.status_code == 200:
            res_json = json.loads(res.text)
            ul = res_json['lists']

            for i in range(0,20):
                index += 1
                single = []
                single.extend(
                    [
                        index,
                        ul[i]['title'],
                        ul[i]['time']['date'][:10],
                        ul[i]['paragraph'],
                        ul[i]['titleLink']
                    ]
                )
                res_list.append(single)

        else:
            print('dead!')

        print('Page ' + str(page) + ' is done ...!'
                  )
        
        time.sleep(random.randrange(1, 10))

    with open(f'./out/{filename}.csv', 'w', encoding='utf-8-sig') as f:
        write = csv.writer(f)
        write.writerows(res_list)

    return print('Done!!!')

# 1100
# 3600

# udn(1100, 1300)
# udn(1280, 1500)
# udn(1480, 1700)
# udn(1680, 1900)
# udn(1880, 2100)
# udn(2080, 2300)
# udn(2280, 2500)
# udn(2480, 2700)
# udn(2680, 2900)
# udn(2880, 3100)
udn(3080, 3300)
udn(3280, 3500)
udn(3480, 3600)
