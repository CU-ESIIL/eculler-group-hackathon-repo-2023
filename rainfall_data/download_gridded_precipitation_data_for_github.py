"""Script to download rainfall gridded data from MERGE CPTEC shapefile for Amazon watershed"""
import shutil
import urllib.request as request
from contextlib import closing
import pandas as pd
from dask.diagnostics import ProgressBar
import datetime as dtt
import os
import os.path as osp
import xarray as xr
import salem
import geopandas as gp
from shapely.geometry import box
ProgressBar().register()

tag = 'Amazon_river'

# -- paths --#
fsave = '/data-store/iplant/home/paulabirocchi/rainfall_data/'
ftpstr = 'http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/DAILY'
fshp = '/data-store/iplant/home/paulabirocchi/watershed_shapefiles/HydroRIVERS_v10_sa.shp'

# -- time period -- #
tperiod = pd.date_range(start='2015/10/01', end='2016/11/14', freq='1D')


# --  configure ftp paths -- #
str_tmplt=f'{ftpstr}/%Y/%m/MERGE_CPTEC_%Y%m%d.grib2' # str template
merge_list = [dtt.datetime.strftime(i, str_tmplt) for i in tperiod] # ftp paths



for ffile in merge_list:
    fout = ffile.split('/')[-1]  # str: get the grib2 file name
    fgrib = osp.join(fsave, fout)  # str: saving path + grib2 filename
    fnc = osp.join(fsave, fout[:-6] + '.nc')  # str: rename  grib2 to nc

    # -- ftp download -- #
    with closing(request.urlopen(ffile)) as r:
        with open(fgrib, 'wb') as f:
            shutil.copyfileobj(r, f)

    # xr.dataset: read grib2 with xarray and cfgrib engine
    nc = xr.open_dataset(fgrib, engine='cfgrib')
    nc.to_netcdf(fnc)

    # cut to amazon river longitude and latitude
    nc = salem.open_xr_dataset(fnc)

    # longitude correction
    nc1 = nc.assign_coords({'longitude': nc['longitude']-360})

    # cut the data into a corners ((lon,lat), (lon,lat))
    nc2 = nc1.salem.subset(corners=((-68, -5.5), (-44, 3.5)), crs=salem.wgs84)

    nc2.to_netcdf(path=f'{fnc[:-3]}_{tag}.nc')
    os.system(f'rm {fsave}/*grib2 {fsave}/*idx {fnc}')
