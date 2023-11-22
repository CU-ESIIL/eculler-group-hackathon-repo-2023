#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 19:49:04 2022

Get MERGE Data from LAT: -3.5 to -5.5, LON:-68 to -44 

@author: jrmgarcia
"""

# Loading needed packages
import os
import requests as req
import pandas as pd
import numpy as np
import xarray as xr
import cfgrib

DATA_SRC='MERGE'  # SAMET (tp2m: min|med|max) or MERGE (rain)
lat1=-5.5; lat2=3.5; lon1=-68; lon2=-44                      # Limits of the bbox of the use case

if DATA_SRC == "MERGE":
   remote_root_fname = "http://ftp.cptec.inpe.br/modelos/tempo/MERGE/GPM/DAILY/YYYY/MM/MERGE_CPTEC_YYYYMMDD.grib2"
   var_name_output = 'prec'
   var_name_ds = 'prec'
   lon1 = 360 + lon1; lon2 = 360 + lon2;   # MERGE is 0:360
if DATA_SRC == "SAMET":
   remote_root_fname = "http://ftp.cptec.inpe.br/modelos/tempo/SAMeT/DAILY/TMED/YYYY/MM/SAMeT_CPTEC_TMED_YYYYMMDD.nc"
   var_name_output = 'tp2m_med'
   var_name_ds = 'tmed'

# Some definitions
dt1="2001-01-01"; dt2="2022-12-31"                           # Common period between both sources
dates = pd.date_range(start=dt1, end=dt2)                    # Build an array of all dates within the period

# Create an empty Pandas dataframe filled with dummy values (them, only updates the row - faster)
DAT = pd.DataFrame(dates, columns=['date'])
DAT['date'] = pd.to_datetime(DAT["date"]).dt.strftime('%Y%m%d')
DAT[var_name_output] = None

idt=0; dt=dates[idt]
# Download data from all dates, crop the bbox and compute the mean value
for idt, dt in enumerate(dates):
   print(var_name_output, ' ', var_name_ds, ' ', dt.strftime('%Y%m%d'), " (", idt+1, "/", len(dates), ")", sep="", flush=True)
   # Extract individual fields from the date being processed
   y = str(dt.year)
   m = str(dt.month).zfill(2)
   d = str(dt.day).zfill(2)
   
   # Set the name of the file to download and do it!
   url = f"{remote_root_fname}".replace("YYYY", y).replace("MM", m).replace("DD", d)
   fname = os.path.basename(url)

   # Try to process 5 times
   for i in range(5):
      try:
         r = req.get(url, allow_redirects=True)                            # Actually do the download here (but don't save)
         f = open(fname, 'wb').write(r.content)                            # Saving now!
         if DATA_SRC == "SAMET":
            ds = xr.open_dataset(fname)
         elif DATA_SRC == "MERGE":
            ds = cfgrib.open_dataset(fname)
            
         break    # Get out of the loop if ok
      except:
         pass


   # Get all data from inside the bbox and calculates the mean (crop the region of interest)
   if DATA_SRC == 'SAMET':
      ds2 = xr.Dataset(ds.sel(lat=slice(lat1, lat2), lon=slice(lon1, lon2)))  
   elif DATA_SRC == 'MERGE':
      ds2 = xr.Dataset(ds.sel(latitude=slice(lat1, lat2), longitude=slice(lon1, lon2)))
   reg_mean = float(ds2[var_name_ds].mean())                               # Compute the mean
   DAT.iloc[idt, 0:2] = [dt.strftime('%Y%m%d'), reg_mean]                  # Update the row  
   ds2.close(); ds.close()                                                 # Close the datasets
   os.remove(fname)          
   if DATA_SRC == 'MERGE':
      os.remove(f'{fname}.923a8.idx')
   
DAT.to_csv(f"{var_name_output}.csv", header=True, index=False)             # Save in CSV format
