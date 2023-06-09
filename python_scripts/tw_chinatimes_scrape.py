# import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import csv
import time
import random
import datetime

def chinatimes(keyword, startpage, endpage):
    base_url = 'https://www.chinatimes.com/search/'

    res_list = [['index', 'title', 'date', 'summary', 'link']]
    index = 0

    for page in range(startpage, (endpage + 1)):
        url = base_url + keyword + '?page=' + str(page) + '&chdtv'

        res = requests.get(url)

        if res.status_code == 200:
            res_soup = bs(res.text, 'html.parser')
            ul = res_soup.select_one('section div ul')
            title = ul.select('li h3.title a')
            date = ul.select('li span.date')
            summary = ul.select('li p.intro')

            # print(title[0].text)
            # print(date[0].text)
            # print(summary[0].text)
            # print(title[0])

            for j in range(0,len(title)):
                index += 1
                single = []
                single.extend(
                    [
                        index,
                        title[j].text,
                        date[j].text,
                        summary[j].text,
                        title[j].attrs['href']
                    ]
                )
                res_list.append(single)
            print('start date: ' + date[0].text)
            print('end date: ' + date[19].text)
            print('number of articles: ' + str(len(title)))
            print('Page ' + str(page) + ' done...!')
            print('--------------------------------------------')
            time.sleep(random.randrange(1, 5))
        else:
            print('dead!')
            break
    return res_list

def write(out, filename):
    with open(f'./out/{filename}.csv', 'w', encoding='utf-8') as f:
        write = csv.writer(f, dialect='excel')
        write.writerows(out)
    return print('perfect!')

df1 = chinatimes('中國', 300, 500)
df2 = chinatimes('中國', 500, 700)
df3 = chinatimes('中國', 700, 900)
df4 = chinatimes('中國', 900, 1030)
# df = chinatimes('中國', 408, 408)

filename = 'chinatimes_4' + '中國' + '_2022_at_' + str(datetime.datetime.today().strftime("%Y%m%d%H%M%S"))

write(df4, filename)

# '中國' 
# 1026
# 299 
