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





########## Make heatmaps

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
                    

                    for version in version_list_nice_names:

                        y_true = df['value_historical']
                        y_pred = df[f'value_{version}']

                        y_true_adim = y_true/df_capacity.at[year,carrier]
                        y_pred_adim = y_pred/df_capacity.at[year,carrier]


                        e_adim = y_true_adim - y_pred_adim


                        ##### Make figure
                        fig_size = [12, 8]  # 3 subplots en una fila, más ancho
                        fig, axes = plt.subplots(1, 4, figsize=fig_size, sharey=True, constrained_layout=True)

                        vmins = []
                        vmaxs = []
                        errors = []


                        ##### Get min and max over the different versions
                        for version in version_list_nice_names:
                            y_true = df['value_historical']
                            y_pred = df[f'value_{version}']
                            y_true_adim = y_true / df_capacity.at[year, carrier]
                            y_pred_adim = y_pred / df_capacity.at[year, carrier]
                            e_adim = y_true_adim - y_pred_adim
                            errors.append(e_adim.values.reshape(365, 24))
                            vmins.append(e_adim.min())
                            vmaxs.append(e_adim.max())

                        abs_max = max(abs(min(vmins)), abs(max(vmaxs)))
                        vmin = -abs_max
                        vmax = abs_max


                        # Dibujar subgráficas
                        for ax, version, e_adim_reshaped in zip(axes, version_list_nice_names, errors):
                            im = ax.imshow(e_adim_reshaped, aspect='auto', cmap='PiYG', vmin=vmin, vmax=vmax)   ##### coolwarm / seismic / PiYG
                            ax.set_xlabel('Hour of the Day')
                            ax.set_title(f'{version}')
                            if ax == axes[0]:
                                ax.set_ylabel('Day of the Year')

                        # Colorbar común
                        cbar = fig.colorbar(im, ax=axes.ravel().tolist(), label='CF error (real - model)')



                        # Título general
                        fig.suptitle(f'{carrier}, {year}, {domain}, {clustering}', fontsize=14)

                        fig_path = 'figs/evaluation/error_t/'
                        fig_name = f'error_t_{domain}_{clustering}_{carrier}_{year}_all_versions.jpg'
                        plt.savefig(fig_path + fig_name)
                        plt.close()



