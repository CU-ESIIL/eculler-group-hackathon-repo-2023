# %%
import pandas as pd
import matplotlib.pyplot as plt

DAT = pd.read_csv("tp2m_med.csv")
enso = pd.read_csv("enso_idx.csv")
prec = pd.read_csv("prec.csv")

DAT['date'] = [str(dt)[0:6] for dt in DAT['date']]
enso['date'] = [str(dt)[0:6] for dt in enso['date']]
prec['date'] = [str(dt)[0:6] for dt in prec['date']]

DAT = pd.DataFrame(DAT.groupby('date')['tp2m_med'].mean())
enso = pd.DataFrame(enso.groupby('date')['enso_idx'].mean())
prec = pd.DataFrame(prec.groupby('date')['prec'].mean())

DAT = DAT.merge(enso, how='left', left_index=True, right_index=True).merge(prec, how='left', left_index=True, right_index=True)

# copy the data 
DAT_z_scaled = DAT.copy() 
# apply normalization techniques 
for column in DAT_z_scaled.columns: 
    DAT_z_scaled[column] = (DAT_z_scaled[column] -
                           DAT_z_scaled[column].mean()) / DAT_z_scaled[column].std()  

DAT_z_scaled.plot()
plt.title('TS for Solimões rivers use case', fontsize=20)

import seaborn as sns
columns = ['tp2m_med', 'enso_idx', 'prec']
sns.pairplot(DAT[columns])

# %%
