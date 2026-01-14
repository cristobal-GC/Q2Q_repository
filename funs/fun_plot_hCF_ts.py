
import matplotlib.pyplot as plt
import os



def fun_plot_hCF_ts(df_hCF, carrier, case, analysis, date_in, date_out):
    '''
    This function generates a figure with the time series of the hourly capacity factors.
    '''

    print('')
    print(f'Starting evaluation hCF time series: {analysis} - {case} - {carrier}')
    print('---------------------------------------------------------------------')




    
    year = df_hCF.index.year[0]
    date_in = f"{year}-{date_in}"
    date_out = f"{year}-{date_out}"


    ##### Create figure
    fig, ax = plt.subplots(1, 1, figsize=(12, 5), constrained_layout=True)


    # Filtrar el intervalo
    df_filtered = df_hCF.loc[date_in:date_out]

    # Graficar cada columna sobre el mismo ax
    for col in df_filtered.columns:
        ax.plot(df_filtered.index, df_filtered[col], label=col)


    # Título general
    fig.suptitle(f'Hourly CF {date_in}:{date_out}, {carrier}, {case}', fontsize=14)

    ax.set_ylabel("CF")
    ax.legend()
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, linestyle='--', linewidth=0.5, color='black', alpha=0.25)
    ax.tick_params(axis='x', rotation=20)


    ##### Save plot
    output_path = f'../figs/evaluation/hCF_ts/{analysis}/'
    ### Comprueba que existe, crear en caso contrario
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    
    output_name = f'hCF_{carrier}_{case}_{date_in}_{date_out}.jpg'

    plt.savefig(output_path + output_name)
    plt.close()





    
