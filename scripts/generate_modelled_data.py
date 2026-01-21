#################### Run this script to generate modelled time series from resolved PyPSA-Spain networks
#
#
# The first time it is run (STEP 2) is to obtain the data modeled according to pypsa-eur, therefore with only one column: ‘q2qNo’.
#
# This can be used to generate the Q2Q transformations, which are then used to run this script a second time with four columns (one without q2q, three with q2q).
#
#


import pandas as pd
import pypsa
import os
import yaml


with open('../analyses.yaml', 'r') as f:
    dic_analyses = yaml.safe_load(f)





#################### Parameters

pypsa_path = '../pypsa-spain/'


##### Analysis case. Comment all but one
#analysis = 'REF'
#analysis = 'cutout'
#analysis = 'cluster'
#analysis = 'onwindWT'
analysis = 'classes'


##### Set q2q list. Comment all but one
#q2q_list = ['q2qNo']                                 # STEP 2
q2q_list = ['q2qNo', 'q2qv1', 'q2qv2', 'q2qv3']       # STEP 6



#################### Derived parameters

output_path = f'../data/modelled_data/{analysis}/'
### Check that it exists, create it if it does not
if not os.path.exists(output_path):
    os.makedirs(output_path)



#################### Loop to generate CSV files with time series

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


