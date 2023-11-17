import geopandas as gp
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import os.path as osp
import numpy as np
import sys
from dry_package.plot_schemes import maps
from matplotlib import rcParams
rcParams['font.size'] = 8


fshp = '/home/paula/Amazon_river_shapefile.shp'
fout = '/home/paula/figures/'

wshed = gp.read_file(fshp)

plt.close()
fig = plt.figure(figsize=[6.41, 4.05])
ax = maps.make_overall2(fig=fig,
                   extent=[-68.0,-44.0, -5.5, 3.5],
                   x_range=np.arange(-68, -44, 3.0),
                   y_range=np.arange(-5.5,3.5,1.0))
wshed.plot(ax=ax, alpha=0.5)
#river.plot(ax=ax, color='r', linewidth=0.5)
ax.coastlines(linewidth=0.5)

#ax1 = maps.insert_transect_minimap(fig,ax,
                                  #projection=ccrs.Orthographic(-48, -24.5),
                                  #xywidth=[0.87, 0.25,0.4])
#ax1.set_global()
#ax1.coastlines('50m', edgecolor='black', linewidth=0.1)
#ax1.scatter(-48, -24.5)
plt.ion()
#plt.show()
plt.tight_layout()
plt.savefig(osp.join(fout, 'bh_rios_zoom_paula_amazon_watershed.png'), dpi=300, bbox_inches='tight')
