def faz_mapa_corr(proj, levels, coords_lim=None):

    fig, ax = plt.subplots(subplot_kw={'projection': proj})
    ax.coastlines()
    ax.set_global()
    if coords_lim != None:
        print('Alterando limites do mapa!')
        ax.set_extent(coords_lim, ccrs.PlateCarree())

    return ax, fig
