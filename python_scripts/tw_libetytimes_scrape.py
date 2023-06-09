import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import time
import datetime
import re
import math
import random
import csv
import os


def liberty_times(year, month, keyword):
    start_date = str(year) + f'{month:02}' + '01'
    if month in [4, 6, 9, 11]:
        end_date = str (year) + f'{month:02}' + '30'
    elif month == 2:
        end_date = str (year) + f'{month:02}' + '28'
    else:
        end_date = str (year) + f'{month:02}' + '31'

    base_url = 'https://search.ltn.com.tw/list?keyword=' + keyword + '&start_time=' + start_date + '&end_time=' + end_date + '&sort=date&type=all'

    pre = requests.get(base_url)
    pre_soup = bs(pre.text, 'html.parser')

    total = pre_soup.select_one('div.mark')
    total_num = re.findall(r'[0-9]+', total.text)
    total_page = math.ceil(int(total_num[0])/20)

    print('total number:' + str(total_num[0]) + '\ntotal page: ' + str(total_page)) 
    
    res_list = [['index', 'title', 'date', 'summary', 'link']]
    index = 0

    for i in range(1,int(total_page)):
        s_url = base_url + '&page=' + str(i)
    
        res = requests.get(s_url)

        if res.status_code == 200:
            res_soup = bs(res.text, 'html.parser')
            ul = res_soup.select_one('section div.page-name ul')
            title = ul.select('li div.cont a.tit')
            date = ul.select('li div.cont span')
            summary = ul.select('li p')
        
            for j in range(0,20):
                index += 1
                single = []
                single.extend(
                    [
                        index,
                        title[j]['title'],
                        date[j].text,
                        summary[j].text,
                        title[j]['href']
                    ]
                )
                res_list.append(single)

        else:
            print('dead!')
            break

        print('On page ' + str(i) + ' of ' + str(total_page) +' in ' + 
                str(year) + f'{month:02}'+ '...'
                  )
        
        time.sleep(random.randrange(1, 10))
    return res_list

def write(year, month, keyword):
    out = liberty_times(year, month, keyword)

    filename = keyword + '_' + str(year) + f'{month:02}' +'_at_' + str(datetime.datetime.today().strftime("%Y%m%d%H%M%S"))
        
    with open(f'./out/{filename}.csv', 'w', encoding='utf-8-sig') as f:
        write = csv.writer(f)
        write.writerows(out)
    return 


st = time.time()

write(2022,5,'中國')

# df = pd.DataFrame()
# for month in range(1, 13):
#     temp = liberty_times(2022, month, '中國')
#     df = pd.concat([df, temp], ignore_index=True)
# 
# filename = 'liberty_times_' + keyword + '_' + str(year)
# with open(f'./out/{filename}.csv', 'w', encoding='utf-8') as f:
#     write = csv.writer(f, dialect='excel')
#     write.writerows(df)

#############################################################################
############################### Merge CSVs ##################################
#############################################################################
files = os.listdir('out')
files.sort(reverse=True)

df = pd.DataFrame()
for i in range(0,len(files)):
    if files[i].split('.')[1] == 'csv':
       file = './out/'+ files[i]
       temp = pd.read_csv(file, encoding='utf-8', sep=',', index_col=0) 
       df = pd.concat([df, temp], ignore_index=True)

df.to_csv('./out/liberty_times_中國_2022.txt', sep=',', encoding='utf-8')

