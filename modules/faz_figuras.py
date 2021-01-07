import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.path as mpath



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
                            standard_parallels=(0, 80))
    fig, ax = plt.subplots(figsize=(20, 15),
                            dpi=400,
                            subplot_kw={'projection': proj})
    # ax = plt.axes(projection=proj)    
    ax.set_extent([-100, 30, 20, 80], crs=ccrs.PlateCarree())
    ax.coastlines()
    
    # Make a boundary path in PlateCarree projection, I choose to start in
    # the bottom left and go round anticlockwise, creating a boundary point
    # every 1 degree so that the result is smooth:
    vertices = [(lon, 0) for lon in range(-100, 31, 1)] + \
               [(lon, 80) for lon in range(30, -101, -1)]
    boundary = mpath.Path(vertices)
    ax.set_boundary(boundary, transform=ccrs.PlateCarree())
    
    
    return fig, ax


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