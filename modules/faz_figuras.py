import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.path as mpath
import cartopy.feature as cfeature



font = {
        'weight' : 'normal',
        'size'   : 22}

matplotlib.rc('font', **font)


def faz_mapa_corr(proj, levels, coords_lim=None):

    matplotlib.rcParams['contour.negative_linestyle'] = 'solid'

    fig, ax = plt.subplots(figsize=(20, 15),
                            dpi=400,
                            subplot_kw={'projection': proj})
    ax.coastlines()
    ax.set_global()
    if coords_lim != None:
        print('Alterando limites do mapa!')
        ax.set_extent(coords_lim, ccrs.PlateCarree())

    return fig, ax

def faz_mapa_lambert():
    proj = ccrs.LambertConformal(central_longitude=-35,
                            central_latitude=40,
                            standard_parallels=(0, 80), cutoff=20)
    fig, ax = plt.subplots(figsize=(20, 15),
                            dpi=400,
                            subplot_kw={'projection': proj})
    # ax = plt.axes(projection=proj)    
    ax.set_extent([-100, 30, 20, 80], crs=ccrs.PlateCarree())
    ax.coastlines(resolution='50m')
    ax.gridlines(alpha=0.8)
    ax.add_feature(cfeature.LAND, 
                   # color='gray',
                   alpha=0.8,
                   zorder=100, 
                   edgecolor='black')
    ax.add_feature(cfeature.BORDERS, linestyle='-', alpha=.8)
    ax.yaxis.tick_left()
    
    # *must* call draw in order to get the axis boundary used to add ticks:
    fig.canvas.draw()
    
    # Define gridline locations and draw the lines using cartopy's built-in gridliner:
    xticks = [-100, -90, -80, -70, -60, -50, -40, 
              -30, -20, -11, 0, 10, 20, 30]
    # xticks = list(ax.get_xticks())
    yticks = [20, 30, 40, 50, 60, 70, 80]
    #yticks = list(ax.get_yticks())
    ax.gridlines(xlocs=xticks, ylocs=yticks)
    
    
    # Make a boundary path in PlateCarree projection, I choose to start in
    # the bottom left and go round anticlockwise, creating a boundary point
    # every 1 degree so that the result is smooth:
        # faz com que a minha figura fique conica
    vertices = [(lon, 20) for lon in range(-100, 31, 1)] + \
               [(lon, 80) for lon in range(30, -101, -1)]
    boundary = mpath.Path(vertices)
    ax.set_boundary(boundary, transform=ccrs.PlateCarree())
    ax.gridlines(draw_labels=True)
    
    # # # Fazendo os labels na mao...
    # # # longitude
    # ax.text(-88, 20, '90°W', transform=ccrs.PlateCarree(),
    #         ha='right', va='center', rotation=-40)
    # ax.text(-78, 20, '80°W', transform=ccrs.PlateCarree(),
    #         ha='right', va='center', rotation=-30)
    # ax.text(-67, 19.7, '70°W', transform=ccrs.PlateCarree(),
    #         ha='right', va='center', rotation=-20)
    # ax.text(-57, 19.5, '60°W', transform=ccrs.PlateCarree(),
    #         ha='right', va='center', rotation=-15)
    # ax.text(-47, 19, '50°W', transform=ccrs.PlateCarree(),
    #         ha='right', va='center', rotation=-10)
    # ax.text(-40, 18.5, '40°W', transform=ccrs.PlateCarree(),
    #         ha='center', va='center', rotation=-3)
    # ax.text(-30, 18.5, '30°W', transform=ccrs.PlateCarree(),
    #         ha='center', va='center', rotation=3)
    # ax.text(-20, 18.5, '20°W', transform=ccrs.PlateCarree(),
    #         ha='center', va='center', rotation=10)
    # ax.text(-11, 18.5, '10°W', transform=ccrs.PlateCarree(),
    #         ha='center', va='center', rotation=15)
    # ax.text(-0, 18.5, '0°', transform=ccrs.PlateCarree(),
    #         ha='center', va='center', rotation=20)
    # ax.text(10, 18.5, '10°E', transform=ccrs.PlateCarree(),
    #         ha='center', va='center', rotation=35)
    # ax.text(20, 18.5, '20°E', transform=ccrs.PlateCarree(),
    #         ha='center', va='center', rotation=42)
    
    
    # # latitudes
    # ax.text(-101, 30, '30°N', transform=ccrs.PlateCarree(),
    #         ha='right', va='center', rotation=-5)
    
    return fig, ax

def faz_map_nbtools():
    from nbtools.map import Lambert
    
    lamb=Lambert(-100,30,20,80)


# def corrige_colorbar(fig, ax):
#     from mpl_toolkits.axes_grid1.inset_locator import inset_axes   
    
#     axins = inset_axes(ax,
#                    width="5%",  # width = 5% of parent_bbox width
#                    height="50%",  # height : 50%
#                    loc='center left',
#                    bbox_to_anchor=(1.05, 0., 1, 1),
#                    bbox_transform=ax.transAxes,
#                    borderpad=0,
#                    )

#     # Controlling the placement of the inset axes is basically same as that
#     # of the legend.  you may want to play with the borderpad value and
#     # the bbox_to_anchor coordinate.
    
#     im = ax.imshow([[1, 2], [2, 3]])
#     fig.colorbar(im, cax=axins)