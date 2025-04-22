from scipy.stats import ecdf
from scipy.interpolate import interp1d
import numpy as np


def get_q2q_transform(df_input, df_target):


    ########## Prepare the data

    ### Get the time series in the form of an array
    ts_input = df_input.values.flatten()
    ts_target = df_target.values.flatten()



    ########## Prepare the CDFs

    ### Get an object with the input CDF
    ecdf_input = ecdf(ts_input)

    ### Get an object with the target CDF
    ecdf_target = ecdf(ts_target)

    ##### Get a function to evaluate the inverse input CDF
    ecdf_input_x = ecdf_input.cdf.quantiles
    ecdf_input_y = ecdf_input.cdf.probabilities
    ecdf_inverse_input = interp1d(ecdf_input_y, ecdf_input_x, kind='zero')

    ### Get a function to evaluate the inverse target CDF
    ecdf_target_x = ecdf_target.cdf.quantiles
    ecdf_target_y = ecdf_target.cdf.probabilities
    ecdf_inverse_target = interp1d(ecdf_target_y, ecdf_target_x, kind='zero')



    ########## Get the Q2Q function

    ### Get the probabilities where to evaluate the inverse CDFs
    prob_min = max([min(ecdf_input_y) , min(ecdf_target_y)]) # the highest between the two minima
    prob_max = min([max(ecdf_input_y) , max(ecdf_target_y)]) # the lowest between the two maxima
    probs = np.linspace(prob_min,prob_max,1000)

    ### Evaluate the inverse CDFs
    ecdf_input_x0 = ecdf_inverse_input(probs)
    ecdf_target_x0 = ecdf_inverse_target(probs)

    ### Include -eps at the beginning, 1+eps at the end for consistency of the Q2Q transform
    eps = 1e-4
    ecdf_input_x0 = np.concatenate([[-eps], ecdf_input_x0, [1+eps]])
    ecdf_target_x0 = np.concatenate([[-eps], ecdf_target_x0, [1+eps]])

    ### Get the transform by interpolation
    q2q_transform = interp1d(ecdf_input_x0, ecdf_target_x0, kind='linear')


    return q2q_transform