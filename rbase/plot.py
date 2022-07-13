import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap #, LinearSegmentedColormap
import numpy as np
import cmaps
from .base import *
from .xarray import *

import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import cartopy.feature as cfeature


from scipy.ndimage import gaussian_filter
from scipy.ndimage.filters import maximum_filter, minimum_filter

from metpy.units import units

def add_shape(ax, shp, linewidth=0.3, **kw):
    shape_feature = ShapelyFeature(Reader(shp).geometries(),
                                ccrs.PlateCarree(), facecolor='none', )
    ax.add_feature(shape_feature, linewidth=linewidth, **kw)
    return ax


def setMapAxis(ax,
               lon=[0, 60, 120, 180, 240, 300, 360],
               lat=[-90, -60, -30, 0, 30, 60, 90]):
    # ax.set_extent([0, 359.9, -60, 90])
    # ax.add_feature(cfeature.STATES.with_scale('10m'),
    #                edgecolor='b', alpha=0.2, zorder=0)
    # ax.add_feature(cfeature.LAND)
    # countries = shapereader.natural_earth(resolution='50m',
    #                                   category='cultural',
    #                                   name='admin_0_countries')
    ax.coastlines(edgecolor='b', resolution='50m')
    ax.set_xticks(lon, crs=ccrs.PlateCarree())
    ax.set_yticks(lat, crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    return ax


def add_china(range = [70, 160, 5, 55]):
    ax = plt.gca()
    dx = 10
    dy = 5
    lon=np.arange(range[0], range[1] + dx/2, 10)
    lat=np.arange(range[2], range[3] + dy/2, 5)
    ax = setMapAxis(ax, lon, lat)
    ax.set_xlim(xmin=range[0], xmax=range[1])
    ax.set_ylim(ymin=range[2], ymax=range[3])
    add_shape(ax, "data/shp/bou2_4p_ChinaProvince_sml.shp")
    return ax


def get_cmap(cmap=cmaps.amwg256, ncol=12,
             under=np.array([1, 1, 1, 0]), extend="both"):
    """
    # References
    - https://matplotlib.org/3.1.1/tutorials/colors/colorbar_only.html#sphx-glr-tutorials-colors-colorbar-only-py
    - https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.colors.BoundaryNorm.html#matplotlib.colors.BoundaryNorm
    - https://matplotlib.org/3.1.1/api/colorbar_api.html#matplotlib.colorbar.ColorbarBase
    """
    # black = np.array([0, 0, 0, 1])
    # pink  = np.array([248/256, 24/256, 148/256, 1])
    # cmaps.amwg256.colors.shape
    if extend == "both":
        cols_all = rbind(under, cmap(np.linspace(0, 1, ncol + 1)))
        cmap = ListedColormap(cols_all[1:-1])
        # 这里修改head和tail的颜色
        cmap.set_over(cols_all[-1])
        cmap.set_under(cols_all[0])
        return cmap
    else:
        cols = rbind(under, cmap(np.linspace(0, 1, ncol - 1)))
        return ListedColormap(cols)


def add_cbar(bounds, cmap=cmaps.amwg256, extend="both", **kwargs):
    """
    Unequal-spaced colorbar

    # Arguments
    - `cmap`: returned by [get_cmap()]
    - `**kwargs`: other parameters to [plt.colorbar()]

    # Examples
    ```python
    x = np.linspace(0, 10, 1000)
    I = np.sin(x) * np.cos(x[:, np.newaxis])

    bounds = c([-1, -0.5, -0.1, 0, 0.1, 0.5, 1])
    cmap = get_cmap(ncol = len(bounds) - 1)
    plt.imshow(I, cmap=cmap)
    add_cbar(bounds, cmap)
    ```
    """
    # ncol = len(bounds) - 1
    # cmap = get_cmap(cmap, ncol, extend=extend)
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cbar = plt.colorbar(
        mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
        extend=extend, **kwargs)
    return cbar
    # cb1 = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
    #                                 norm=norm,
    #                                 extend='both',
    #                                 orientation='horizontal')
    # cb1.set_label('Default BoundaryNorm ouput')


def r_contourf(ds, brks = [0.1, 0.2, 0.5, 1, 2, 5], show_cbar=True):
    ax = plt.gca()
    ncol = (len(brks) - 1) * 2
    # cmap = cmaps.amwg256
    cmap = get_cmap(ncol=ncol)
    lon, lat = get_coords(ds)
    ax.contourf(lon, lat, 
        ds,
        levels=brks,
        cmap=cmap,
        # levels=clevthick, colors=color,
        # linewidths=1.0, linestyles=linestyle,
        extend="both",
        transform=ax.projection)
    if show_cbar:
        norm = mpl.colors.BoundaryNorm(brks, cmap.N)  
        ax.figure.colorbar(
            mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
            orientation='horizontal',
            extend="both",
            aspect=30, shrink=0.8, pad=0.05)


# 500hPa z brks
def get_zbrks(mid=588, half=10, by=4):
    return (
        np.arange(mid - by*half, mid, by), 
        np.array([mid]), 
        np.arange(mid, mid + by*half, by), 
    )

def contour_z(z, brks = None, lev=500, colors = ('tab:blue', 'tab:red', 'r'), **kw):
    """
    Plot thickness with multiple colors
    
    # Argument
    - `**kw`: others to [get_zbrks()]
    
    # Examples
    ```python
    brks = (np.arange(0, 5400, 60),
            np.array([5400]),
            np.arange(5460, 7000, 60))
    ```
    """
    ax = plt.gca()
    if brks == None:
        if lev == 500:
            brks = get_zbrks(588, **kw)
        elif lev > 500:
            brks = get_zbrks(150, **kw)
        else:
            brks = get_zbrks(1200, **kw)
    
    lon, lat = get_coords(z)
    # if colors == None:
    #     colors = ('tab:blue', 'b', 'tab:red')
    kw_clabels = {'fontsize': 11, 'inline': True, 'inline_spacing': 10, 'fmt': '%i',
        # "manual": True, 
        'rightside_up': True
    #   'use_clabeltext': True
        }
    lwd = c(0.7, 1.5, 0.7)
    k = 0
    for clevthick, color in zip(brks, colors):
        # linestyle = "solid" if color == 'r' else "dashed"
        linestyle = "solid"
        cs = ax.contour(lon, lat, z, levels=clevthick, colors=color,
                        linewidths=lwd[k], linestyles=linestyle, 
                        transform=ax.projection)
        plt.clabel(cs, **kw_clabels)
        k=k+1


def plot_maxmin_points(z, nsize = 12, 
    extrema = "max", symbol = "H", color='k', transform=None):
    """
    This function will find and plot relative maximum and minimum for a 2D grid.

    The function can be used to plot an H for maximum values (e.g., High
    pressure) and an L for minimum values (e.g., low pressue). It is best to
    used filetered data to obtain  a synoptic scale max/min value. The symbol
    text can be set to a string value and optionally the color of the symbol and
    any plotted value can be set with the parameter color
    
    # Arguments

    - `lon`        : plotting longitude values (2D) `lat` = plotting latitude values (2D)
    - `data`       : 2D data that you wish to plot the max/min symbol placement
    - `extrema`    : "max" or "min"
    - `nsize`      : Size of the grid box to filter the max and min values to plot a reasonable number 
    - `symbol`     : String to be placed at location of max/min value 
    - `color`      : String matplotlib colorname to plot the symbol (and numerica value, if plotted) 
    - `plot_value` : Boolean (True/False) of whether to plot the numeric value of max/min point. 
        The max/min symbol will be plotted on the current axes within the bounding frame (e.g., clip_on=True)

    # References
    - https://unidata.github.io/python-gallery/examples/HILO_Symbol_Plot.html
    """
    
    ax = plt.gca()
    lon, lat = get_coords(z)
    data = z.values

    if (extrema == 'max'):
        data_ext = maximum_filter(data, nsize, mode='nearest')
    elif (extrema == 'min'):
        data_ext = minimum_filter(data, nsize, mode='nearest')
    else:
        raise ValueError('Value for hilo must be either max or min')

    Ilat, Ilon = np.where(data_ext == data)

    # ax = plt.gca()
    for i in range(len(Ilat)):
        x, y = lon[Ilon[i]], lat[Ilat[i]]
        # print("|", x, y, Ilon[i], Ilat[i])
        # print(data.shape)
        ax.text(x, y, symbol, color=color, size=24,
            clip_on=True, horizontalalignment='center', verticalalignment='center',
            transform=ax.projection)
        ax.text(x, y,
            '\n' + str(np.int(data[Ilat[i], Ilon[i]])),
            color=color, size=12, clip_on=True, fontweight='bold',
            horizontalalignment='center', verticalalignment='top', transform=ax.projection)


# mixing_ratio = np.array([0.0004, 0.001, 0.002, 0.004, 0.007, 0.01, 
#     0.016, 0.024, 0.032]).reshape(-1, 1)
# ax.text(x, y, '\n' + str(np.int(data[Ilat[i], Ilon[i]])),
#             color=color, size=12, clip_on=True, fontweight='bold',
#             horizontalalignment='center', verticalalignment='top', transform=ax.projection)

def smooth_uv(u, v, sigma=3.0, unit = units('m/s')):
    """
    # Arguments:
    - `unit`: `units('m/s')`
    """
    u = gaussian_filter(u.data, sigma=sigma) * unit
    v = gaussian_filter(v.data, sigma=sigma) * unit
    return u, v


def add_wind(ds, step = 10, length = 6, **kw):
    """
    https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.barbs.html
    ## Arguments:

    - `barb_increments`: dict(half=5, full=10, flag=50)
    """
    ax = plt.gca()
    ind = (slice(None, None, step), slice(None, None, step))
    
    u = ds["u"][ind[0], ind[1]]
    v = ds["v"][ind[0], ind[1]]
    u, v = smooth_uv(u, v)
    lon, lat = get_coords(ds)
    ax.barbs(lon[ind[0]], lat[ind[1]],
            u.to('kt').m, v.to('kt').m,
            #  fill_empty = True, 
             length = length, **kw,
             barb_increments=dict(half=5, full=10, flag=50),
            #  barb_increments=dict(half=2, full=4, flag=10),
            sizes=dict(emptybarb=0, spacing=0.2, height=0.3),
            #  pivot='middle', 
            color='black', transform=ax.projection)
