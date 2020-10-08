"""
Bibliography:
https://www.sciencedirect.com/science/article/pii/B9780127329512500089

https://www.sciencedirect.com/science/article/pii/B9780128117149000061

https://www.sciencedirect.com/science/article/pii/B9780127329512500120
"""

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import xarray as xr
import cfgrib


g = 9.81

file = '/home/aline/Documents/IST_investigation/ERA5/geopotential_1989_2019.grib'

DS = cfgrib.open_datasets(file)[0]
height = DS/g
Hmean = height.mean(dim='time')
anomalie = height - Hmean


# making plot area
ax1 = plt.subplot(projection=ccrs.Orthographic(0, 90))
DS.isel(time=0).z.plot(transform=ccrs.PlateCarree(),
                        subplot_kws={"projection": ccrs.Orthographic(0, 90)},
                        cmap='RdBu_r')
ax1.coastlines(zorder=3)
plt.title('Geopotencial 1989-01-01')
plt.savefig('/home/aline/Documents/IST_investigation/ERA5/images/geopotencialt0.png')
plt.show(block=False)


ax2 = plt.subplot(projection=ccrs.Orthographic(0, 90))
height.isel(time=0).z.plot(transform=ccrs.PlateCarree(),
                        subplot_kws={"projection": ccrs.Orthographic(0, 90)},
                        cmap='RdBu_r')
ax2.coastlines(zorder=3)
plt.title('Altura geopotencial (geopotencial/g)  1989-01-01')
plt.savefig('/home/aline/Documents/IST_investigation/ERA5/images/altura_geopotencial.png')
plt.show(block=False)


ax3 = plt.subplot(projection=ccrs.Orthographic(0, 90))
Hmean.z.plot(transform=ccrs.PlateCarree(),
                        subplot_kws={"projection": ccrs.Orthographic(0, 90)},
                        cmap='coolwarm')
ax3.coastlines(zorder=3)
plt.title('Mean 1000 hPa Geopotential Height')
plt.savefig('/home/aline/Documents/IST_investigation/ERA5/images/altura_geopotencial_media_coolwarm.png')
plt.show(block=False)
plt.close()

for t in range(len(anomalie.time)):
    ax = plt.subplot(projection=ccrs.Orthographic(0, 90))
    anomalie.isel(time=t).z.plot(transform=ccrs.PlateCarree(),
                        subplot_kws={"projection": ccrs.Orthographic(0, 90)},
                        cmap='RdBu_r',
                        vmin=anomalie.z.min(),
                        vmax=anomalie.z.max())
    ax.coastlines(zorder=3)
    plt.title('1000 hPa Geopotential Height Anomalies: ' + str(anomalie.isel(time=t).time.values)[:7])
    plt.savefig('/home/aline/Documents/IST_investigation/ERA5/images/Calculo_altura_atm/anomalia_' + str(anomalie.isel(time=t).time.values)[:7])
    plt.close()

############################################################
############################################################
############################################################
#   Fazendo teste de figura com contour
anomalie.isel(time=0).z.plot.contourf(levels=[-250, -200, -150, -100, -50, 0, 50, 100, 150, 200, 250], transform=ccrs.PlateCarree(), subplot_kws={"projection": ccrs.Orthographic(0, 90)})

anomalie.isel(time=0).z.plot.contour(levels=[-250, -200, -150, -100, -50, 0, 50, 100, 150, 200, 250], colors='black', transform=ccrs.PlateCarree(), subplot_kws={"projection": ccrs.Orthographic(0, 90)})
