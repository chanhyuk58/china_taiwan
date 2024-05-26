import requests
# import csv
import json
import pandas as pd

id = ['sm8soRRSarMfOeldpuGO', '5lFGF1Evz9FOup32pqnc', 'OEWYTlF6f9vvEs37UQyK']
passwords = ['WsTyew7q9L', 'YpNAaPcf15', 'oHoytMg7g1']
# function: papago translate post requests
def papago(origianl, source_lang, target_lang, k):
    url = 'https://openapi.naver.com/v1/papago/n2mt'
    headers = {
        'Content-Type':'application/json',
        'X-Naver-Client-Id': id[k],
        'X-Naver-Client-Secret': passwords[k]
    }
    data = {
        'source':str(source_lang),
        'target':str(target_lang),
        'text':str(original)
    }
    res = requests.post(url, data = json.dumps(data), headers = headers)
    res_dict = res.json()
    output = res_dict['message']['result']['translatedText']
    return output

# load data
pro_china_nouns = pd.read_csv('../data/taiwan/nouns/pro_china_nouns.csv', names = ['chinese', 'count'], skiprows = 1)
tw_libertytimes_nouns = pd.read_csv('../data/taiwan/nouns/tw_libertytimes_nouns.csv', names = ['chinese', 'count'], skiprows = 1)
tw_nextapple_nouns = pd.read_csv('../data/taiwan/nouns/tw_nextapple_nouns.csv',names = ['chinese', 'count'], skiprows = 1)

# get the list of words without duplicates
nouns = pd.concat([pro_china_nouns, tw_libertytimes_nouns, tw_nextapple_nouns], ignore_index=True)
nouns = nouns.drop_duplicates(subset=['chinese'], ignore_index=True)
nouns['korean'] = 'NaN'
nouns['english'] = 'NaN'
nouns = nouns.drop(['count'], axis=1)

# generate translated list
nouns = pd.read_csv('../data/taiwan/nouns/translated/translated_full.csv', index_col=False)
output_ko = list(nouns['korean'].dropna())
output_en = list(nouns['english'].dropna())
n = 0
for i in range(len(nouns)):
    if pd.isna(nouns.loc[i, 'english']):
        if n <= 10000:
            k = 0
        elif n <= 20000:
            k = 1
        elif n <= 30000:
            k = 2
        else:
            break
        original = nouns['chinese'][i]
        output_ko = output_ko + [papago(original, 'zh-TW', 'ko', k)]
        output_en = output_en + [papago(original, 'zh-TW', 'en', k)]
        n += 2
    print(f'{i + 1} of {len(nouns)} has been done!' + f' | n = {n}')
nouns['korean'] = pd.Series(output_ko)
nouns['english'] = pd.Series(output_en)
nouns.to_csv('../data/taiwan/nouns/translated/translated_full.csv', encoding='utf-8-sig', index=False)

# merge and save
pro_china_nouns_trans = pro_china_nouns.merge(nouns, how='left', on = 'chinese')
pro_china_nouns_trans.to_csv('../data/taiwan/nouns/translated/pro_china_nouns_translated.csv', encoding = 'utf-8-sig', index=False)

tw_libertytimes_nouns_trans = tw_libertytimes_nouns.merge(nouns, how='left', on = 'chinese')
tw_libertytimes_nouns_trans.to_csv('../data/taiwan/nouns/translated/tw_libertytimes_nouns_translated.csv', encoding = 'utf-8-sig', index=False)

tw_nextapple_nouns_trans = tw_nextapple_nouns.merge(nouns, how='left', on = 'chinese')
tw_nextapple_nouns_trans.to_csv('../data/taiwan/nouns/translated/tw_nextapple_nouns_translated.csv', encoding = 'utf-8-sig', index=False)
