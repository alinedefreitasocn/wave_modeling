#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 11 15:10:39 2021

@author: aline

avaliando periodo de mudança de sinal do indice da ao

"""
import xarray as xr
import pandas as pd
import numpy as np
import cfgrib
import matplotlib.pyplot as plt
from faz_figuras import *


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


change = np.where(np.sign(ppcs).diff())[0]
duration = np.diff(change)
duration_sort = np.sort(duration)
imax_duration = np.where(duration == duration_sort[-1])[0][0]

max_duration = np.arange(change[imax_duration], 
                         change[imax_duration+1])
periodo_continuo = ppcs.iloc[max_duration]

# lendo arquivos de onda do CMIP
mypath = '/home/aline/Documents/Dados/Jerry/WW3_Marta/Futuro/'
mypath = '/home/aline/Documents/Dados/Jerry/WW3_Marta/Presente/'

wf = mypath + 'futuro_hs_mean_mensal.nc'
wf = mypath + 'presente_hs_mean_mensal.nc'

hs = xr.open_dataset(wf)
hs = hs.drop_vars('MAPSTA')
hs = hs.sel(latitude=slice(20,90), longitude= slice(-101,  35))

# removendo a sazonalidade


permanece_negativo = hs.sel(time=slice(periodo_continuo.index[0], 
                                          periodo_continuo.index[-1]))
anomalia_periodo_negativo = (permanece_negativo.hs.mean(dim='time') - 
                             hs.hs.mean(dim='time'))


####################################################################
# Fazendo o mesmo para o ERA5

fwave = '/home/aline/Documents/Dados/ERA5/montly_mean_1979_2020.grib'
dwave = cfgrib.open_datasets(fwave)[0]
findex = '/home/aline/Documents/Dados/indices/calculados/index_era5.txt'
indices = pd.read_csv(findex, 
                  header=0,
                  parse_dates=True,
                  index_col='time',
                  names=['time', 'id'])

change = np.where(np.sign(indices).diff())[0]
duration = np.diff(change)
duration_sort = np.sort(duration)
imax_duration = np.where(duration == duration_sort[-1])[0][0]

max_duration = np.arange(change[imax_duration], 
                         change[imax_duration+1])
periodo_continuo = indices.iloc[max_duration]
permanece_negativo = dwave.sel(time=slice(periodo_continuo.index[0], 
                                          periodo_continuo.index[-1]))
anomalia_periodo_negativo = (permanece_negativo.swh.mean(dim='time') - 
                             dwave.swh.mean(dim='time'))


for i in range(len(change)):
        ondinha_indice = indices.iloc[np.arange(change[i], change[i+1])]
        permanece_negativo = dwave.sel(time=slice(ondinha_indice.index[0],
                                                  ondinha_indice.index[-1]))
        anomalia = (permanece_negativo.swh.mean(dim='time') - 
                    dwave.swh.mean(dim='time')).to_dataset(name='anomalia')
        plot_correlacao(anomalia, 'anomalia', 'AO', 100)
        plt.title(str(ondinha_indice.index[0]) + ' - ' +
                  str(ondinha_indice.index[-1]))
        plt.savefig(('/home/aline/Dropbox/IST_investigation/Teleconnections/' + 
                     'indice_negativo/ERA5/' + 
                    str(ondinha_indice.index[0]) + '-' +
                  str(ondinha_indice.index[-1]) + '.png'))
        plt.close()