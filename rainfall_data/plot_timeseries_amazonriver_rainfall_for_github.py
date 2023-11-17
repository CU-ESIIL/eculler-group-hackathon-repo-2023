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

a = xr.open_dataset('/home/paula/ESIIL_HACKATON/MERGE_2015/20151001_20161114_rainfall_amazon.nc')
b = xr.open_dataset('/home/paula/ESIIL_HACKATON/20221001_20231114_rainfall_amazon.nc')


preca = a['prec'].mean(dim=['latitude','longitude']).data.copy()
precb = b['prec'].mean(dim=['latitude','longitude']).data.copy()

plt.figure()
plt.plot(preca,'k',alpha=0.5,linewidth=4,label='2015-10-01/2016-11-14')
plt.plot(precb,'r',alpha=0.6,linewidth=2,label='2022-10-01/2023-11-14')
plt.legend()
plt.xlabel('Time (Daily data)',fontsize=12)
plt.ylabel(r' Mean Precipitation [kg m$^{-2}$ s$^{-1}$]',fontsize=12)
plt.savefig('rainfall_in_amazon.png', dpi=300, bbox_inches='tight')
