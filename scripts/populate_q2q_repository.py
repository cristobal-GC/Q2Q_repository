import pandas as pd
import os
import sys
import pickle


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


path_data = '../data/'
path_outputs = '../q2q_repository/'



########## Loop

for carrier in carrier_list:

    for domain in domain_list:

        # To define year_list, consider de intersection for the years of the specific domain, and all the carriers
        year_dic_local = {k: v for k, v in year_dic.items() if k in [domain]+carrier_list}
        
        year_list = set.intersection(*[set(year_list_local) for year_list_local in year_dic_local.values()])

        # print(f'year_list = {year_list}')


        for year in year_list:
            
            for clustering in clustering_list:
            
                ##### Load input data
                file_input = path_data + 'modelled_data/' + f'{carrier}_{domain}_{year}_{clustering}.csv'
                df_input = pd.read_csv(file_input, index_col=0, parse_dates=True)

                ##### Load target data
                file_target = path_data + 'historical_data/' + f'{carrier}_{year}.csv'
                df_target = pd.read_csv(file_target, index_col=0, parse_dates=True)


                for norm_version in norm_version_list:


                    file_q2q = f'q2q_{carrier}_{domain}_{year}_{clustering}_{norm_version}.pkl'


                    ##### Check if the output already exists    
                    if os.path.exists(path_outputs+file_q2q):
                        print(f'Skipping existing file: {file_q2q}')
                        continue


                    ##### Normalise data
                    if norm_version == 'v1':

                        df_capacity = pd.read_csv('../data/installed_capacity.csv', index_col='year')
                        installed_capacity = df_capacity.at[year, carrier]

                        df_input_norm = df_input.div(installed_capacity)
                        df_target_norm = df_target.div(installed_capacity)


                    if norm_version == 'v2':

                        x_max = max([df_input.max().max(),df_target.max().max()])

                        df_input_norm = df_input.div(x_max)
                        df_target_norm = df_target.div(x_max)


                    if norm_version == 'v3':

                        input_max = df_input.max().max()
                        target_max = df_target.max().max()

                        df_input_norm = df_input.div(input_max)
                        df_target_norm = df_target.div(target_max)    


                    ##### Get the Q2Q transform
                    q2q_transform = funs.fun_q2q_transform(df_input_norm, df_target_norm)


                    ##### Save transform
                    with open(path_outputs+file_q2q, 'wb') as f:
                        pickle.dump(q2q_transform, f)
                        
                    print(f'Created q2q function: {file_q2q}')



