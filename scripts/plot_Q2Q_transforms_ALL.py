#################### Run this script to generate plots of the Q2Q transformations
#
# Hay que habilitar las 3 versiones, que son las que se crean, y comentar la v0
#
# Este script NO COMPRUEBA si la figura existe, la sobreescribe



import pandas as pd
import os
import sys
import pickle
import numpy as np
import matplotlib.pyplot as plt
import yaml


with open('../analyses.yaml', 'r') as f:
    dic_analyses = yaml.safe_load(f)


##### Import local functions
sys.path.append(os.path.abspath(os.path.join('..')))
import funs





#################### Parameters

##### Analysis case (except REF)
# analysis = 'cutout'
# analysis = 'cluster'
# analysis = 'onwindWT'
analysis = 'classes'





#################### Loop

carrier_list = dic_analyses['solartype_list']
carrier_list.append('onwind')



for carrier in carrier_list:

    ##### Path for analysis 'onwindWT', for which solar-hsat was not needed
    if analysis == 'onwindWT' and carrier == 'solar-hsat':
        print('>>>>>>>>>> PATCH for analysis onwindWT: ommitting carrier solar-hsat')
        continue


    # Crear figura con una fila y 3 columnas de subplots (una por cada q2q)
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))



    for case in dic_analyses[f'{analysis}_list']:

        #####  Possible reformulation of case and analysis (equal or not to the REF case)
        if case == dic_analyses.get('REF', {}).get(analysis):
            analysis_local = 'REF'
            case_local = 'REF'
        else:
            analysis_local = analysis
            case_local = case


        ##### Path where Q2Q transforms are located
        q2q_path = f'../q2q_repository/{analysis_local}/'

        ##### Path to save the figures
        output_path = f'../figs/q2q_transforms/{analysis}/'
        ### Comprueba que path to save existe, crear en caso contrario
        if not os.path.exists(output_path):
            os.makedirs(output_path)



        for idx, q2q in enumerate(['q2qv1', 'q2qv2', 'q2qv3']):

            version = q2q[-2:]
            file_q2q = f'q2q_{carrier}_{case_local}_{version}.pkl'

            try:
                with open(q2q_path + file_q2q, 'rb') as f:
                    q2q_transform = pickle.load(f)

                    x_values = np.linspace(0, 1, 1000)
                    y_values = q2q_transform(x_values)

                    ax = axes[idx]
                    ax.plot(x_values, y_values, alpha=0.5, label=case)
                    ax.plot([0, 1], [0, 1], linestyle='--', color='black', alpha=0.25)

                    ax.set_title(f'Q2Q - {version}')
                    ax.set_xlabel('input')
                    ax.set_ylabel('output')
                    ax.grid(True, linestyle='--', linewidth=0.5, color='black', alpha=0.25)

            except FileNotFoundError:
                print(f'Archivo no encontrado: {file_q2q}, se omite.')

    # Agregar leyendas si hay varios casos
    for ax in axes:
        ax.legend(loc='best', fontsize='small')

    # Guardar la figura por carrier
    file_output = f'q2q_{carrier}_{analysis}_ALL.jpg'
    fig.tight_layout()
    print(f'Saving (and perhaps overwriting) figure {file_output}')
    plt.savefig(output_path + file_output)
    plt.close()

