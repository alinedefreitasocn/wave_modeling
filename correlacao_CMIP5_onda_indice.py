#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 10:20:57 2021

@author: aline

Correlacao entre dados do CMIP5
"""
import xarray as xr
import pandas as pd
from xskillscore import pearson_r
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import cartopy.crs as ccrs
from faz_figuras import *

# clevs = np.arange(-1, 1.1, 0.1)
clevs = np.linspace(-1, 1, 21)
colormap = plt.cm.Spectral

mypath = '/home/aline/Documents/Dados/Jerry/WW3_Marta/Futuro/'
mypath = '/home/aline/Documents/Dados/Jerry/WW3_Marta/Presente/'

wf = mypath + 'futuro_hs_mean_mensal.nc'
wf = mypath + 'presente_hs_mean_mensal.nc'
hs = xr.open_dataset(wf)
hs = hs.drop_vars('MAPSTA')
hs = hs.sel(latitude=slice(20,90), longitude= slice(-101,  35))



# pasta para salvar os arquivos
indexpath = '/home/aline/Documents/Dados/Jerry/GEOPOT_1000hPa/'

# indice historico calculado a partir da pressao atmosferica do CMIP5
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

# excluindo os 10 primeiros anos para obter o numero certo de climatologias
ppcs = ppcs[slice(hs.isel(time=0).time.values, 
                           hs.isel(time=-1).time.values)].to_xarray()
ppcs = ppcs.expand_dims({'latitude': hs.latitude, 
                           'longitude':hs.longitude})

hs_ppcs = xr.merge([hs, ppcs])

correlacao = xr.corr(hs_ppcs.hs, 
                     hs_ppcs.pseudo_pcs, 
                     dim='time').to_dataset(name='Hs')


plot_correlacao(correlacao, 'Hs', 'AO', 0.19)


# fazendo alguns testes
onda_media_climatologica = hs_ppcs.hs.mean(dim='time')
onda_media_indice_negativo = hs_ppcs.where(
    hs_ppcs.pseudo_pcs < 0, drop=True).hs.mean(dim='time')
anomalia_indice_negativo = (onda_media_indice_negativo - 
                                onda_media_climatologica).to_dataset(name='Hs')
plot_correlacao(anomalia_indice_negativo, 'Hs', 'AO', 0.5,
                clevs=np.linspace(-0.3,
                                  0.3,
                                  21))
onda_media_indice_extremo_negativo = hs_ppcs.where(
    hs_ppcs.pseudo_pcs < -2, drop=True).hs.mean(dim='time')
anomalia_indice_extremo_negativo = (onda_media_indice_extremo_negativo - 
                                onda_media_climatologica).to_dataset(name='Hs')
plot_correlacao(anomalia_indice_extremo_negativo, 'Hs', 'AO', 3,
                clevs=np.linspace(-2,
                                  2,
                                  21))


onda_media_indice_positivo = hs_ppcs.where(
    hs_ppcs.pseudo_pcs > 0, drop=True).hs.mean(dim='time')
anomalia_indice_positivo = (onda_media_indice_positivo - 
                                onda_media_climatologica).to_dataset(name='Hs')
plot_correlacao(anomalia_indice_positivo, 'Hs', 'AO', 0.5,
                clevs=np.linspace(-0.3,
                                  0.3,
                                  21))
onda_media_indice_extremo_positivo = hs_ppcs.where(
    hs_ppcs.pseudo_pcs > 2, drop=True).hs.mean(dim='time')
anomalia_indice_extremo_positivo = (onda_media_indice_extremo_positivo - 
                                onda_media_climatologica).to_dataset(name='Hs')
plot_correlacao(anomalia_indice_extremo_positivo, 'Hs', 'AO', 3, 
                clevs=np.linspace(-2, 2, 21))


# inverno 
winter = hs_ppcs.sel(time=hs_ppcs['time.season'] == 'DJF')

winter_correlacao = xr.corr(winter.hs, 
                     winter.pseudo_pcs, 
                     dim='time').to_dataset(name='Hs')

plot_correlacao(winter_correlacao, 'Hs', 'AO', 0.361)



