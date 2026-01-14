#################### Run this script to generate Q2Q transformations from modelled and historical data
#
# Hay que habilitar las 3 versiones, que son las que se crean, y comentar la v0
#
# Este script COMPRUEBA antes de guardar que el archivo no existe, para evitar sobreescribir los ya existentes



import pandas as pd
import os
import sys
import pickle
import yaml


with open('../analyses.yaml', 'r') as f:
    dic_analyses = yaml.safe_load(f)


##### Import local functions
sys.path.append(os.path.abspath(os.path.join('..')))
import funs





#################### Parameters

data_path = '../data/'

##### Analysis case
# analysis = 'REF'
# analysis = 'cutout'
# analysis = 'cluster'
# analysis = 'onwindWT'
analysis = 'classes'





#################### Derived parameters

output_path = f'../q2q_repository/{analysis}/'
### Comprueba que existe, crear en caso contrario
if not os.path.exists(output_path):
    os.makedirs(output_path)





#################### Loop

carrier_list = dic_analyses['solartype_list']
carrier_list.append('onwind')



for carrier in carrier_list:

    ##### Path for analysis 'onwindWT', for which solar-hsat was not needed
    if analysis == 'onwindWT' and carrier == 'solar-hsat':
        print('>>>>>>>>>> PATCH for analysis onwindWT: ommitting carrier solar-hsat')
        continue


    for case in dic_analyses[f'{analysis}_list']:

        # For case equal to REF case, do nothing
        if case == dic_analyses.get('REF', {}).get(analysis):
            continue


        ##### Define 'year', required for historical data
        if analysis=='cutout':
            year = int(case[-4:])   ##### CHECK FOR CUTOUT ANALYSIS
        else:
            year = int(dic_analyses['REF']['cutout'][-4:])


        ##### Define 'carrier_target', que es el historical data que se coge: vale 'solar' cuando carrier es 'solar-hsat'
        if carrier == 'solar-hsat':
            carrier_target = 'solar'
        else:
            carrier_target = carrier


        ##### Load input data
        file_input = data_path + f'modelled_data/{analysis}/' + f'{carrier}_{case}.csv'
        df_input = pd.read_csv(file_input, index_col=0, parse_dates=True)


        ##### Load target data
        file_target = data_path + 'historical_data/' + f'{carrier_target}_{year}.csv'
        df_target = pd.read_csv(file_target, index_col=0, parse_dates=True)



        for q2q in ['q2qv1', 'q2qv2', 'q2qv3']:

            ##### Get version as string
            version = q2q[-2:]


            file_q2q = f'q2q_{carrier}_{case}_{version}.pkl'


            ##### Check if the output already exists    
            if os.path.exists(output_path+file_q2q):
                print(f'Skipping existing file: {file_q2q}')
                continue


            ##### Normalise data
            if version == 'v1':

                df_capacity = pd.read_csv(f'{data_path}/installed_capacity.csv', index_col='year')
                installed_capacity = df_capacity.at[year, carrier_target]

                df_input_norm = df_input.div(installed_capacity)
                df_target_norm = df_target.div(installed_capacity)


            if version == 'v2':

                x_max = max([df_input.max().max(),df_target.max().max()])

                df_input_norm = df_input.div(x_max)
                df_target_norm = df_target.div(x_max)


            if version == 'v3':

                input_max = df_input.max().max()
                target_max = df_target.max().max()

                df_input_norm = df_input.div(input_max)
                df_target_norm = df_target.div(target_max)    


            ##### Get the Q2Q transform
            q2q_transform = funs.fun_q2q_transform(df_input_norm, df_target_norm)


            ##### Save transform
            with open(output_path+file_q2q, 'wb') as f:
                pickle.dump(q2q_transform, f)
                
            print(f'Created q2q function: {file_q2q}')






