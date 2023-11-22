import pandas as pd

ENSO = pd.read_csv("enso_idx_original.txt", comment="#")

# Some definitions
var_name_output='enso_idx'
dt1="2001-01-01"; dt2="2022-12-01"                           # Common period between both sources
dates = pd.date_range(start=dt1, end=dt2, freq='MS')         # Build an array of all months within the period
dates = [(dt + pd.Timedelta(days=14)).strftime('%Y%m%d') for dt in dates]

# Create an empty Pandas dataframe filled with all dates and dummy values for variable (which will be updated later - faster)
DAT = pd.DataFrame(dates, columns=['date'])
DAT[var_name_output] = None
DAT.set_index("date", inplace=True)

irow=0; row=ENSO.iloc[irow]
for irow, row in ENSO.iterrows(): 
    m=0
    for m in range(12):
        dt = f"{int(row.YEAR)}{'{:02}'.format(m+1)}15"        # Set a date in the middle of the month
        DAT.loc[dt, var_name_output] = row.iloc[m+1]          # Update the row 

DAT.to_csv(f"{var_name_output}.csv", header=True)             # Save in CSV format


