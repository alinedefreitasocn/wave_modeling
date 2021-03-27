#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 07:37:59 2021

@author: aline

analisando periodo historico de indices

"""
import xarray as xr
from eofs.xarray import Eof
from calculaEOF import calcEOF
from reading_AO_index import read_index
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

mypath = '/home/aline/Documents/Dados/Jerry/GEOPOT_1000hPa/'

pseudo_pcs = xr.open_dataset(mypath + 'index_historical1.nc')

pseudo_pcs = pseudo_pcs.rename({'__xarray_dataarray_variable__':'indice'})

ppcs = pd.DataFrame(data=pseudo_pcs.indice.values, 
                    index=pseudo_pcs.time.values, 
                    columns=['pseudo_pcs'])
# f_ind = f_ind[0]
# f_ind = f_ind['1960-02-01':'2020-09-01']

# excluindo os 10 primeiros anos para obter o numero certo de climatologias
ppcs = ppcs['1970-01-01':'2100-12-31']

# merged = ppcs.merge(f_ind, on=ppcs.index)
# merged.index = merged['key_0']
# merged = merged.drop(columns='key_0')
# merged = merged.rename()
# merged = merged.rename(columns={'pseudo_pcs': 'CMIP5', 'id': 'NCEP'})

# estats = {'max': merged.max(),
#           'std': merged.std(),
#           'mean': merged.mean(),
#           'quantile': merged.quantile([0.95, 0.99])}


"""
PEGAR SERIE DO PPCS E SEPARAR EM PERIODOS DE 30 ANOS
60-90
91-2020
21-50
51-80
81-100
FAZER GRÁFICO DE MEDIA, DESVIO, MAX, QUANTILE AO LOGO DESSES PERIODOS

seaborn calcula regression line with confidence interval, drawn using
translucent bands around the regression line. the confidence interval is
estimated using a bootstrap
default ci is 95

resample(30YS):
    60-90
    90-20
    20-50
    50-80
    80-100
"""

medias = ppcs.resample('30YS').mean()
desvio = ppcs.resample('30YS').std()
maximos = ppcs.resample('30YS').max()
quantile95 = ppcs.resample('30YS').quantile(0.95)
quantile99 = ppcs.resample('30YS').quantile(0.99)


fig, axs = plt.subplots(3, sharex=True)
sns.regplot(medias.index.year, medias.values, ax=axs[0])
axs[0].grid()
axs[0].set_ylabel('30 yrs \n mean  ')
sns.regplot(desvio.index.year, desvio.values, ax=axs[1])
axs[1].grid()
axs[1].set_ylabel('30 yrs \n std')
sns.regplot(maximos.index.year, maximos.values, ax=axs[2])
axs[2].grid()
axs[2].set_ylabel('30 yrs \n max  ')
plt.suptitle('CMIP5 index projection')


fig3, axs = plt.subplots(2, sharex=True)
sns.regplot(quantile95.index.year, quantile95.values, ax=axs[0])
axs[0].grid()
axs[0].set_ylabel('30 yrs \n Q95  ')
sns.regplot(quantile99.index.year, quantile99.values, ax=axs[1])
axs[1].grid()
axs[1].set_ylabel('30 yrs \n Q99  ')
plt.suptitle('CMIP5 index projection')

# medias = [
#     ppcs['1960-01-01':'1990-12-31'].mean(),
#     ppcs['1991-01-01':'2020-12-31'].mean(),
#     ppcs['2021-01-01':'2050-12-31'].mean(),
#     ppcs['2051-01-01':'2080-12-31'].mean(),
#     ppcs['2081-01-01':'2100-12-31'].mean(),
#     ppcs['2070-01-01':'2100-12-31'].mean()
#     ]


# desvio = [
#     ppcs['1960-01-01':'1990-12-31'].std(),
#     ppcs['1991-01-01':'2020-12-31'].std(),
#     ppcs['2021-01-01':'2050-12-31'].std(),
#     ppcs['2051-01-01':'2080-12-31'].std(),
#     ppcs['2081-01-01':'2100-12-31'].std(),
#     ppcs['2070-01-01':'2100-12-31'].std()
#     ]


# maximos = [
#     ppcs['1960-01-01':'1990-12-31'].max(),
#     ppcs['1991-01-01':'2020-12-31'].max(),
#     ppcs['2021-01-01':'2050-12-31'].max(),
#     ppcs['2051-01-01':'2080-12-31'].max(),
#     ppcs['2081-01-01':'2100-12-31'].max(),
#     ppcs['2070-01-01':'2100-12-31'].max()
#     ]




# quantiles95 = [
#     ppcs['1960-01-01':'1990-12-31'].quantile([0.95]),
#     ppcs['1991-01-01':'2020-12-31'].quantile([0.95]),
#     ppcs['2021-01-01':'2050-12-31'].quantile([0.95]),
#     ppcs['2051-01-01':'2080-12-31'].quantile([0.95]),
#     ppcs['2081-01-01':'2100-12-31'].quantile([0.95]),
#     ppcs['2070-01-01':'2100-12-31'].quantile([0.95])
#     ]

# quantiles99 = [
#     ppcs['1960-01-01':'1990-12-31'].quantile([0.99]),
#     ppcs['1991-01-01':'2020-12-31'].quantile([0.99]),
#     ppcs['2021-01-01':'2050-12-31'].quantile([0.99]),
#     ppcs['2051-01-01':'2080-12-31'].quantile([0.99]),
#     ppcs['2081-01-01':'2100-12-31'].quantile([0.99]),
#     ppcs['2070-01-01':'2100-12-31'].quantile([0.99])




""" Outras analises temporais"""
media_anual = ppcs.groupby(by=ppcs.index.year).mean()
std_anual = ppcs.groupby(by=ppcs.index.year).std()
max_anual = ppcs.groupby(by=ppcs.index.year).max()
q95_anual = ppcs.groupby(by=ppcs.index.year).quantile(0.95)
q99_anual = ppcs.groupby(by=ppcs.index.year).quantile(0.99)


fig2, axs = plt.subplots(3, sharex=True)
sns.regplot(media_anual.index, media_anual.values, ax=axs[0])
axs[0].grid()
axs[0].set_ylabel('Annual \n mean  ')
sns.regplot(std_anual.index, std_anual.values, ax=axs[1])
axs[1].grid()
axs[1].set_ylabel('Annual \n std')
sns.regplot(max_anual.index, max_anual.values, ax=axs[2])
axs[2].grid()
axs[2].set_ylabel('Annual \n max  ')
plt.suptitle('CMIP5 index projection')


fig3, axs = plt.subplots(2, sharex=True)
sns.regplot(q95_anual.index, q95_anual.values, ax=axs[0])
axs[0].grid()
axs[0].set_ylabel('Annual \n Q95  ')
sns.regplot(q99_anual.index, q99_anual.values, ax=axs[1])
axs[1].grid()
axs[1].set_ylabel('Annual \n Q99  ')
plt.suptitle('CMIP5 index projection')


# seasonal analysis
# winter
wppcs = ppcs[ppcs.index.month.isin([1, 2, 12])]

wmedia_anual = wppcs.groupby(by=wppcs.index.year).mean()
wstd_anual = wppcs.groupby(by=wppcs.index.year).std()
wmax_anual = wppcs.groupby(by=wppcs.index.year).max()
wq95_anual = wppcs.groupby(by=wppcs.index.year).quantile(0.95)
wq99_anual = wppcs.groupby(by=wppcs.index.year).quantile(0.99)



fig2, axs = plt.subplots(3, sharex=True)
sns.regplot(wmedia_anual.index, wmedia_anual.values, ax=axs[0])
axs[0].grid()
axs[0].set_ylabel('Annual \n mean  ')
sns.regplot(wstd_anual.index, wstd_anual.values, ax=axs[1])
axs[1].grid()
axs[1].set_ylabel('Annual \n std')
sns.regplot(wmax_anual.index, wmax_anual.values, ax=axs[2])
axs[2].grid()
axs[2].set_ylabel('Annual \n max  ')
plt.suptitle('Winter CMIP5 index projection')


fig3, axs = plt.subplots(2, sharex=True)
sns.regplot(wq95_anual.index, wq95_anual.values, ax=axs[0])
axs[0].grid()
axs[0].set_ylabel('Annual \n Q95  ')
sns.regplot(wq99_anual.index, wq99_anual.values, ax=axs[1])
axs[1].grid()
axs[1].set_ylabel('Annual \n Q99  ')
plt.suptitle('Winter CMIP5 index projection')
