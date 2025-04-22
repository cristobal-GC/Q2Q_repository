import pandas as pd
import os
import sys
import pickle


##### Import local functions
sys.path.append(os.path.abspath(os.path.join('..')))
import funs
#################### Populate q2q repository


########## Parameters

carrier_list = ['onwind', 'solar']

domain_list = ['iberia', 'europe']

year_dic = {'iberia': list(range(2016, 2024)),
            'europe': [2019, 2020, 2023]
            }

clustering_list = ['NUTS2', 'NUTS3']


path_data = '../data/'
path_outputs = '../q2q_repository/'


########## Loop

for carrier in carrier_list:

    for domain in domain_list:

        for year in year_dic[domain]:
            
            for clustering in clustering_list:

                ##### Load input data
                file_input = path_data + 'modelled_data/' + f'{carrier}_{domain}_{year}_{clustering}.csv'
                df_input = pd.read_csv(file_input, index_col=0, parse_dates=True)

                ##### Load target data
                file_target = path_data + 'historical_data/' + f'{carrier}_{year}.csv'
                df_target = pd.read_csv(file_target, index_col=0, parse_dates=True)


                ##### Get the Q2Q transform
                q2q_transform = funs.get_q2q_transform(df_input, df_target)


                ##### Save transform
                file_q2q = f'q2q_{carrier}_{domain}_{year}_{clustering}'
                with open(f'{path_outputs}{file_q2q}.pkl', 'wb') as f:
                    pickle.dump(q2q_transform, f)



