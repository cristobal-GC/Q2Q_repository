import numpy as np


def fun_get_df_hCF_errors(df_hCF):
    ''' 
    This function computes the error of the hourly capacity factors.    
    '''
    
    ### En realidad yo querría usar esto, que resta la primera columna menos la columna en cuestión
    # col1 = df_hCF.iloc[:, 0]
    # df_hCF_errors = col1.sub(df_hCF.iloc[:, 1:], axis=0)
    
    
    ##### Pero uso esto de momento, la columna en cuestión menos la primera, porque esto no comprueba duplicidades, que tengo que ver por qué las hay en los datos históricos
    # Lo multiplico por -1 para invertir el resultado, y que sea lo que quiero, histórico menos estimado
    col1 = df_hCF.iloc[:, 0]
    df_hCF_errors = -df_hCF.iloc[:, 1:].subtract(col1, axis=0)


    return df_hCF_errors
