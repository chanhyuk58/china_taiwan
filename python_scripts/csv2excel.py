import pandas as pd
import os
import re
# import openpyxl
# import xlrd
import glob
import csv
# import datetime

path = '../data'
target = 'tw_chinatimes'
file_list = glob.glob(f'{path}/{target}/*.csv')
# file_name_list=[re.sub('\.csv', '', file) for file in file_list] 

df_all = pd.DataFrame(columns=['title', 'date', 'summary', 'link', 'content'])
for file in file_list:
    temp = pd.read_csv(file)
    temp = temp.loc[temp.rel == 1,['title', 'date', 'summary', 'link']]

    df_all = pd.concat([df_all.reset_index(drop=True), temp.reset_index(drop=True)], axis=0)
    df_all = df_all.drop_duplicates()
    df_all.date = pd.to_datetime(df_all.date, format='mixed')
    df_all = df_all.sort_values('date')
    # df_all = df_all.loc[
    # ('2021-12-31' < df_all.date) & (df_all.date < '2023-01-01'), :
    # ]

# df_all.to_csv(f'{path}/{target}/{target}_all.csv', index=False)

# df_all = pd.read_csv(f'{path}/{target}/{target}_all.csv')
df_all.date = pd.to_datetime(df_all.date)

for month in range(1,13):
    df_month = df_all.loc[df_all.date.dt.month == month,:]
    df_month.to_csv(f'{path}/{target}/{target}_{month:02d}.csv', encoding='utf-8-sig', index=False)
