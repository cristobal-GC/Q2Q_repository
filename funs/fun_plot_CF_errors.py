
import matplotlib.pyplot as plt
import os
import numpy as np


def fun_plot_CF_errors(df_CF_errors, carrier, analysis):
    '''
    This function generates a bar plot with CF for a specific analysis.
    '''


    print('')
    print(f'Starting evaluation CF errors (RMSE): {analysis} - {carrier}')
    print('---------------------------------------------------------------------')



    fontsize = 16


    ########## Fig. CF
    plt.rc('font', size=fontsize)          #    texto general
    plt.rc('axes', titlesize=fontsize)     #    título
    plt.rc('axes', labelsize=fontsize)     #    labels de ejes
    plt.rc('xtick', labelsize=fontsize)    #    ticks eje x
    plt.rc('ytick', labelsize=fontsize)    #    ticks eje y
    plt.rc('legend', fontsize=fontsize)



    fig, ax = plt.subplots(1, 1, figsize=(df_CF_errors.shape[0]*5, 6))



    ##### Bars
    df_CF_errors.plot(kind='bar', ax=ax)

    ax.set_ylabel('CF RMSE', fontsize=fontsize)
    ax.grid(True, linestyle='--', linewidth=0.5, color='black', alpha=0.25)
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.tick_params(axis='x', rotation=0)


    fig.tight_layout()



    ##### Save plot
    output_path = f'../figs/evaluation/CF_errors/{analysis}/'
    ### Comprueba que existe, crear en caso contrario
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    output_file = f'CF_errors_{carrier}_{analysis}.jpg'
    print(f'Saving (and perhaps overwriting) figure {output_file}')
    plt.savefig(output_path + output_file)

    plt.close()


