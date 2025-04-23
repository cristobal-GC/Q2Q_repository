import pandas as pd
import os
import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt


##### Import local functions
sys.path.append(os.path.abspath(os.path.join('..')))
import funs



########## Parameters

carrier_list = ['onwind', 'solar']

domain_list = ['iberia', 'europe']

year_dic = {'iberia': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023], # 2024 doesn't run
            'europe': [1996, 2010, 2012, 2013, 2019, 2020, 2023], # sarah3-era5
            'onwind': [2011, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024], # historical data
            'solar': [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024], # historical data
            }

clustering_list = ['NUTS2', 'NUTS3']

norm_version_list = ['v1', 'v2', 'v3']


path_inputs = '../q2q_repository/'



########## Loop

for carrier in carrier_list:

    for domain in domain_list:

        # To define year_list, consider de intersection for the years of the specific domain, and all the carriers
        year_dic_local = {k: v for k, v in year_dic.items() if k in [domain]+carrier_list}
        
        year_list = set.intersection(*[set(year_list_local) for year_list_local in year_dic_local.values()])

        # print(f'year_list = {year_list}')


        for year in year_list:
            
            for clustering in clustering_list:

                for norm_version in norm_version_list:


                    ### Define (and create if required) output path
                    path_outputs = f'../figs/q2q_transforms/{domain}/{clustering}/{carrier}/{norm_version}/'
                    if not os.path.exists(path_outputs):
                        os.makedirs(path_outputs)

                    
                    ##### Load and plot q2q
                    file_q2q = f'q2q_{carrier}_{domain}_{year}_{clustering}_{norm_version}.pkl'

                    with open(path_inputs+file_q2q, 'rb') as f:
                        q2q_transform = pickle.load(f)

                        ### Get interpolated data
                        x_values = np.linspace(0, 1, 1000)
                        y_values = q2q_transform(x_values)


                        ### Make figure
                        fig, ax = plt.subplots(figsize=(6,6))

                        ax.scatter(x_values,y_values,s=5)
                        ax.plot([0, 1],[0, 1],color='black',alpha=0.25)

                        #ax.set_title(f'Q2Q transform \n Normalisation scheme {i+1}')
                        ax.set_xlabel('input')
                        ax.set_ylabel('output')
                        ax.grid(True, linestyle='--', linewidth=0.5, color='black', alpha=0.25)


                        ##### Export figure
                        file_output = f'q2q_{carrier}_{domain}_{year}_{clustering}_{norm_version}.jpg'
                        fig.tight_layout()

                        plt.savefig(path_outputs+file_output)
                        plt.close()

