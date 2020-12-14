import matplotlib
import matplotlib.pyplot as plt

font = {'family' : 'normal',
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
