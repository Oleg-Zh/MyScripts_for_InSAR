#!/usr/bin/env python3
# OlegZh 16.02.2022

import os
import numpy as np
import pandas as pd

output_file = 'xy.csv'
# Создание списка с датами
fname = 'date.txt' # файл с датами интерферограмм
if os.path.exists(fname):
    try:
        f_date = open(fname, 'r')
        columns_date = list(map(lambda s: (s.strip().replace('.','')[:8]), (f_date.readlines())))
    finally:
        f_date.close()
else:
    print(f'Файл с датами <{fname}> отсутствует!')
    print('Этот скрипт надо запускать в каталоге с файлами *.xy')
    exit(1)

for i, name_column in enumerate(columns_date):
    i +=1
    fname = f'ps_u-dm.{i}.xy' #Перебор файлов с даннными
    print(f'Обработка файла {fname}')
    if os.path.exists(fname):
        try:
            f_data = open(fname, 'r')
            data = list(map(lambda s: (s.split()), (f_data.readlines())))
        finally:
            f_data.close()
    else:
        print(f'Файл с данными <{fname}> отсутствует!')
        os.exit(1)
    if i == 1: #Создание DataFrame и колонок с координатными данными
        col_tmp = []
        for i in data:
            col_tmp.append(float(i[0]))
        df = pd.DataFrame(col_tmp, columns=['Longitude'])
        col_tmp = []
        for i in data:
            col_tmp.append(float(i[1]))
        df['Latitude'] = col_tmp
    col_tmp = []
    for i in data:
        col_tmp.append(float(i[2]))
    df[name_column] = col_tmp

fname = 'ps_mean_v.xy'
if os.path.exists(fname):
    try:
        f_data = open(fname, 'r')
        data = list(map(lambda s: (s.split()), (f_data.readlines())))
    finally:
        f_date.close()
else:
    print(f'Файл со средними значениями <{fname}> отсутствует!')
    os.exit(1)
col_tmp = []
for i in data:
    col_tmp.append(float(i[2]))
df[fname[:-3]] = col_tmp

fname = 'dem_error.xy'
if os.path.exists(fname):
    try:
        f_data = open(fname, 'r')
        data = list(map(lambda s: (s.split()), (f_data.readlines())))
    finally:
        f_date.close()
else:
    print(f'Файл <{fname}> отсутствует!')
    os.exit(1)
col_tmp = []
for i in data:
    col_tmp.append(float(i[2]))
df[fname[:-3]] = col_tmp

#df['mean'] = df.loc[:,columns_date].apply(np.mean, axis=1)
#df['median'] = df.loc[:,columns_date].apply(np.median, axis=1)
#df['std'] = df.loc[:,columns_date].apply(np.std, axis=1)
#df['average'] = df.loc[:,columns_date].apply(np.average, axis=1)

print('Идет запись результатов...')
df.to_csv(output_file, index=False)
print(f'Записан файл {output_file}')

