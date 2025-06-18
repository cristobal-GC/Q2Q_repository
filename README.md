# Q2Q_repository

Estimating hourly capacity factors for renewable technologies can be challenging, as errors arising from simplifications and limitations may occur at several stages of the process.

In [PyPSA-Spain](https://github.com/cristobal-GC/pypsa-spain), a proposal consisting on Q2Q transformations between historical and modelled time series were implemented, see the [seminal paper](https://doi.org/10.1016/j.esr.2025.101764) for details

This repository provides comprehensive material to help you understand the approach. It also contains a set of ready-to-use Q2Q transformations, as well as evaluation analyses to help you select the most appropriate one. Please note that this material is only valid for studies focused on Spain. However, a similar methodology can be followed for other countries, provided that the necessary historical data is available.


The contents of this repository are as follows:

- **data/** folder contains historical and modelled generation time series for onshore wind and solar PV technologies in peninsular Spain over several years. Data with historical installed capacities are also included. The modelled data were obtained using PyPSA-Spain under various configurations.

- **figs/** contains figures of all the Q2Q transforms included in the repository, as well as the results of performance analyses.

- **notebooks/** includes some illustrative Jupyter notebooks in the form of tutorials.

- **q2q_repository/** contains the set of precomputed Q2Q transformations.

- The rest of the folders contain support material.



The names of the files in this repository sometimes include labels that provide information about the configuration used to create the file.

- **europe/iberia** refers to the meteorological cutout:
    - *europe* is a cutout with a spatial resolution of 0.3 degrees. Wind speed data are from the ECMWF ERA5 reanalysis dataset, and solar radiation data are from the CMSAF SARAH-3 solar surface radiation dataset.
    - *iberia* is a cutout with a spatial resolution of 0.3 degrees. Both wind speed and solar radiation data are from ERA5.
    
- **NUTS 2/3** is the clustering level of the network.

- **v1, v2, v3** refer to the normalisation scheme employed to build the Q2Q transformation.



The main conclusions of the analyses contained in this repository are as follows:

- For **onshore windpower**, the Q2Q transformation is **essential** for correcting the underestimation of the wind capacity factor (CF). The recommended normalisation scheme is **v2**.

- For **solar PV**, the Q2Q transformation only makes **minor improvements**, as the CF is already estimated fairly accurately by the model. The recommended normalisation scheme is **v1**.

Note that these recommendations differ from those in the [seminal paper](https://doi.org/10.1016/j.esr.2025.101764) due to methodological changes implemented in [PyPSA-Eur](https://github.com/PyPSA/pypsa-eur) between versions v0.0.0 and v2025.04.0 of PyPSA-Spain.



If you are interested in finding out more about the contents of this repository, or if you notice any errors or have any suggestions, please visit the [Issues section](https://github.com/cristobal-GC/Q2Q_repository/issues) or [make a PR](https://github.com/cristobal-GC/Q2Q_repository/pulls).