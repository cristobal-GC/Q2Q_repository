
import matplotlib.pyplot as plt
import os

from .fun_get_df_hCF_errors import fun_get_df_hCF_errors


def fun_plot_hCF_errors(df_hCF, carrier, case, analysis):
    '''
    This function generates a figure with three plots, one per q2q version. Each plot is a heatmap representation of the hourly capacity factors.
    '''


    print('')
    print(f'Starting evaluation hCF error heatmaps: {analysis} - {case} - {carrier}')
    print('---------------------------------------------------------------------')



    ##### Get df_hCF_errors
    df_hCF_errors = fun_get_df_hCF_errors(df_hCF)

    ### Máx. value in abs. to adjust common limits in plots
    abs_max = df_hCF_errors.abs().max().max()



    ##### Create figure
    fig, axes = plt.subplots(1, df_hCF_errors.shape[1], figsize=(12, 8), sharey=True, constrained_layout=True)


    ##### Loop in columns
    for ax, col in zip(axes, df_hCF_errors.columns):

        data = df_hCF_errors[col].to_numpy().reshape(365, 24)

        im = ax.imshow(data, aspect='auto', cmap='PiYG', vmin=-abs_max, vmax=abs_max)

        ax.set_xlabel('Hour of the Day')
        ax.set_title(f'{col}')

        if ax == axes[0]:
            ax.set_ylabel('Day of the Year')

    # Colorbar común
    cbar = fig.colorbar(im, ax=axes.ravel().tolist(), label='Hourly CF error (real - model)')


    # Título general
    fig.suptitle(f'{carrier}, {case}', fontsize=14)


    ##### Save plot
    output_path = f'../figs/evaluation/hCF_errors/{analysis}/'
    ### Comprueba que existe, crear en caso contrario
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    
    output_name = f'HCF_error_{carrier}_{case}.jpg'

    plt.savefig(output_path + output_name)
    plt.close()





    
