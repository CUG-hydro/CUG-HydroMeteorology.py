# %%
from main_pkgs import *
import metpy
import metpy.calc as mpcalc


ds_surf_raw = xr.open_dataset("data/ERA5_202205_Asia_prcp.nc")
ds_surf = ds_surf_raw.resample(time = "6h", restore_coord_dims = True).sum()

ds_lev = xr.open_dataset("data/ERA5_202205_Asia.nc")
ds = ds_lev.merge(ds_surf, join="inner")

dates = xr_date(ds)
d = pd.DataFrame({
  "date": date(dates), 
  "hour": hour(dates),
})

dates
# geoheight = mpcalc.geopotential_to_height(ds_lev.sel(level=500.0)["z"])/10 # dm

# from datetime import timedelta
# time = dates[1] + timedelta(hours=1)

# %%
from rbase import *

def plot_main(i=0):
  time = dates[i]
  fig = plt.figure(1, figsize=(13., 9.), constrained_layout=True)
  fig.clf()
  # multiple levels
  # fig, axs = plt.subplots(2, 2, constrained_layout=True)
  # axs = axs.flatten()
  levs = [200, 500, 850]

  for k in seq(0, 2):
    ax = plt.subplot(2, 2, k+1, projection=ccrs.PlateCarree())
    # ax = setMapAxis_China(ax)
    # ax = ax.axes()
    if (k <= 2):
      lev = levs[k]
      
      d = ds.sel(level=lev, time = time)
      z = metpy.calc.geopotential_to_height(d["z"])/10  # dm, np.array
      z.values = gaussian_filter(z.values, sigma = 3)

      lon, lat = get_coords(z)
      # 1. add contour for gph
      by = 10 if lev < 500 else 4
      contour_z(z, lev=lev, half=10, by=by)
      # cs = ax.contour(lon, lat, z)
      # kw_clabels = {'fontsize': 11, 'inline': True, 'inline_spacing': 5, 'fmt': '%i',
      #               'rightside_up': True, 'use_clabeltext': True}
      # plt.clabel(cs, **kw_clabels)

      # 2. add H, L for gph
      nsize = (3/0.25)**2
      plot_maxmin_points(z, nsize, "max", "H", "red")
      plot_maxmin_points(z, nsize, "min", "L", "blue")
      ax.set_title('{}hPa geopotential height (dm)'.format(lev))
      ## wind
      add_wind(d, step=14, length = 5, linewidth=0.4)
      
      if lev >= 500:
        x = ds["tp"].sel(time = time)
        r_contourf(x*1000, brks = [0.1, 0.2, 0.5, 1, 2, 5], show_cbar=False)
    else:
      # wind
      x = ds["tp"].sel(time = time)
      r_contourf(x*1000, brks = [0.1, 0.2, 0.5, 1, 2, 5])

    add_china()

  h = plt.suptitle('Valid Time: {}'.format(time), fontsize=16)
  # h = h.set_y(0.95) # change height
  fout = "Figures/gph_multiple_levels_%02d.pdf" % i
  print(fout)
  write_fig(fout, 13, 8)
  # plt.savefig("gph_multiple_levels.svg")

n = length(dates)
[plot_main(i) for i in range(0, n)]
# plot_main(1)

# %%
# files = glob("Figures/*.pdf")
from rbase import *

pdfs = r_dir("Figures", "*.pdf")
merge_pdf(pdfs, "ERA5_gph_3levs.pdf", delete=False)

# imgs = r_dir("Figures/", "*.jpg")
# images2gif(imgs, "ERA5_prcp_202205.gif", duration=500)
# images2pdf(imgs, "ERA5_prcp_202205.pdf")
