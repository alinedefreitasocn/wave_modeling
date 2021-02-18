#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 18:24:15 2021

@author: aline

trabalhando com os netcdfs das correlacoes ja calculadas
"""
import xarray as xr
from faz_figuras import *
import matplotlib as mpl

mpl.rcParams['hatch.linewidth'] = 0.5


tele = 'AO'
basefilename = '/home/aline/Documents/Dados/netCDFs_correlacao/'
finalpath = (r'/home/aline/Dropbox/IST_investigation'
                           '/Teleconnections/correlacoes/' + tele + '/')


""" winter wave """

# critical value for pearson correlation
significant_winter = 0.3

wwvc = 'map_corr_AO_winter2.nc'
winter_wave_corr = xr.open_dataset(basefilename + wwvc)
winter_wave_corr_filtrado = winter_wave_corr.where(abs(winter_wave_corr) < 0.86)

for k in winter_wave_corr_filtrado.data_vars.keys():
    fig, ax = plot_correlacao(winter_wave_corr_filtrado, 
                              k, 
                              tele, 
                              significant_winter)
    fig.savefig((finalpath + 'winter_' + k + '_' + tele + '_NA_Lambert.png'),
                dpi=400)
    
    plt.close()


""" Year-Round """

wvc = 'map_corr2_AO.nc'
wave_corr = xr.open_dataset(basefilename + wvc)
# critical value for pearson correlation
significant = 0.16
for k in wave_corr.data_vars.keys():
    fig, ax = plot_correlacao(wave_corr, 
                              k, 
                              tele, 
                              significant)
    fig.savefig((finalpath + k + '_' + tele + '_NA_Lambert.png'),
                dpi=400)
    
    plt.close()


