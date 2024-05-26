import os
import glob
import pandas
import re
import csv

file_list = glob.glob(os.path.join('*.csv'))

for file in file_list:
    # file = file_list[0]
    read = open(file, 'r')
    reader = read.read()
    csvRe = re.sub(r'(<.[a-z]+>)+', '', str(reader))
    write = open(file, 'w')
    write.write(csvRe)
    read.close()
    write.close()
