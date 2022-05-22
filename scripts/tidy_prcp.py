# %%
import numpy as np
import xarray as xr
import pandas as pd
import datetime
from rbase import *


f = "ERA5_202205_Asia_prcp.nc"
ds_raw = xr.open_dataset(f)
dates = xr_date(ds_raw)
d = pd.DataFrame({
  "date": date(dates), 
  "hour": hour(dates),
})
d

ds = ds_raw.resample(time = "6h", restore_coord_dims = True).sum()
dates = xr_date(ds)
# .transpose("longitude", "latitude", "time")

# %%
from rbase import *
from matplotlib.animation import FuncAnimation

def plot_prcp(i):
  fig = plt.figure(1, figsize=(10., 7.2), constrained_layout=True, dpi=200)
  fig.clf()
  ax = plt.axes(projection=ccrs.PlateCarree())

  date = dates[i]
  x = ds["tp"].isel(time = i)
  contourf_prcp(ax, x*1000, brks = [0.1, 0.2, 0.5, 1, 2, 5])

  ax = add_China(ax, range = [75, 160, 5, 55])
  plt.title('Valid Time (UTC): {}\n'.format(date) + 
      '500-hPa Geopotential Heights (contour, dm), surface precipitation (fill, mm/6h), and Wind Barbs (kt)', loc='left', fontsize = 13)
  # return ax
  outdir = "Figures/"
  fout = "%s/ERA5_prcp_%02d.jpg" % (outdir, i)
  print(fout)
  plt.savefig(fout)

# anim = FuncAnimation(fig, plot_prcp,
#                     # init_func = init,
#                     frames = 10,
#                     interval = 100)
# init_func = init, blit = True
# anim.save('continuousSineWave.gif',
#           writer = 'ffmpeg', fps = 30)
n = length(dates)
[plot_prcp(i) for i in range(0, n)]

# %%
# files = glob("Figures/*.pdf")
from rbase import *

# pdfs = r_dir("Figures", "*.pdf")
# merge_pdf(pdfs, "ERA5_prcp.pdf", delete=False)
imgs = r_dir("Figures/", "*.jpg")
images2gif(imgs, "ERA5_prcp_202205.gif", duration=500)
# images2pdf(imgs, "ERA5_prcp_202205.pdf")
