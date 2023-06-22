import csv
import pandas as pd
import os
import re
import requests
from bs4 import BeautifulSoup as bs
import time
import random
import glob

############################## Chinatimes ##############################
def chinatimes(limit):
    path = '../data/tw_chinatimes/'
    file_list = glob.glob(f'{path}*_[0-9][0-9].csv')

    cnt = 0
    for file in file_list:
        temp = pd.read_csv(file, index_col=None)
        
        for i in range(0,len(temp)):
            if cnt >= limit:
                break
                break
            else:
                if pd.isnull(temp.at[i, 'content']):
                    cnt += 1
                    link = temp.at[i, 'link']
                    res = requests.get(link)
                    text = bs(res.text, 'html.parser')
                    body = text.select('div.article-body p')
                    body = ''.join(map(str,body))
                    body = re.sub('<p>', '', body)
                    body = re.sub('</p>', '', body)
            
                    temp.at[i, 'content'] = body
            
                    print(f'>>>> Link {cnt} is done!')
                    time.sleep(random.randrange(0,2))
        
        temp.to_csv(file, index=False, encoding='utf-8-sig')
        print(f'<<<< File {file} is on!')
    return print('>>> Chinatimes is done!!! <<<')

############################## Libertytimes ###########################

def libertytimes(limit):
    path = '../data/tw_libertytimes/'
    file_list = glob.glob(f'{path}*_[0-9][0-9].csv')

    cnt = 0
    for file in file_list:
        temp = pd.read_csv(file, index_col=None)
        
        for i in range(0,len(temp)):
            if cnt >= limit:
                break
                break
            else:
                if pd.isnull(temp.at[i, 'content']):
                    cnt += 1
                    link = temp.at[i, 'link']
                    res = requests.get(link)
                    text = bs(res.text, 'html.parser')
                    body = text.select(
                        'div.content div.text p:not(.appE1121,p:has(a[title*=點我訂閱自由財經Youtube頻道]))'
                    )
                    body2 = text.select('div.content div.text p')
                    body = ''.join([sentence.text for sentence in body])
                    temp.at[i, 'content'] = body
            
                    print(f'>>>> Link {cnt} is done!')
                    time.sleep(random.randrange(0,2))
        
        print(f'<<<< File {file} is on!')
        temp.to_csv(file, index=False, encoding='utf-8-sig')
    return print('>>> Libertytimes is done!!! <<<')

############################## Nextapple ##############################

def nextapple(limit):
    path = '../data/tw_nextapple/'
    file_list = glob.glob(f'{path}*_[0-9][0-9].csv')

    cnt = 0
    for file in file_list:
        temp = pd.read_csv(file, index_col=None)
        
        for i in range(0,len(temp)):
            if cnt >= limit:
                break
                break
            else:
                if pd.isnull(temp.at[i, 'content']):
                    cnt += 1
                    link = temp.at[i, 'link']
                    res = requests.get(link)
                    text = bs(res.text, 'html.parser')
                    body = text.select('div.post-content p')
                    body = ''.join([sentence.text for sentence in body])
                    body = re.sub('\n|\r', '', body)
                    temp.at[i, 'content'] = body
            
                    print(f'>>>> Link {cnt} is done!')
                    time.sleep(random.randrange(0,2))
        
        print(f'<<<< File {file} is on!')
        temp.to_csv(file, index=False, encoding='utf-8-sig')
    return print('>>> Nextapple is done!!! <<<')

############################## udn #################################

def udn(limit):
    path = '../data/tw_udn/'
    file_list = glob.glob(f'{path}*_[0-9][0-9].csv')

    cnt = 0
    for file in file_list:
        temp = pd.read_csv(file, index_col=None)
        
        for i in range(0,len(temp)):
            if cnt >= limit:
                break
                break
            else:
                if pd.isnull(temp.at[i, 'content']):
                    cnt += 1
                    link = temp.at[i, 'link']

                    res = requests.get(link)
                    text = bs(res.text, 'html.parser')
                    body = text.select(
                        'section.article-content__paragraph p, div#container p'
                    )
                    body = ''.join([sentence.text for sentence in body])
                    body = re.sub('\n|\r', '', body)

                    temp.at[i, 'content'] = body
            
                    print(f'>>>> Link {cnt} is done!')
                    time.sleep(random.randrange(0,2))
        print(f'<<<< File {file} is on!')
        temp.to_csv(file, index=False, encoding='utf-8-sig')
        
    return print('>>> udn is done!!! <<<')

################################ Loop ################################

for i in range(0,5):
    # chinatimes(100)
    libertytimes(100)
    # nextapple(100)
    udn(100)
