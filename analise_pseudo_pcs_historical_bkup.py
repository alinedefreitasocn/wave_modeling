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
from scipy import stats

# defining month names for plots
meses = ['' , 'Jan', 'Feb', 'Mar', 'Apr', 
         'May', 'Jun', 'Jul', 'Aug', 'Sep',
         'Oct', 'Nov', 'Dec']

# separating by season
month_num_to_season =   { 1:'DJF',  2:'DJF', 
                          3:'MAM',  4:'MAM',  5:'MAM', 
                          6:'JJA',  7:'JJA',  8:'JJA',
                          9:'SON', 10:'SON', 11:'SON',
                         12:'DJF'}
unique_season = set(month_num_to_season.values())


# pasta para salvar os arquivos
mypath = '/home/aline/Documents/Dados/Jerry/GEOPOT_1000hPa/'

# indice historico calculado a partir da pressao atmosferica do CMIP5
pseudo_pcs = xr.open_dataset(mypath + 'index_historical1.nc')

# transformacao do objeto
pseudo_pcs = pseudo_pcs.rename({'__xarray_dataarray_variable__':'indice'})
ppcs = pd.DataFrame(data=pseudo_pcs.indice.values, 
                    index=pseudo_pcs.time.values, 
                    columns=['pseudo_pcs'])

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



mensal_completo = ppcs.groupby(ppcs.index.month)

##########################################################
# AVALIACAO MENSAL DOS MESES DE INVERNO
# slope, intercept, r_value, p_value, slope_std_error = stats.linregress(dezembro)

# selecionar um periodo de 30 anos do era5 e comparra com os mesmos
# 30 anos do cmip5. fazer os histogramas mensais com o matplotlib
# e ver se funciona. depois comparar o momento atual do cmip com 30 anos 
# do fim do seculo

# Reading ERA5 index
findex = '/home/aline/Documents/Dados/indices/calculados/index_era5.txt'
indices = pd.read_csv(findex, 
                  header=0,
                  parse_dates=True,
                  index_col='time',
                  names=['time', 'id'])

# Dividindo as series por meses
# cmip eh o indice gerado pelo cenario futuro, porem no periodo atual
# para ser possivel de comparar com o ERA5
mensal_futuro = ppcs['2070-01-01':'2100-12-01'].groupby(
    ppcs['2070-01-01':'2100-12-01'].index.month)

# selecionando o mesmo periodo pro cmip e era 5
mensal_cmip = ppcs['1979-01-01':'2009-12-01'].groupby(
    ppcs['1979-01-01':'2009-12-01'].index.month)
mensal_era = indices['1979-01-01':'2009-12-01'].groupby(
    indices['1979-01-01':'2009-12-01'].index.month)

"""density : bool, default: False
    If ``True``, draw and return a probability density: each bin
    will display the bin's raw count divided by the total number of
    counts *and the bin width*
    (``density = counts / (sum(counts) * np.diff(bins))``),
    so that the area under the histogram integrates to 1
    (``np.sum(density * np.diff(bins)) == 1``)."""

b = np.arange(-4, 4, 0.8)
m=1
for i in range(3):
    fig, axs = plt.subplots(2, 2, sharex=True, sharey=True)
    for j in range(4):
        print('Iniciando mes: ' + str(m))
        ax = plt.subplot(2, 2, j+1)
        plt.hist(mensal_cmip.get_group(m),
                     density = True,
                     alpha = 0.5,
                     color ='turquoise',
                     bins = b,
                     label='CMIP5')
        plt.hist(mensal_era.get_group(m), 
                      density = True,
                      alpha = 0.5,
                      color ='lightsalmon',
                      bins = b,
                      label='ERA5')
        plt.hist(mensal_futuro.get_group(m), 
                      density = True,
                      color ='k',
                      bins = b,
                      label='Future',
                      histtype='step')
        plt.ylim([0,1])
        plt.xlim([-4,4])
        plt.title(meses[m])
        plt.grid(':', alpha=0.5)
        if j in (0,2):
            plt.ylabel('Probability Density')
        else:
            plt.setp(ax.get_yticklabels(), visible=False)
        if j in (2, 3):
            plt.xlabel('AO Index')
        else:
            plt.setp(ax.get_xticklabels(), visible=False)
        
        m += 1
    fig.legend(bbox_to_anchor=(0.9, 1), 
               labels=['CMIP5', 'ERA5', 'Future'], 
               loc='upper right', 
               ncol=3)
    plt.suptitle('Present Index   1979 - 2009')


s = {key: None for key in meses}
r = {key: None for key in meses}
p = {key: None for key in meses}

# Two-sided p-value for a hypothesis test whose null hypothesis is
#     that the slope is zero, using Wald Test with t-distribution of
#     the test statistic.
for m in range(1, 13, 1):
    # plt.figure()
    # sns.regplot(x= mensal_completo.get_group(m).index.year,
    # y = mensal_completo.get_group(m).values)
    # plt.title(meses[m])
    # plt.grid()
    # plt.ylabel('AO Index')
    # figure = plt.gcf()
    # figure.set_size_inches(120, 15)
    # plt.savefig('/home/aline/Dropbox/IST_investigation/Teleconnections/Future/' +
    #             meses[m] + 'png', dpi=200)
    # plt.close()
    slope, intercept, r_value, p_value, std_err = stats.linregress(mensal_completo.get_group(m).index.year,
                                                                   np.concatenate([np.array(i) for i in mensal_completo.get_group(m).values]))
    # a, b = np.polyfit(mensal_completo.get_group(m).index.year, 
    #                   mensal_completo.get_group(m).values, 
    #                   1)
    s[meses[m]] = slope.round(4)
    r[meses[m]] = r_value.round(4)
    p[meses[m]] = p_value.round(4)




# grouping CMIP by season 
grouped_cmip =  ppcs.groupby(lambda x: month_num_to_season.get(x.month)) 


s2 = {key: None for key in uniqueValues}
r2 = {key: None for key in uniqueValues}
p2 = {key: None for key in uniqueValues}

for season in uniqueValues:
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        grouped_cmip.get_group(season).index.year,
        np.concatenate([np.array(i) for i in grouped_cmip.
                        get_group(season).values]))
    s2[season] = slope.round(4)
    r2[season] = r_value.round(4)
    p2[season] = p_value.round(4)


# m=1
# for i in range(3):
#     fig, axs = plt.subplots(2, 2, sharex=True, sharey=True)
#     for j in range(4):
#         print('Iniciando mes: ' + str(m))
#         plt.subplot(2, 2, j+1)
#         plt.hist(mensal_cmip.get_group(m),
#                      density = True,
#                      alpha = 0.5,
#                      color ='purple',
#                      bins = b,
#                      label='Present')
#         plt.hist(mensal_futuro.get_group(m), 
#                       density = True,
#                       alpha = 0.5,
#                       color ='gold',
#                       bins = b,
#                       label='Future')
#         plt.ylim([0,1])
#         plt.xlim([-4,4])
#         plt.title(meses[m])
#         plt.grid(':', alpha=0.5)
        
#         m += 1
    
#     plt.ylabel('Probability Density')
#     plt.xlabel('AO Index')
#     fig.legend(labels=['Present', 'Future'], loc='upper right', ncol=2)
#     plt.suptitle('CMIP5 Index Projection')








# dezembro = ppcs[ppcs.index.month == 12]
# cmip_dez = ppcs_now[ppcs_now.index.month == 12]
# era_dez = indices[indices.index.month == 12]

# janeiro = ppcs[ppcs.index.month == 1]
# era_jan = indices[indices.index.month == 1]
# cmip_jan = ppcs_now[ppcs_now.index.month == 1]

# fevereiro = ppcs[ppcs.index.month == 2]
# era_fev = indices[indices.index.month == 2]
# cmip_fev = ppcs_now[ppcs_now.index.month == 2]

# mar = ppcs[ppcs.index.month == 3]
# era_mar = indices[indices.index.month == 3]
# cmip_mar = ppcs_now[ppcs_now.index.month == 3]


# abr = ppcs[ppcs.index.month == 4]
# mai = ppcs[ppcs.index.month == 5]
# jun = ppcs[ppcs.index.month == 6]
# jul = ppcs[ppcs.index.month == 7]

# ago = ppcs[ppcs.index.month == 8]
# sete = ppcs[ppcs.index.month == 9]
# out = ppcs[ppcs.index.month == 10]
# nov = ppcs[ppcs.index.month == 11]




# fig, axs = plt.subplots(4, sharex=True, sharey=True)
# sns.regplot(mensal_futuro.get_group(12).index.year, 
#             mensal_futuro.get_group(12).values, ax=axs[0])
# axs[0].set_title('December')
# sns.regplot(janeiro.index.year, janeiro.values, ax=axs[1])
# axs[1].set_title('January')
# sns.regplot(fevereiro.index.year, fevereiro.values, ax=axs[2])
# axs[2].set_title('February')
# sns.regplot(mar.index.year, mar.values, ax=axs[3])
# axs[3].set_title('March')
# axs[0].set_ylim([-5,5])

# fig, axs = plt.subplots(4, sharex=True, sharey=True)
# sns.regplot(abr.index.year, abr.values, ax=axs[0])
# axs[0].set_title('April')
# sns.regplot(mai.index.year, mai.values, ax=axs[1])
# axs[1].set_title('May')
# sns.regplot(jun.index.year, jun.values, ax=axs[2])
# axs[2].set_title('June')
# sns.regplot(jul.index.year, jul.values, ax=axs[3])
# axs[3].set_title('July')
# axs[0].set_ylim([-5,5])

# fig, axs = plt.subplots(2, 2, sharex=True, sharey= True)
# sns.histplot(mensal_ppcs.get_group(12), ax=axs[0,0], 
#              legend=False, 
#              kde=True, 
#              bins=10, 
#              alpha=0.5,
#              stat='probability',
#              element='step')
# # sns.histplot(era_dez, ax=axs[0,0], 
# #              legend=False, 
# #              bins=10, 
# #              alpha=0.5,
# #              stat='probability',
# #              element='step',
# #              color='DarkRed')
# axs[0,0].set_title('December')
# sns.histplot(janeiro, ax=axs[0,1], 
#              legend=False, kde=True, 
#              bins=10, stat='frequency')
# axs[0,1].set_title('January')
# sns.histplot(fevereiro, ax=axs[1,0], 
#              legend=False, kde=True, 
#              bins=10, stat='frequency')
# axs[1,0].set_title('February')
# sns.histplot(mar, ax=axs[1,1], 
#              legend=False, 
#              kde=True, 
#              bins=10, stat='frequency')
# axs[1,1].set_title('March')
# axs[1,1].set_xlim([-5,5])







# fig, axs = plt.subplots(2, 2, sharex=True, sharey= True)
# sns.histplot(abr, ax=axs[0,0], 
#              legend=False, kde=True, 
#              bins=10, stat='frequency')
# axs[0,0].set_title('April')
# sns.histplot(mai, ax=axs[0,1], 
#              legend=False, kde=True, 
#              bins=10, stat='frequency')
# axs[0,1].set_title('May')
# sns.histplot(jun, ax=axs[1,0], 
#              legend=False, kde=True, 
#              bins=10, stat='frequency')
# axs[1,0].set_title('June')
# sns.histplot(jul, ax=axs[1,1], 
#              legend=False, kde=True, 
#              bins=10, stat='frequency')
# axs[1,1].set_title('July')
# axs[1,1].set_xlim([-5,5])




# fig, axs = plt.subplots(2, 2, sharex=True, sharey= True)
# sns.histplot(ago, ax=axs[0,0], 
#              legend=False, kde=True, 
#              bins=10, stat='frequency')
# axs[0,0].set_title('August')
# sns.histplot(sete, ax=axs[0,1], 
#              legend=False, kde=True, 
#              bins=10, stat='frequency')
# axs[0,1].set_title('September')
# sns.histplot(out, ax=axs[1,0], 
#              legend=False, kde=True, 
#              bins=10, stat='frequency')
# axs[1,0].set_title('October')
# sns.histplot(nov, ax=axs[1,1], 
#              legend=False, kde=True, 
#              bins=10, stat='frequency')
# axs[1,1].set_title('November')
# axs[1,1].set_xlim([-5,5])