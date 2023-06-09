import csv
import pandas as pd
import os
import re
import requests
from bs4 import BeautifulSoup as bs
import time
import random

path = '/Users/chanhyuk/Documents/projects/china_taiwan/data/taiwan_chinatimes'
file_list=os.listdir(path)

file_list_csv=[file for file in file_list if file.endswith(".csv")] 
file_list_csv=[re.sub('\.csv', '', file) for file in file_list_csv] 

for file in file_list_csv:
    # file = file_list_csv[3]
    temp = pd.read_csv(f'{path}/{file}.csv', index_col=None)
    temp = temp.loc[temp.rel == 1,:]
    links = list(temp.link)

    content = list()
    i = 0
    for link in links:
        # link = links[0]
        i += 1
        res = requests.get(link)
        text = bs(res.text, 'html.parser')
        body = text.select('div.article-body p')
        body = ''.join(map(str,body))
        body = re.sub('<p>', '', body)
        body = re.sub('</p>', '', body)

        content.append(body)

        time.sleep(random.randrange(0,5))

        print(f'>>>> Link {i} is done!')

    content1 = pd.DataFrame(content,columns=['content']) 
    file2 = pd.concat([temp.reset_index(drop=True), content1.reset_index(drop=True)], axis=1)

    file2.to_csv(f'{path}/{file}(2).csv', index=False, encoding='utf-8-sig')
    print(f'<<<< File {file} is done!')
