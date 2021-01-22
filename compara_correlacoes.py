#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 09:15:44 2021

@author: aline

Comparando os mapas de correlacao do AO e do NAO

"""
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import cartopy.crs as ccrs
from faz_figuras import *
import numpy as np


finalpath = (r'/home/aline/Dropbox/IST_investigation'
                           '/Teleconnections/correlacoes/AO'
                           '/map_corr_AO.nc')
AO = xr.open_dataset(finalpath)


finalpath = (r'/home/aline/Dropbox/IST_investigation'
                           '/Teleconnections/correlacoes/NAO' 
                           '/map_corr_NAO.nc')
NAO = xr.open_dataset(finalpath)

clevs = np.arange(-1, 1.1, 0.1)
colormap = plt.cm.RdBu

for k in ['Hs', 'Tp', 'mwd']:
    # fig, ax = faz_mapa_corr(proj,
    #                         clevs,
    #                         coords_lim = limites)
    corr = AO[k] - NAO[k]
    fig, ax = faz_mapa_lambert()
    # where faz com que tudo que estiver entre 0.1 e -0.1 fique nan
    # e apareca branco no mapa
    cf = corr.where(abs(corr.values) < 0.1).plot.contourf(levels=clevs,
                                cmap=colormap,
                                transform=ccrs.PlateCarree(),
                                add_colorbar=False
                                )
    fig.colorbar(cf, orientation='horizontal', 
                 pad=0.25)
    plt.title('AO/NAO correlation differences in ' + k)
    # plt.show(block=False)
    fig.savefig((finalpath[:66] + k + '_AO_NAO_diff.png'))
    plt.close()
