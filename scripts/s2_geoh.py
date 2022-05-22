# %%
from main_pkgs import *

ds_raw = xr.open_dataset("data/ERA5_202205_Asia_prcp.nc")
dates = xr_date(ds_raw)
d = pd.DataFrame({
  "date": date(dates), 
  "hour": hour(dates),
})
d

ds = ds_raw.resample(time = "6h", restore_coord_dims = True).sum()
dates = xr_date(ds)

ds
# .transpose("longitude", "latitude", "time")
ds_lev = xr.open_dataset("data/ERA5_202205_Asia.nc")
ds_lev

xr_date(ds_lev)
xr_date(ds)
# z = ds_lev["z"].sel(level = 500)
# z
# import metpy
import metpy.calc as mpcalc

geoheight = mpcalc.geopotential_to_height(
    ds_lev.sel(level=500.0)["z"])/10  # to dm
geoheight


# %%

from datetime import timedelta
time = dates[1] + timedelta(hours=1)

# %%
from rbase import *

def plot_prcp(i = 0):
  # figsize=(10., 7.2)
  fig = plt.figure(1, constrained_layout=True, dpi=200)
  fig.clf()
  ax = plt.axes(projection=ccrs.PlateCarree())

  time = dates[i]
  # x = ds["tp"].isel(time = i)  
  # r_contourf(ax, x*1000, brks = [0.1, 0.2, 0.5, 1, 2, 5])
  try:
    # geoheight.sel(time = time)
    z = geoheight.sel(time = time)
    contour_z500(z, half=20)

    nsize = 100
    plot_maxmin_points(z, nsize, "max", "H", "red")
    plot_maxmin_points(z, nsize, "min", "L", "blue")
  except:
    print("No geoheight data in that time!")

  ax = add_China(range = [75, 160, 5, 55])
  plt.title('Valid Time (UTC): {}\n'.format(time) + 
      '500-hPa Geopotential Heights (contour, dm), surface precipitation (fill, mm/6h), and Wind Barbs (kt)', loc='left', fontsize = 13)
  
  # return ax
  outdir = "Figures/"
  fout = "%s/ERA5_z500_%02d.pdf" % (outdir, i)
  print(fout)
  write_fig(fout, 10, 7.2, forward=True)
  # plt.savefig(fout)

n = length(dates)
# [plot_prcp(i) for i in range(0, n)]
plot_prcp()

## TODO: 绘制高压中心和低压中心

# %%
# files = glob("Figures/*.pdf")
from rbase import *

# pdfs = r_dir("Figures", "*.pdf")
# merge_pdf(pdfs, "ERA5_prcp.pdf", delete=False)
imgs = r_dir("Figures/", "*.jpg")
images2gif(imgs, "ERA5_prcp_202205.gif", duration=500)
# images2pdf(imgs, "ERA5_prcp_202205.pdf")
