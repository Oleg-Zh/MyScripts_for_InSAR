#!/usr/bin/python
import sys
import pathlib
from scipy.io import loadmat
import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime

# определение пути
currentDirectory = pathlib.Path('.')

# определение шаблона
currentPattern = "ps_plot_ts*.mat"

# конвертирование в формат csv
for inputfile in currentDirectory.glob(currentPattern):
    outputfile = str(inputfile)[:-3] + 'csv'
    ts = loadmat(inputfile)
    def from_mat_date(md):
        return str(date.fromordinal(int(md)) + timedelta(days=md%1) - timedelta(days = 366))

    columns_date = [(lambda i: from_mat_date(int(str(i))))(i) for i in ts['day'].flat]
    df = pd.DataFrame(ts['ph_mm'],columns=columns_date)
    dstat = pd.DataFrame()
    dstat['mean'] = df.apply(np.mean, axis=1)
    dstat['median'] = df.apply(np.median, axis=1)
    dstat['std'] = df.apply(np.std, axis=1)
    dstat['average'] = df.apply(np.average, axis=1)

    d0 = pd.concat([df, dstat], axis=1)

    columns = ['longitude', 'latitude']
    d1 = pd.DataFrame(ts['lonlat'], columns=columns)

    df = pd.concat([d1,d0], axis=1)
    df.to_csv(outputfile, index=False)
    print('File {} has been converting and writing to {}'.format(inputfile, outputfile))
