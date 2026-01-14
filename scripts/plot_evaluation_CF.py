#################### Run this script to generate plots for evaluating the modelled data: CFs
#
# Este script NO COMPRUEBA si la figura existe, la sobreescribe



import pandas as pd
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import yaml


with open('../analyses.yaml', 'r') as f:
    dic_analyses = yaml.safe_load(f)


##### Import local functions
sys.path.append(os.path.abspath(os.path.join('..')))
import funs





#################### Parameters

##### Define analyses to consider (except REF)
analysis_vector = [
                   #'cutout',
                   #'cluster',
                   #'onwindWT',
                   'classes',
                   ]


# hCF time series
date_in = "03-01"
date_out = "03-10"




#################### Loop in analysis

for analysis in analysis_vector:

    print(f'#################### Evaluating: {analysis} ####################')
        

    ########## Load installed capacities (required for hourly CF determination)
    cap_path = '../data/'
    cap_file = 'installed_capacity.csv'

    df_capacity = pd.read_csv(cap_path+cap_file, index_col=0)




    #################### Loop in carrier
    carrier_list = dic_analyses['solartype_list']
    carrier_list.append('onwind')

    for carrier in carrier_list:


        ##### Patch for analysis 'onwindWT', for which solar-hsat is not needed
        if analysis == 'onwindWT' and carrier == 'solar-hsat':
            print('>>>>>>>>>> PATCH for analysis onwindWT: ommitting carrier solar-hsat')
            continue



        ##### Create empty dataframes to store results: df_CF , df_cf_errors
        df_CF = pd.DataFrame()
        df_CF_errors = pd.DataFrame()


        for case in dic_analyses[f'{analysis}_list']:

            ##### Use analysis_local and case_local for case matching the REF case
            if case == dic_analyses.get('REF', {}).get(analysis):
                analysis_local = 'REF'
                case_local = 'REF'
            else:
                analysis_local = analysis
                case_local = case


            ##### Define 'year', required for historical data
            if analysis=='cutout':
                year = int(case[-4:])
            else:
                year = int(dic_analyses['REF']['cutout'][-4:])


            ##### Define 'carrier_target', to use for historical data ('solar' if carrier is 'solar-hsat')
            if carrier == 'solar-hsat':
                carrier_target = 'solar'
            else:
                carrier_target = carrier



            ##### Load historical data
            historical_data_path = f'../data/historical_data/'
            historical_data_file = f'{carrier_target}_{year}.csv'
            df_historical = pd.read_csv(historical_data_path+historical_data_file, index_col=0, parse_dates=True)
            ### Historical data were obtained 'tz-aware' to impose UTC+00. Make it 'tz-naive'
            df_historical.index = df_historical.index.tz_localize(None)
            ### Rename value to historical
            df_historical.rename(columns={'value': 'historical'}, inplace=True)



            ##### Load modelled data
            modelled_data_path = f'../data/modelled_data/{analysis_local}/'
            modelled_data_file = f'{carrier}_{case_local}.csv'
            df_modelled = pd.read_csv(modelled_data_path+modelled_data_file, index_col=0, parse_dates=True)



            ##### Get df_hCF: hourly capacity factors, by joinning historial and modelled data, and normalising
            #
            ### df_hCF is a datraframe with hourly capacity factors, and the following columns:
            #
            #   index:timestamps | historical | q2qNo | q2qv1 | q2qv2 | q2qv3
            #
            df_hCF = df_historical.join(df_modelled, how='inner').div(df_capacity.at[year,carrier_target])




            #################### FIGURE: time series for hourly CFs
            funs.fun_plot_hCF_ts(df_hCF, carrier, case, analysis, date_in, date_out)


            #################### FIGURE: Duration curves of hourly CF errors
            funs.fun_plot_hCF_durationCurves(df_hCF, carrier, case, analysis, dic_analyses['colors'])


            #################### FIGURE: heatmap of hourly CF errors
            funs.fun_plot_hCF_errors(df_hCF, carrier, case, analysis)



            ##### Populate df_CF and df_CF_errors with aggregated data from df_hCF
            df_CF[case] = df_hCF.mean().T
            df_CF_errors[case] = df_hCF.iloc[:, 1:].apply(lambda col: funs.fun_rmse(df_hCF.iloc[:, 0], col))



        ##### Get df_CF: capacity factors
        #
        ### df_CF is a datraframe with capacity factors, and the following columns:
        #
        #   index:cases | historical | q2qNo | q2qv1 | q2qv2 | q2qv3
        #
        ##### Get df_CF_errors: RMSE with respect to historical
        #
        #   index:cases | q2qNo | q2qv1 | q2qv2 | q2qv3
        #
        df_CF = df_CF.T
        df_CF_errors = df_CF_errors.T



        #################### FIGURE: bars for CFs
        funs.fun_plot_CF(df_CF, carrier, analysis)


        #################### FIGURE: bars for CF errors
        funs.fun_plot_CF_errors(df_CF_errors, carrier, analysis)







