#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Aline Lemos de Freitas
15 de setembro de 2020


Reading NAO index
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import matplotlib.dates as mdates
import xarray as xr
from cfgrib import xarray_store
import cfgrib
import numpy as np

def read_index():
    file = '/home/aline/Documents/Dados/NCEP_NCAR/ao_index_CPC.txt'

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

    return f, fig, ax

def le_indice_onda(modelo, tempo, parametro):
    if modelo == 'ERA5':
        '''
        REading index file
        for index as txt
        '''
        findex = '/home/aline/Documents/Dados/indices/calculados/index_era5.txt'
        pseudo_pcs = pd.read_csv(findex, 
                          header=0,
                          parse_dates=True,
                          index_col='time',
                          names=['time', 'indice'])
        
        # selecionando 30 anos do ERA5 que representa o tempo presente: 
        # de 1980 a 2020
        # reading wave file
        fwave = '/home/aline/Documents/Dados/ERA5/montly_mean_1979_2020.grib'
        dwave = cfgrib.open_datasets(fwave)[0]
        
        if parametro == 'WND':
            fwave = '/home/aline/Documents/Dados/ERA5/wind_monthly_1979_2020.grib'
            dwave = cfgrib.open_datasets(fwave)[0]
        dwave = dwave.sel(time=slice('1980-01-01','2009-12-01'),
                          latitude=slice(90,20), 
                          longitude= slice(-101,  35))
    elif modelo == 'CMIP5':
        indexpath = '/home/aline/Documents/Dados/Jerry/GEOPOT_1000hPa/'
        
        #mypath = '/home/aline/Documents/Dados/Jerry/WW3_Marta/' + parametro
        
        if parametro == 'swh':
            mypath = '/home/aline/Documents/Dados/Jerry/WW3_Marta/Hs/'
            #fwave = mypath + 'presente_hs_mean_mensal2.nc'
            if tempo == 'presente':
                fwave = mypath + 'mensalmean_1980_2009.nc'
            elif tempo == 'futuro':
                fwave = mypath + 'mensalmean_2070_2099.nc'
            #fwave = mypath + 'futuro_hs_mean_mensal2.nc'
            dwave = xr.open_dataset(fwave).rename({'hs':'swh'})
        elif parametro =='mwp':
            mypath = '/home/aline/Documents/Dados/Jerry/WW3_Marta/T02/'
            #fwave = mypath + 'presente_hs_mean_mensal2.nc'
            if tempo == 'presente':
                fwave = mypath + 'mensalmean_1980_2009.nc'
            elif tempo == 'futuro':
                fwave = mypath + 'mensalmean_2070_2099.nc'
            #fwave = mypath + 'futuro_hs_mean_mensal2.nc'
            dwave = xr.open_dataset(fwave).rename({'t02':'mwp'})
        elif parametro =='mwd':
            mypath = '/home/aline/Documents/Dados/Jerry/WW3_Marta/DIR/'
            #fwave = mypath + 'presente_hs_mean_mensal2.nc'
            if tempo == 'presente':
                fwave = mypath + 'mensalmean_1980_2009.nc'
            elif tempo == 'futuro':
                fwave = mypath + 'mensalmean_2070_2099.nc'
            #fwave = mypath + 'futuro_hs_mean_mensal2.nc'
            dwave = xr.open_dataset(fwave).rename({'dir':'mwd'})
        elif parametro == 'WND':
            mypath = '/home/aline/Documents/Dados/Jerry/WW3_Marta/WND/'
            #fwave = mypath + 'presente_hs_mean_mensal2.nc'
            if tempo == 'presente':
                fwave = mypath + 'mensalmean_1980_2009.nc'
            elif tempo == 'futuro':
                fwave = mypath + 'mensalmean_2070_2099.nc'
            #fwave = mypath + 'futuro_hs_mean_mensal2.nc'
            dwave = xr.open_dataset(fwave).rename({'uwnd':'u10', 'vwnd':'v10'})
        
        pseudo_pcs = xr.open_dataset(indexpath + 'index_historical1.nc')
        
        pseudo_pcs = pseudo_pcs.rename({'__xarray_dataarray_variable__':'indice'})
        pseudo_pcs = pd.DataFrame(data=pseudo_pcs.indice.values, 
                            index=pseudo_pcs.time.values, 
                            columns=['indice'])
        # precisei fazer essas transformacoes para calcular a correlacao
        # nao estava identificando a dimensao time na serie ppcs (estava como index)
        # e nao sei por qual motivo estava com algumas medias mensais com o 
        # indice no segundo dia do mes...
        datetime_indices = {'YEAR': pseudo_pcs.index.year, 
                            'MONTH': pseudo_pcs.index.month,
                            'DAY': np.ones(len(pseudo_pcs),dtype=int)
                            }
        pseudo_pcs.index = pd.to_datetime(datetime_indices)
        pseudo_pcs.index.name = 'time'
    return pseudo_pcs, dwave
