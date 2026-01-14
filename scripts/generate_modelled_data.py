#################### Run this script to generate modelled time series from resolved pypsa networks
#
#
# La primera vez que se corre (PASO 2) es para obtener los datos modelados según pypsa-eur, por tanto solo con una columna: 'q2qNo'
#
# Con esto se pueden generar las Q2Q transforms, que luego se emplean para correr este script por segunda vez ya con 4 columnas, (1 sin q2q, 3 con q2q)
#
#
# Este script NO COMPRUEBA antes de guardar que el archivo no existe, por lo que sobreescribe. Esto es necesario para que en el paso 6 sobreescriba el output del paso 2, ampliando el dataframe con las columnas de q2qX



import pandas as pd
import pypsa
import os
import yaml


with open('../analyses.yaml', 'r') as f:
    dic_analyses = yaml.safe_load(f)





#################### Parameters

pypsa_path = '../pypsa-spain/'


##### Analysis case
#analysis = 'REF'
#analysis = 'cutout'
#analysis = 'cluster'
#analysis = 'onwindWT'
analysis = 'classes'





##### Set q2q list. Comment all but one
#q2q_list = ['q2qNo']                                 # PASO 2
q2q_list = ['q2qNo', 'q2qv1', 'q2qv2', 'q2qv3']       # PASO 6



#################### Derived parameters

output_path = f'../data/modelled_data/{analysis}/'
### Comprueba que existe, crear en caso contrario
if not os.path.exists(output_path):
    os.makedirs(output_path)





#################### Loop para generar los archivos csv con las series temporales


for solartype in dic_analyses['solartype_list']:

    ##### Path for analysis 'onwindWT', for which solar-hsat was not needed
    if analysis == 'onwindWT' and solartype == 'solar-hsat':
        print('>>>>>>>>>> PATCH for analysis onwindWT: ommitting solartype solar-hsat')
        continue


    ##### Define carrier list
    carrier_list = ['onwind', solartype]



    for case in dic_analyses[f'{analysis}_list']:

        # For case equal to REF case, do nothing
        if case == dic_analyses.get('REF', {}).get(analysis):
            continue


        ##### Create a dic of dataframes, one per carrier
        dic_dfs = {f'df_{carrier}': pd.DataFrame() for carrier in carrier_list}



        for q2q in q2q_list:

            ##### Load network
            input_path = f'results/{case}_{solartype}_{q2q}/networks/'

            ## Retrieve file name, chech there is only one file and take this name
            files = [f for f in os.listdir(pypsa_path+input_path) if os.path.isfile(os.path.join(pypsa_path+input_path, f))]

            if len(files) == 1:
                input_file = files[0]
            else:
                raise ValueError(f"The number of files in '{path}' is {len(files)}, rather than 1.")

            n = pypsa.Network(pypsa_path+input_path+input_file)


            ########## retrieve time series
            for carrier in carrier_list:

                dic_dfs[f'df_{carrier}'][f'{q2q}'] = n.generators_t['p'].filter(like=carrier).sum(axis=1)


            ########## round to 2 decimals and save df
            for carrier in carrier_list:

                df = dic_dfs[f'df_{carrier}']

                output_file = f'{carrier}_{case}.csv'   ##### Ommitting solar_type because not required

                print(f"##### Exporting file {output_path+output_file}...")
                df.round(2).to_csv(output_path+output_file)


