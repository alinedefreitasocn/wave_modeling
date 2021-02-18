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
significant = 0.16
significant_winter = 0.3

tele = 'AO'
basefilename = '/home/aline/Documents/Dados/netCDFs_correlacao/'
finalpath = (r'/home/aline/Dropbox/IST_investigation'
                           '/Teleconnections/correlacoes/' + tele + '/')


""" winter wave """

# critical value for pearson correlation


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


""" Year-Round wave"""

wvc = 'map_corr2_AO.nc'
wave_corr = xr.open_dataset(basefilename + wvc)
# critical value for pearson correlation

for k in wave_corr.data_vars.keys():
    fig, ax = plot_correlacao(wave_corr, 
                              k, 
                              tele, 
                              significant)
    fig.savefig((finalpath + k + '_' + tele + '_NA_Lambert.png'),
                dpi=400)
    
    plt.close()

" Wind"
wind = 'map_corr_wind_AO.nc'
wind_corr = xr.open_dataset(basefilename + wind)

for k in wind_corr.data_vars.keys():
    fig, ax = plot_correlacao(wind_corr, 
                              k, 
                              tele, 
                              significant)
    fig.savefig((finalpath + k + '_' + tele + '_NA_Lambert.png'),
                dpi=400)
    
    plt.close()
    

wwind = 'map_corr_wind_AO_winter.nc'
wwind_corr = xr.open_dataset(basefilename + wwind)

for k in wwind_corr.data_vars.keys():
    fig, ax = plot_correlacao(wwind_corr, 
                              k, 
                              tele, 
                              significant_winter)
    fig.savefig((finalpath + 'winter' + k + '_' + tele + '_NA_Lambert.png'),
                dpi=400)
    
    plt.close()
    
    
wwave = 'map_corr_wind_wave_AO.nc'
wwave_corr = xr.open_dataset(basefilename + wwave)
# critical value for pearson correlation

for k in wwave_corr.data_vars.keys():
    fig, ax = plot_correlacao(wwave_corr, 
                              k, 
                              tele, 
                              significant)
    fig.savefig((finalpath + k + '_' + tele + '_NA_Lambert.png'),
                dpi=400)
    
    plt.close()
    

wwwave = 'map_corr_wind_wave_AO_winter.nc'
wwwave_corr = xr.open_dataset(basefilename + wwwave)
wwwave_corr_filtrado = wwwave_corr.where(abs(wwwave_corr) < 0.86)
# critical value for pearson correlation

for k in wwwave_corr_filtrado.data_vars.keys():
    fig, ax = plot_correlacao(wwwave_corr_filtrado, 
                              k, 
                              tele, 
                              significant_winter)
    fig.savefig((finalpath + 'winter' + k + '_' + tele + '_NA_Lambert.png'),
                dpi=400)
    
    plt.close()