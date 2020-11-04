#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Aline Lemos de Freitas
15 de setembro de 2020

4 de novembro

Reading NAO index
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import matplotlib.dates as mdates

file = '/home/aline/Documents/IST_investigation/Teleconnections/AO_index.txt'

f = pd.read_csv(file, sep='\s+',
                names=['year', 'month', 'id'],
                header=2,
                parse_dates={'datetime':[0, 1]},
                index_col='datetime'
                )
f_sel=f[f.index.year > 1988]



fig, ax = plt.subplots()
ax.bar(f_sel[f_sel.id > 0].index,
        f_sel[f_sel.id > 0].id,
        width=10)
# ax.bar(negativo.index,
#        negativo.id,
#        color='DarkRed', width=10)
ax.bar(f_sel[f_sel.id < 0].index,
         f_sel[f_sel.id < 0].id,
         color='DarkRed',
         width=10)
plt.title('Arctic Oscillation Index - NOAA')
plt.autoscale(enable=True, axis='x', tight=True)
plt.grid('--', alpha=0.6)
plt.ylim(-4.5, 4.5)
plt.show(block=False)
