import geopandas as gp
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import os.path as osp
import numpy as np
import sys

from dry_package.plot_schemes import maps
import xarray as xr
from cmocean import cm
from matplotlib import rcParams
rcParams['font.size'] = 8

ppt = 'MERGE_CETEC_RdI_2016.nc'
fout = '/home/paula/'

nc = xr.open_dataset(ppt)
#river = gp.read_file(rshp)

plt.close()

plt.close()
fig = plt.figure(figsize=[6.41, 4.05])
ax = maps.make_overall2(fig=fig,
                   extent=[-68.0,-44.0, -5.5, 3.5],
                   x_range=np.arange(-68, -44, 3.0),
                   y_range=np.arange(-5.5,3.5,1.0))
#wshed.plot(ax=ax, alpha=0.5)
#river.plot(ax=ax, color='r', linewidth=0.5)
ax.coastlines(linewidth=0.5)
pc = ax.pcolor(nc['longitude'], nc['latitude'], nc['prec'].mean(axis=0), cmap=cm.rain)
# nc['prec'].mean(axis=0).plot(ax=ax, alpha=0.5, cmap=cm.rain, add_colorbar=False)
#river.plot(ax=ax, color='r', linewidth=0.5)
ax.coastlines(linewidth=0.5)
cb = plt.colorbar(pc, pad=0.025, fraction=0.05)
cb.set_label(r'Precipitation [kg m$^{-2}$ s$^{-1}$]')
pc.set_clim(0, 13) 
# ax1 = maps.insert_transect_minimap(fig,ax,
#                                   projection=ccrs.Orthographic(-48, -24.5),
#                                   xywidth=[0.87, 0.25,0.4])
# ax1.set_global()
# ax1.coastlines('50m', edgecolor='black', linewidth=0.1)
# ax1.scatter(-48, -24.5)
plt.ion()
plt.show()
plt.tight_layout()
plt.subplots_adjust(top=1.0,
bottom=0.037,
left=0.082,
right=0.936,
hspace=0.2,
wspace=0.2)
plt.savefig(osp.join(fout, 'ppt_rios_amazon_river_2016.png'), dpi=300, bbox_inches='tight')
