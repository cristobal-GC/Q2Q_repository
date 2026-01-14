
import matplotlib.pyplot as plt
import os



def fun_plot_hCF_durationCurves(df_hCF, carrier, case, analysis, colors):
    '''
    This function generates a figure with three plots, each comparing the duration curve of
    historical, q2qNo, and q2qvX, X=1,2,3.
    '''
    
    print('')
    print(f'Starting evaluation DURATION CURVES: {analysis} - {case} - {carrier}')
    print('---------------------------------------------------------------------')



    combinations = [
        ['historical', 'q2qNo', 'q2qv1'],
        ['historical', 'q2qNo', 'q2qv2'],
        ['historical', 'q2qNo', 'q2qv3']
    ]


    ##### Create figure
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)



    ii=0

    for ax, cols in zip(axes, combinations):


        for col in cols:
            sorted_values = df_hCF[col].sort_values(ascending=False).reset_index(drop=True)
            ax.plot(sorted_values, label=col, color=colors[col], linewidth=2)

        if ii==0:
            ax.set_ylabel("CF")

        ii +=1


        ax.legend()
        ax.set_ylim([0, 8760])
        ax.set_ylim([0, 1])
        ax.grid(True, linestyle='--', linewidth=0.5, color='black', alpha=0.25)



    plt.tight_layout()



    # Título general
    fig.suptitle(f'Duration curves {carrier}, {case}', fontsize=14)



    ##### Save plot
    output_path = f'../figs/evaluation/hCF_durationCurves/{analysis}/'
    ### Comprueba que existe, crear en caso contrario
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    
    output_name = f'hCF_{carrier}_{case}.jpg'

    plt.savefig(output_path + output_name)
    plt.close()





    
