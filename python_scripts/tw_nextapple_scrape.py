import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import time
import datetime
import random
import csv

page = 200
def nextapple(startpage, endpage):
    res_list = [['index', 'title', 'date', 'summary', 'link']]
    index = 0
    for page in range(startpage, endpage + 1):
        base_url = f'https://tw.nextapple.com/search/中國/{page}?sort=time'

        res = requests.get(base_url)
        if res.status_code == 200:

            res_soup = bs(res.text, 'html.parser')
    
            ul = res_soup.select_one('div.row')
            title = ul.select('article.post-style3 h3 a')
            summary = ul.select('article.post-style3 p')
            date = ul.select('article.post-style3 time')
    
            for j in range(0,len(title)):
                index += 1
                single = []
                single.extend(
                    [
                        index,
                        title[j].text,
                        date[j].text,
                        summary[j].text,
                        title[j]['href']
                    ]
                )
                res_list.append(single)
        else:
            print('dead!')
            break
        print(f'Page {page} is... done!')
        
        time.sleep(random.randrange(1, 10))
    return res_list

def write(start, end):
    out = nextapple(start, end)

    filename = f'中國_{start}_{end}_' + str(datetime.datetime.today().strftime("%Y%m%d%H%M%S"))
        
    with open(f'./out/{filename}.csv', 'w', encoding='utf-8-sig') as f:
        write = csv.writer(f)
        write.writerows(out)
    return 

# 260
# 529
# write(230, 310)
# write(300, 380)
# write(370, 430)
# write(420, 490)
write(480, 550)
