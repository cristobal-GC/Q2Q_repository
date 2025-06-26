

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import sys
import os
import numpy as np
import xarray as xr


##### Import local functions
sys.path.append(os.path.abspath(os.path.join('')))
import funs


########## Parameters
version_list = ['', '_q2q_v1', '_q2q_v2', '_q2q_v3']
version_list_nice_names = ['no_q2q', 'q2q_v1', 'q2q_v2', 'q2q_v3']
version_list_nice_names_complete = ['historical'] + version_list_nice_names

clustering_list = ['NUTS2', 'NUTS3']

carrier_list = ['onwind', 'solar']

domain_list = ['iberia', 'europe']

year_list = list(range(2016, 2024))



########## Load installed capacities
cap_path = 'data/'
cap_file = 'installed_capacity.csv'

df_capacity = pd.read_csv(cap_path+cap_file, index_col=0)


########## Create CFs container
CF = xr.DataArray(
    np.empty((len(version_list_nice_names_complete), 
              len(clustering_list), 
              len(carrier_list), 
              len(domain_list), 
              len(year_list))
            ),
    coords={
            'version': version_list_nice_names_complete,
            'clustering': clustering_list,
            'carrier': carrier_list,
            'domain': domain_list,
            'year': year_list,
            },
    dims=['version', 'clustering', 'carrier', 'domain', 'year']
)



########## Create RMSE container
RMSE = xr.DataArray(
    np.empty((len(version_list_nice_names), 
              len(clustering_list), 
              len(carrier_list), 
              len(domain_list), 
              len(year_list))
            ),
    coords={
            'version': version_list_nice_names,
            'clustering': clustering_list,
            'carrier': carrier_list,
            'domain': domain_list,
            'year': year_list,
            },
    dims=['version', 'clustering', 'carrier', 'domain', 'year']
)





########## Retrieve CFs, RMSEs

for carrier in carrier_list:

    for year in year_list:

        ### Load historical data
        hist_path = 'data/historical_data/'
        hist_file = f'{carrier}_{year}.csv'    
        df_historical = pd.read_csv(hist_path+hist_file, index_col=0, parse_dates=True)
        ### Historical data were obtained 'tz-aware' to impose UTC+00. Make it 'tz-naive'
        df_historical.index = df_historical.index.tz_localize(None)
        ### Rename value to value_historical
        df_historical.rename(columns={'value': 'value_historical'}, inplace=True)


        for domain in domain_list:
            
            for clustering in clustering_list:

                ### If modelled data exists
                mod_path = 'data/modelled_data/'
                mod_file = f'{carrier}_{domain}_{year}_{clustering}.csv'

                if os.path.exists(mod_path+mod_file):

                    ### Load modelled data, and rename no_q2q column
                    df_modelled = pd.read_csv(mod_path+mod_file, index_col=0, parse_dates=True)
                    df_modelled.rename(columns={'value': 'value_no_q2q'}, inplace=True)
                    
                    ### Join historial and modelled data in case there is some date mismatch
                    df = df_historical.join(df_modelled, how='inner')
                    

                    for version in version_list_nice_names_complete:

                        y_true = df['value_historical']
                        y_pred = df[f'value_{version}']

                        y_true_adim = y_true/df_capacity.at[year,carrier]
                        y_pred_adim = y_pred/df_capacity.at[year,carrier]

                        if version == 'historical':

                            CF.loc[version,clustering,carrier,domain,year] = np.mean(y_true_adim)

                        else:

                            CF.loc[version,clustering,carrier,domain,year] = np.mean(y_pred_adim)
                            RMSE.loc[version,clustering,carrier,domain,year] = funs.fun_rmse(y_true_adim, y_pred_adim)
                            

##### Replace residuals with NaNs
threshold = 1e-10
CF.values[np.abs(CF.values) < threshold] = np.nan
RMSE.values[np.abs(RMSE.values) < threshold] = np.nan





########## CF plots
for carrier in carrier_list:

    for clustering in clustering_list:

        for domain in domain_list:


            CF_subset = CF.sel(clustering=clustering,
                            carrier=carrier,
                            domain=domain,
                            )

            df = CF_subset.to_pandas().T


            ########## Make plot
            plt.rc('font', size=16)
            fig, ax = plt.subplots(1,1,figsize=(10,6))

            df.drop(columns=['historical']).plot(ax=ax, kind='bar')

            j=0
            for i, year in enumerate(df.index):  # df.index son los años
                value = df.at[year,'historical']
                if not np.isnan(value):
                    if j == 0:
                        ax.hlines(value, i - 0.4, i + 0.4, colors='black', linestyles='dashed', label='Historical')
                        j+=1
                    else:
                        ax.hlines(value, i - 0.4, i + 0.4, colors='black', linestyles='dashed')

            ax.set_xlabel('Year')
            ax.set_title(f'CF - {carrier}\ncutout={domain} , clustering={clustering}')
            ax.grid(True, linestyle='--', linewidth=0.5, color='black', alpha=0.25)
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')


            ##### Export figure
            fig_path = 'figs/evaluation/CF/'
            fig_name = f'CF_{carrier}_{domain}_{clustering}.jpg'

            fig.tight_layout()
            plt.savefig(fig_path+fig_name)
            plt.close()



########## RMSE plots
for carrier in carrier_list:

    for clustering in clustering_list:

        for domain in domain_list:


            RMSE_subset = RMSE.sel(clustering=clustering,
                            carrier=carrier,
                            domain=domain,
                            )

            df = 100*RMSE_subset.to_pandas().T


            ########## Make plot
            plt.rc('font', size=16)
            fig, ax = plt.subplots(1,1,figsize=(10,6))

            df.plot(ax=ax, kind='bar')
        
            ax.set_xlabel('Year')
            ax.set_ylabel('% Installed capacity')
            ax.set_title(f'RMSE - {carrier}\ncutout={domain} , clustering={clustering}')
            ax.grid(True, linestyle='--', linewidth=0.5, color='black', alpha=0.25)
            ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')


            ##### Export figure
            fig_path = 'figs/evaluation/RMSE/'
            fig_name = f'RMSE_{carrier}_{domain}_{clustering}.jpg'

            fig.tight_layout()
            plt.savefig(fig_path+fig_name)
            plt.close()




