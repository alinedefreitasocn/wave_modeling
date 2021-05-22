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

# general definitions
tele = 'AO'
finalpath = (r'/home/aline/Dropbox/IST_investigation'
                           '/Teleconnections/correlacoes/' + tele + '/')

# clevs = np.arange(-1, 1.1, 0.1)
clevs = np.linspace(-1, 1, 21)
colormap = plt.cm.Spectral

if tele == 'AO':
    '''
    REading index file
    for index as txt
    '''
    findex = '/home/aline/Documents/Dados/indices/calculados/index_era5.txt'
    indices = pd.read_csv(findex, 
                      header=0,
                      parse_dates=True,
                      index_col='time',
                      names=['time', 'id'])
    
# selecionando 30 anos do ERA5 que representa o tempo presente: 
# de 1980 a 2020
# reading wave file
fwave = '/home/aline/Documents/Dados/ERA5/montly_mean_1979_2020.grib'
dwave = cfgrib.open_datasets(fwave)[0]
dwave = dwave.sel(time=slice('1990-01-01','2020-12-01'),
                  latitude=slice(90,20), 
                  longitude= slice(-101,  35))

# removendo media mensal
medias_mensais_era = dwave.swh.groupby('time.month').mean('time')
deseason_era = dwave.swh.groupby('time.month') - medias_mensais_era
deseason_era = deseason_era.drop('month')

# cropping index time series to match data
index_crop = indices[slice(dwave.isel(time=0).time.values,
                                dwave.isel(time=-1).time.values)]
index_crop = index_crop.id.to_xarray()

corr_era5 = xr.corr(dwave.swh.round(3), 
                                index_crop.round(3), 
                                dim='time').to_dataset(name='Hs')

fig, ax = faz_mapa_lambert()
cd = corr_era5.Hs.plot(levels=clevs,
                                cmap=colormap,
                                transform=ccrs.PlateCarree(),
                                add_colorbar=False)
plt.title('correlation ERA5 Hs/AO index - 1990 : 2020')


# mesma coisa para o CMIP5
indexpath = '/home/aline/Documents/Dados/Jerry/GEOPOT_1000hPa/'

mypath = '/home/aline/Documents/Dados/Jerry/WW3_Marta/Presente/'
wf = mypath + 'presente_hs_mean_mensal.nc'
hs = xr.open_dataset(wf)

# removendo media mensal
medias_mensais = hs.hs.groupby('time.month').mean('time')
deseason = hs.hs.groupby('time.month') - medias_mensais
deseason = deseason.drop('month')


pseudo_pcs = xr.open_dataset(indexpath + 'index_historical1.nc')

pseudo_pcs = pseudo_pcs.rename({'__xarray_dataarray_variable__':'indice'})
ppcs = pd.DataFrame(data=pseudo_pcs.indice.values, 
                    index=pseudo_pcs.time.values, 
                    columns=['pseudo_pcs'])
# precisei fazer essas transformacoes para calcular a correlacao
# nao estava identificando a dimensao time na serie ppcs (estava como index)
# e nao sei por qual motivo estava com algumas medias mensais com o 
# indice no segundo dia do mes...
datetime_indices = {'YEAR': ppcs.index.year, 'MONTH': ppcs.index.month,
                    'DAY': np.ones(len(ppcs), dtype=int)}
ppcs.index = pd.to_datetime(datetime_indices)
ppcs.index.name = 'time'

ppcs = ppcs[slice(hs.isel(time=0).time.values, 
                           hs.isel(time=-1).time.values)].to_xarray()
ppcs = ppcs.expand_dims({'latitude': hs.latitude, 
                           'longitude':hs.longitude})

hs_ppcs = xr.merge([hs, ppcs])
hs_deseason_ppcs = xr.merge([deseason, ppcs])

correlacao_cmip = xr.corr(hs_ppcs.hs, 
                     hs_ppcs.pseudo_pcs, 
                     dim='time').to_dataset(name='Hs')

correlacao_cmip_deseason = xr.corr(hs_deseason_ppcs.hs, 
                     hs_deseason_ppcs.pseudo_pcs, 
                     dim='time').to_dataset(name='Hs')



fig, ax = faz_mapa_lambert()
cd = correlacao_cmip.Hs.plot(levels=clevs,
                                cmap=colormap,
                                transform=ccrs.PlateCarree(),
                                add_colorbar=False)
plt.title('correlation CMIP5 Hs/AO index - 1990 : 2020')

fig, ax = faz_mapa_lambert()
cd = correlacao_cmip_deseason.Hs.plot(levels=clevs,
                                cmap=colormap,
                                transform=ccrs.PlateCarree(),
                                add_colorbar=False)
plt.title('correlation CMIP5 Hs/AO index - 1990 : 2020 \n (deseason)')
