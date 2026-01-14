# Q2Q_repository

Estimating hourly generation time series for renewable technologies can be challenging. A common strategy, usually referred to as *physical approach*, consists on combining outputs from weather models, like wind speed or solar radiation, with a model of the  conversion processes taking place in a wind turbine or solar PV pannel. In this case, errors in the obtained generation time series may arise from hypotheses and simplifications throughout the entire conversion process (such as biases in the weather data, the spatio-temporal discretisation, simplified assumptions on the conversion model, etc.).

In [PyPSA-Spain](https://github.com/cristobal-GC/pypsa-spain), a methodology to reduce such errors was proposed and implemented, see the [seminal paper](https://doi.org/10.1016/j.esr.2025.101764) for details. The methodology, referred to as **quantile-to-quantile (Q2Q) transform**, relies on a statistical mapping between historical and modelled hourly capacity factors (hCF) for solar and wind power technologies. The main advantage and limitation of this approach is its statistical nature, as all the errors are handled all together regardless its nature (advantage), but no information regarding the source of error is obtained (limitation).

This repository provides comprehensive material to analyse the Q2Q performance under varying configuration parameters. As a by-product, it also contains a set of ready-to-use Q2Q transforms and scripts to reproduce the results. Note that this material is only valid for analyses focused on Spain. However, a similar methodology can be followed for other countries, provided that the necessary historical hCF time series are available.



## Content

The contents of this repository are as follows:

- **data/** contains historical and modelled hourly generation time series at country level for onshore wind and solar PV technologies for several years. Data with historical installed capacities to derive hCF time series are also included. Historical data were retrieved from [esios](https://api.esios.ree.es/). Modelled data were generated with PyPSA-Spain, under various configurations.

- **env/** contains a python environment to run the scripts contained in this repository.

- **figs/** contains a folder with figures of the Q2Q transforms included in the repository, and an evaluation folder with figures showing different performance assessments of the Q2Q transforms.

- **funs/** contais auxiliary functions required by the scripts.

- **notebooks/** includes some tutorials in the form of Jupyter notebooks.

- **pypsa-spain** contains the configuration files of the different runs of the model to compute all the modelled generation time series.

- **q2q_repository/** contains the set of Q2Q transformations obtained in the considered cases. They are ready-to-use in PyPSA-Spain (after considering the potential impacts of assumming different configuration parameters as those employed to obtain the selected Q2Q transforms).

- **scripts/** contains python scripts to reproduce the contents of the repository.



## Methodology

(tbd)



## Conclusions

The main conclusions of the analyses contained in this repository are as follows:

- For **onshore windpower**, the Q2Q transformation is **essential** for correcting the underestimation of the wind capacity factor (CF). The recommended normalisation scheme is **v2**.

- For **solar PV**, the Q2Q transformation only makes **minor improvements**, as the CF is already estimated fairly accurately by the model. The recommended normalisation scheme is **v1**.

Note that these recommendations differ from those in the [seminal paper](https://doi.org/10.1016/j.esr.2025.101764) due to methodological changes implemented in [PyPSA-Eur](https://github.com/PyPSA/pypsa-eur) between versions v0.0.0 and v2025.04.0 of PyPSA-Spain.



If you are interested in finding out more about the contents of this repository, or if you notice any errors or have any suggestions, please visit the [Issues section](https://github.com/cristobal-GC/Q2Q_repository/issues) or [make a PR](https://github.com/cristobal-GC/Q2Q_repository/pulls).