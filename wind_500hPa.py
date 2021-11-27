# %%
# from operator import mul
# from matplotlib import cm
import metpy
from metpy import calc
from metpy.units import units
from rbase import *
import matplotlib.pyplot as plt
# import pandas as pd

bbox = c(70, 160, 5, 65) # 1d vec

file_sf = "data/ERA5_surface_6hour_2021JJA.grib"
data_sf = read_grib(file_sf, bbox)

data_prcp = read_grib(file_sf, bbox, filter_by_keys={'shortName': 'tp'})
data_prcp

data_lev = read_grib(
    "/mnt/i/CUG-HydroMeteorology/data/ERA5_pressure_levels_6hour_2021JJA.grib", 
    bbox, multi_lev = True)
data_lev

date = np.datetime64('2021-08-01T08:00:00')
delta_t = np.timedelta64(6, "h")

ds_lev = data_lev.sel(time=date)

tp = ERA5_Prcp_StackOverTime(data_prcp.tp) # accumulated prcp in 6 hour
prcp = tp.sel(time=(date))
prcp

# %%
# x.time.values[:5], x.valid_time.values[:5]
# x1 = x.isel(step = 1)
# data_sf.time.values[:5]

# %%
from rbase import *


fig = plt.figure(1, figsize=(13., 9.), constrained_layout=True)
# prj = ccrs.PlateCarree(central_longitude = 180)
ax = plt.axes(projection=ccrs.PlateCarree())
ax = setMapAxis_China(ax)

contourf_prcp(ax, prcp*1000)

plt.title('Valid Time: {}\n'.format(date) + 
    '500-hPa Geopotential Heights (contour, dm), surface precipitation (fill, mm/h), and Wind Barbs (kt)', loc='left')
# plt.title('Valid Time: {}'.format(date), loc='right')

chunk = 12
ind = (slice(None, None, chunk), slice(None, None, chunk))
u = ds_lev.sel(lev=500.0)["u"][ind[0], ind[1]]
v = ds_lev.sel(lev=500.0)["v"][ind[0], ind[1]]
u, v = smooth_uv(u, v)

lon = ds_lev.lon
lat = ds_lev.lat
ax.barbs(lon.values[ind[0]], lat.values[ind[1]],
         u.to('kt').m, v.to('kt').m,
        #  fill_empty = True, 
        #  length = 6, 
        #  barb_increments=dict(half=10, full=20, flag=100),
         sizes=dict(emptybarb=0, spacing=0.2, height=0.3),
        #  pivot='middle', 
         color='black', transform=ax.projection)


# 1. geoheight
geoheight = metpy.calc.geopotential_to_height(
    ds_lev.sel(lev=500.0)["z"])/10  # to dm
contourf_gph500(ax, geoheight)

plt.savefig("gph_500hpa.pdf")
plt.savefig("gph_500hpa.svg")
"ok"


# %% Figure 2. 
from rbase import *
fig = plt.figure(1, figsize=(13., 9.), constrained_layout=True, )
# multiple levels
# fig, axs = plt.subplots(2, 2, constrained_layout=True)
# axs = axs.flatten()
levs = [200, 500, 850]

for i in seq(0, 2):
    ax = plt.subplot(2, 2, i+1, projection=ccrs.PlateCarree())
    ax = setMapAxis_China(ax)
    # ax = ax.axes()
    lev = levs[i]
    z = metpy.calc.geopotential_to_height(
        ds_lev.sel(lev=lev)["z"])/10  # to dm
    lon = z.lon.values
    lat = z.lat.values
    # 1. add contour for gph
    cs = ax.contour(lon, lat, z)
    kw_clabels = {'fontsize': 11, 'inline': True, 'inline_spacing': 5, 'fmt': '%i',
                  'rightside_up': True, 'use_clabeltext': True}
    plt.clabel(cs, **kw_clabels)
    ax.set_title('{}hPa geopotential height (dm)'.format(lev))
    # contourf_gph500(ax, geoheight)

    # 2. add H, L for gph
    nsize = 100
    plot_maxmin_points(ax, z, nsize, "max", "H", "red")
    plot_maxmin_points(ax, z, nsize, "min", "L", "blue")

h = plt.suptitle('Valid Time: {}\n'.format(date), fontsize=16)
# h = h.set_y(0.95) # change height
plt.savefig("gph_multiple_levels.pdf")
plt.savefig("gph_multiple_levels.svg")
