#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 22 11:39:42 2021

@author: aline

Fazeno passo a passo para correlacionar o indice e Hs do era5 para 
comparar com o cmip5
"""

import xarray as xr
from cfgrib import xarray_store
import cfgrib
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import cartopy.crs as ccrs
import numpy as np
from faz_figuras import *
from xskillscore import pearson_r
from reading_AO_index import *

# clevs = np.arange(-1, 1.1, 0.1)
clevs = np.linspace(-1, 1, 21)
colormap = plt.cm.Spectral

# significancias estatisticas de pearson
# para dados no inverno, 30 pontos independentes
n30_95 = 0.3610 #95%
n30_90 = 0.3060
n30_80 = 0.2407

# para year-round data
n100_95 = 0.1946 #95%
n100_90 = 0.1638
n100_80 = 0.1279

# modelo = 'ERA5'
modelo = 'CMIP5'

tempo = 'presente' 
# tempo = 'futuro'

parametro = 'swh'
parametro = 'mwd'
parametro = 'WND'
parametro = 'mwp'

pseudo_pcs, dwave = le_indice_onda(modelo, tempo, parametro)

# if modelo == 'ERA5':
#     '''
#     REading index file
#     for index as txt
#     '''
#     findex = '/home/aline/Documents/Dados/indices/calculados/index_era5.txt'
#     pseudo_pcs = pd.read_csv(findex, 
#                       header=0,
#                       parse_dates=True,
#                       index_col='time',
#                       names=['time', 'indice'])
    
#     # selecionando 30 anos do ERA5 que representa o tempo presente: 
#     # de 1980 a 2020
#     # reading wave file
#     fwave = '/home/aline/Documents/Dados/ERA5/montly_mean_1979_2020.grib'
#     dwave = cfgrib.open_datasets(fwave)[0]
#     dwave = dwave.sel(time=slice('1990-01-01','2020-12-01'),
#                       latitude=slice(90,20), 
#                       longitude= slice(-101,  35))
# elif modelo == 'CMIP5':
#     indexpath = '/home/aline/Documents/Dados/Jerry/GEOPOT_1000hPa/'
#     if tempo == 'presente':
#         mypath = '/home/aline/Documents/Dados/Jerry/WW3_Marta/Presente/'
#         #mypath = '/home/aline/Documents/Dados/Jerry/WW3_Marta/Futuro/'
#         fwave = mypath + 'presente_hs_mean_mensal2.nc'
#         #fwave = mypath + 'futuro_hs_mean_mensal2.nc'
#     elif tempo == 'futuro':
#         mypath = '/home/aline/Documents/Dados/Jerry/WW3_Marta/Futuro/'
#         fwave = mypath + 'futuro_hs_mean_mensal2.nc'
#     dwave = xr.open_dataset(fwave).rename({'hs':'swh'})
    
#     pseudo_pcs = xr.open_dataset(indexpath + 'index_historical1.nc')
    
#     pseudo_pcs = pseudo_pcs.rename({'__xarray_dataarray_variable__':'indice'})
#     pseudo_pcs = pd.DataFrame(data=pseudo_pcs.indice.values, 
#                         index=pseudo_pcs.time.values, 
#                         columns=['indice'])
#     # precisei fazer essas transformacoes para calcular a correlacao
#     # nao estava identificando a dimensao time na serie ppcs (estava como index)
#     # e nao sei por qual motivo estava com algumas medias mensais com o 
#     # indice no segundo dia do mes...
#     datetime_indices = {'YEAR': pseudo_pcs.index.year, 
#                         'MONTH': pseudo_pcs.index.month,
#                         'DAY': np.ones(len(pseudo_pcs), dtype=int)}
#     pseudo_pcs.index = pd.to_datetime(datetime_indices)
#     pseudo_pcs.index.name = 'time'
    

# recortando para que o indice tenha a mesma serie temporal do 
# modelo de ondas  
# ppcs = pseudo_pcs[slice(dwave.isel(time=0).time.values, 
#                             dwave.isel(time=-1).time.values)]
# ppcs = pseudo_pcs[slice('1980-01-01', 
#                             '2009-12-01')]
ppcs = pseudo_pcs[slice('2070-01-01', 
                             '2099-12-01')]
# pseudo_pcs = pseudo_pcs[slice(dwave.isel(time=0).time.values, 
#                             dwave.isel(time=-1).time.values)].to_xarray()
# pseudo_pcs = pseudo_pcs[slice('1980-01-01', 
#                             '2009-12-01')].to_xarray()
pseudo_pcs = pseudo_pcs[slice('2070-01-01', 
                            '2099-12-01')].to_xarray()
pseudo_pcs = pseudo_pcs.expand_dims({'latitude': dwave.latitude, 
                           'longitude': dwave.longitude})

# talvez tenha que fazer para igualar os indices
# dwave = dwave.sel(time=slice('1980-02-01','2009-12-31'))
dwave['time'] = pseudo_pcs['time']

# unindo onda e indice
hs_ppcs = xr.merge([dwave, pseudo_pcs])

# removendo media mensal
# if parametro == 'Hs':
medias_mensais = dwave[parametro].groupby('time.month').mean('time')
deseason = dwave[parametro].groupby('time.month') - medias_mensais
# elif parametro == 'T02':
#     medias_mensais = dwave.mwp.groupby('time.month').mean('time')
#     deseason = dwave.mwp.groupby('time.month') - medias_mensais
# elif parametro == 'DIR':
#     medias_mensais = dwave.mwd.groupby('time.month').mean('time')
#     deseason = dwave.mwd.groupby('time.month') - medias_mensais

deseason = deseason.drop('month')

#unindo onda e indice
hs_deseason_ppcs = xr.merge([deseason, pseudo_pcs])

# plotando só pra ver
hs_ppcs[parametro].sel(latitude=40,
                longitude=-10.5,
                method='nearest').plot()
hs_deseason_ppcs[parametro].sel(latitude=40,
                         longitude=-10.5,
                         method='nearest').plot()


# # calculando a correlacao
# correlation = xr.corr(hs_ppcs.swh, 
#                     hs_ppcs.indice, 
#                     dim='time').to_dataset(name='Hs')

# fig, ax = faz_mapa_lambert()
# cd = correlation.Hs.plot(levels=clevs,
#                                 cmap=colormap,
#                                 transform=ccrs.PlateCarree(),
#                                 add_colorbar=True)

# significant = correlation.where(abs(correlation) > siglev)

# significant['Hs'].plot.contourf(colors='none', 
#                                 hatches = ['///'], 
#                                 transform=ccrs.PlateCarree(),
#                                 add_colorbar=False)

# if tempo == 'presente':
#     plt.title('Correlation ' + modelo + ' Hs/AO index - 1990 : 2020')
# elif tempo == 'futuro':
#     plt.title('Correlation ' + modelo + ' Hs/AO index - 2070 : 2100')


# e agora a correlacao com os resultados sem a sazonalidade
# corr_deseason = xr.corr(hs_deseason_ppcs.swh, 
#                         hs_deseason_ppcs.indice, 
#                         dim='time').to_dataset(name=parametro)
# siglev = n100_80

# fig, ax = faz_mapa_lambert()
# cd = corr_deseason.Hs.plot(levels=clevs,
#                                 cmap=colormap,
#                                 transform=ccrs.PlateCarree(),
#                                 add_colorbar=False)
# significant = corr_deseason.where(abs(corr_deseason) > siglev)

# significant['Hs'].plot.contourf(colors='none', 
#                                 hatches = ['///'], 
#                                 transform=ccrs.PlateCarree(),
#                                 add_colorbar=False)

# if tempo == 'presente':
#     plt.title('Correlation ' + modelo + ' Hs/AO index - 1980 : 2009')
# elif tempo == 'futuro':
#     plt.title('Correlation ' + modelo + ' Hs/AO index - 2070 : 2100')


# selecionando agora só o periodo de inverno dos dois datasets
hs_deseason_ppcs_winter = hs_deseason_ppcs.sel(time=hs_deseason_ppcs[
                                                'time.season']=='DJF')

corr_deseason_winter = xr.corr(hs_deseason_ppcs_winter[parametro], 
                        hs_deseason_ppcs_winter.indice, 
                        dim='time').to_dataset(name=parametro)

siglev = n30_80
fig, ax = faz_mapa_lambert()
cd = corr_deseason_winter[parametro].plot(levels=clevs,
                                cmap=colormap,
                                transform=ccrs.PlateCarree(),
                                add_colorbar=False)
fig.colorbar(cd, orientation='horizontal', 
              pad=0.03, shrink=0.8)
significant = corr_deseason_winter.where(abs(corr_deseason_winter) > siglev)

significant[parametro].plot.contourf(colors='none', 
                                hatches = ['///'], 
                                transform=ccrs.PlateCarree(),
                                add_colorbar=False)

if tempo == 'presente':
    plt.title('Correlation ' + modelo + ' ' + parametro + ' /AO index - 1980 : 2009 \n Winter')
elif tempo == 'futuro':
    plt.title('Correlation ' + modelo + ' ' + parametro + ' /AO index - 2070 : 2100 \n Winter')



# avaliando as mudancas de sinal
change = np.where(np.sign(ppcs.indice).diff())[0]
# duration = np.diff(change)
# duration_sort = np.sort(duration)
# imax_duration = np.where(duration == duration_sort[-1])[0][0]

# max_duration = np.arange(change[imax_duration], 
#                          change[imax_duration+1])
periodo_continuo = ppcs.iloc[max_duration]

for i in range(len(change) -1):
    if (change[i+1] - change[i] >= 3):
        plt.figure()
        permanece_sinal = hs_deseason_ppcs.sel(time=slice(ppcs.index[change[i]], 
                                          ppcs.index[change[i+1] - 1]))
        (permanece_sinal.swh.mean(dim='time') - 
                             hs_deseason_ppcs.swh.mean(dim='time')).plot()
        if permanece_sinal.indice.values[0][0][0] > 0:
            plt.title('Positive index for ' + str(len(permanece_sinal.time)) +
                      ' months')
            plt.savefig((r'/home/aline/Dropbox/IST_investigation/Teleconnections/'
                     'indice_negativo/CMIP5/positive_' + str(i) + '.png'))
        elif permanece_sinal.indice.values[0][0][0] < 0:
            plt.title('Negative index for ' + str(len(permanece_sinal.time)) +
                      ' months')
            plt.savefig((r'/home/aline/Dropbox/IST_investigation/Teleconnections/'
                     'indice_negativo/CMIP5/negative_' + str(i) + '.png'))
        plt.close()




permanece_negativo = hs_deseason_ppcs.sel(time=slice(ppcs.index[change[0]], 
                                          ppcs.index[change[1]]))


# correlacionando HGT
historical = historical.sel(time=slice('1960-02-01', '2019-12-01'))
f = f.sel(time=slice('1960-02-01', '2019-12-01'))
corr_hgt = xr.corr(historical.hgt, f.hgt, dim='time')


fig, ax = faz_mapa_lambert()
corr_hgt.plot(levels=clevs,
              cmap=colormap,
              transform=ccrs.PlateCarree())


# comparando as duas series de ppcs
CMIP = pseudo_pcs.to_dataframe()
ERA = pseudo_pcs.to_dataframe()

coincidente = pd.merge(CMIP, ERA, on='time', how='inner', 
                       suffixes=('_CMIP', '_ERA'))

coincidente.corr()

# plot significancia pearson


