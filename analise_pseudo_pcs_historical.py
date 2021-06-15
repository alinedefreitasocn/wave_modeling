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

#############################################################################
#############################################################################
##                      DEFINICAO DE VARIAVEIS
#############################################################################

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
unique_season = list(set(month_num_to_season.values()))

#############################################################################
#############################################################################
##                      LEITURA DE ARQUIVOS
#############################################################################
# pasta para salvar os arquivos
mypath = '/home/aline/Documents/Dados/Jerry/GEOPOT_1000hPa/'

# indice historico calculado a partir da pressao atmosferica do CMIP5
pseudo_pcs = xr.open_dataset(mypath + 'index_historical1.nc')

# Reading ERA5 index
findex = '/home/aline/Documents/Dados/indices/calculados/index_era5.txt'
indices = pd.read_csv(findex, 
                  header=0,
                  parse_dates=True,
                  index_col='time',
                  names=['time', 'id'])

#############################################################################
#############################################################################
##                      MANIPULACAO VARIAVEIS
#############################################################################
# transformacao do objeto
pseudo_pcs = pseudo_pcs.rename({'__xarray_dataarray_variable__':'indice'})
ppcs = pd.DataFrame(data=pseudo_pcs.indice.values, 
                    index=pseudo_pcs.time.values, 
                    columns=['pseudo_pcs'])

# excluindo os 10 primeiros anos para obter o numero certo de climatologias
ppcs = ppcs['1980-01-01':'2100-12-31']
mensal_completo = ppcs.groupby(ppcs.index.month)

cmip_presente = ppcs['1990-01-01':'2020-12-01']
era_presente = indices['1990-01-01':'2020-12-01']
cmip_futuro = ppcs['2070-01-01':'2100-12-01']


negatives = ppcs[ppcs < 0]
positives = ppcs[ppcs >= 0]

##########################################################
# AVALIACAO MENSAL DOS MESES DE INVERNO
# slope, intercept, r_value, p_value, slope_std_error = stats.linregress(dezembro)

# selecionar um periodo de 30 anos do era5 e comparra com os mesmos
# 30 anos do cmip5. fazer os histogramas mensais com o matplotlib
# e ver se funciona. depois comparar o momento atual do cmip com 30 anos 
# do fim do seculo

# Dividindo as series por meses
# cmip eh o indice gerado pelo cenario futuro, porem no periodo atual
# para ser possivel de comparar com o ERA5
mensal_futuro = cmip_futuro.groupby(cmip_futuro.index.month)

# selecionando o mesmo periodo pro cmip e era 5
# PARA FAZER OS HISTOGRAMAS MENSAIS
mensal_cmip = cmip_presente.groupby(cmip_presente.index.month)
mensal_era = era_presente.groupby(era_presente.index.month)

# grouping CMIP e ERA by season 
grouped_cmip_season =  cmip_presente.groupby(lambda x: month_num_to_season.get(x.month)) 
grouped_era_season = era_presente.groupby(lambda x: month_num_to_season.get(x.month)) 
grouped_futuro_season = cmip_futuro.groupby(lambda x: month_num_to_season.get(x.month)) 
grouped_completo_season = ppcs.groupby(lambda x: month_num_to_season.get(x.month))

grouped_negatives_season = negatives.groupby(lambda x: month_num_to_season.get(x.month))

"""
PEGAR SERIE DO PPCS E SEPARAR EM PERIODOS DE 30 ANOS
1981-2010
2011-2040
2041-2070
2071-2100
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
#############################################################################
#############################################################################
##                           ESTATISTICAS 30 ANOS

medias = ppcs.resample('30YS').mean()
desvio = ppcs.resample('30YS').std()
maximos = ppcs.resample('30YS').max()
minimos = ppcs.resample('30YS').min()
variancia = ppcs.resample('30YS').var()
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

#############################################################################
#############################################################################
##                        """ Outras analises temporais"""

# POR ANO
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

#############################################################################
#############################################################################
##                        INVERNO
## extended winter
# wppcs = ppcs[ppcs.index.month.isin([1, 2, 3, 11, 12])]
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



#############################################################################
#############################################################################
##                        HISTOGRAMAS

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



#############################################################################
#############################################################################
##                        HISTOGRAMAS SAZONAL

unique_season.sort()
b = np.arange(-4, 4, 0.8)

fig, axs = plt.subplots(2, 2, sharex=True, sharey=True)
for j in range(4):
    ax = plt.subplot(2, 2, j+1)
    print('Iniciando SEASON: ' + unique_season[j])
    plt.hist(grouped_cmip_season.get_group(unique_season[j]),
                 density = True,
                 alpha = 0.5,
                 facecolor ='turquoise',
                 bins = b,
                 label='CMIP5',
                 #hatch='//',
                 edgecolor='k',
                 linewidth=0.5)
    plt.hist(grouped_era_season.get_group(unique_season[j]), 
                  density = True,
                  alpha = 0.5,
                  facecolor ='lightsalmon',
                  bins = b,
                  label='ERA5',
                  #hatch='--',
                  edgecolor='k',
                  linewidth=0.5)
    plt.hist(grouped_futuro_season.get_group(unique_season[j]), 
                  density = True,
                  color ='k',
                  bins = b,
                  label='Future',
                  histtype='step')
    plt.ylim([0,1])
    plt.xlim([-4,4])
    plt.title(unique_season[j])
    plt.grid(':', alpha=0.5)
    if j in (0,2):
        plt.ylabel('Probability Density')
    else:
        plt.setp(ax.get_yticklabels(), visible=False)
    if j in (2, 3):
        plt.xlabel('AO Index')
    else:
        plt.setp(ax.get_xticklabels(), visible=False)

    plt.legend(# bbox_to_anchor=(0.9, 1), 
               labels=['CMIP5 Present', 'ERA5', 'CMIP5 Future'], 
               loc='upper right', 
               ncol=3)
# plt.suptitle('Present Index   1979 - 2009')


#############################################################################
#############################################################################
##                  REGRESSOES MENSAIS

# calculando as regressoes, com o r2 e o p-value
# para os valores mensais do CMIP
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



#############################################################################
#############################################################################
##                  REGRESSOES SAZONAIS


s2 = {key: None for key in unique_season}
r2 = {key: None for key in unique_season}
p2 = {key: None for key in unique_season}

for season in unique_season:
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        grouped_completo_season.get_group(season).index.year,
        np.concatenate([np.array(i) for i in grouped_completo_season.
                        get_group(season).values]))
    s2[season] = slope.round(4)
    r2[season] = r_value.round(4)
    p2[season] = p_value.round(4)

#############################################################################
#############################################################################
##  
#                   separando positivos de negativos
sn = {key: None for key in unique_season}
rn = {key: None for key in unique_season}
pn = {key: None for key in unique_season}

for season in unique_season:
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        grouped_negatives_season.get_group(season).dropna().index.year,
        np.concatenate([np.array(i) for i in grouped_negatives_season.
                        get_group(season).dropna().values]))
    sn[season] = slope.round(4)
    rn[season] = r_value.round(4)
    pn[season] = p_value.round(4)
    
    
#############################################################################
#############################################################################
##  
#                   Regressao dados completos

slope, intercept, r_value, p_value, std_err = stats.linregress(
        ppcs.index.year,
        np.concatenate([np.array(i) for i in ppcs.values]))