import pandas as pd
import os
import re
import openpyxl
import xlrd

path='/Users/chanhyuk/Downloads/taiwan/libertytimes'
file_list=os.listdir(path)

file_list_csv=[file for file in file_list if file.endswith(".xls")] 
file_list_csv=[re.sub('\.xls', '', file) for file in file_list_csv] 

for file in file_list_csv:
    test = pd.read_excel(f'{path}/{file}.xls')
    test = test.iloc[:, 0:8]
    test.columns = ['relsub', 'relsum', 'rel', 'index', 'title', 'date',
                    'summary', 'link']
    
    test.to_csv(
        f'/Users/chanhyuk/Documents/projects/china_taiwan/data/taiwan_libertytimes/{file}.csv', encoding='utf-8-sig', index=False
    )

