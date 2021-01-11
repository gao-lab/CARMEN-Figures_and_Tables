#!/bin/bash
input_data_path="./model/CARMEN-E-input.hdf5"
weights_path="./model/CARMEN-E-h901_crossvalidation_seed_2_random_seed_6_split_4.hdf5"
input_dim_start=2424
data_set_name="CARMEN-E-feature-contribution"
hidden=901
ipython 01_deeplift_model_interpretation.py ${weights_path} ${input_data_path} ${input_dim_start} ${data_set_name} ${hidden}



input_data_path="./model/CARMEN-F-input.hdf5"

weights_path="./model/CARMEN-F-h1501_crossvalidation_seed_2_random_seed_5_split_1.hdf5"
input_dim_start=2424
data_set_name="CARMEN-F-feature-contribution"
hidden=1501
ipython 01_deeplift_model_interpretation.py ${weights_path} ${input_data_path} ${input_dim_start} ${data_set_name} ${hidden}
