#!/bin/usr/python
#This script require keras verion 1.1.0
import os
import h5py
import numpy
import keras
import sys
import time
import itertools
import pandas as pd
import numpy as np
from keras.models import Model
from keras import regularizers
from keras.regularizers import l1, activity_l1
from keras import backend as K
import sklearn.cross_validation
import deeplift
from deeplift.conversion import keras_conversion as kc
import keras
	
	# Get the weights of model before and input file
weights_path = sys.argv[1]
weights = h5py.File(weights_path)
input_data_path = sys.argv[2]
data = h5py.File(input_data_path)
data_training = data['data_tensor'].value
label = data['label_tensor'].value
label = label.reshape(label.shape[0],1)
input_dim_start = int(sys.argv[3])
data_set_name = sys.argv[4]
hidden_unit = int(sys.argv[5])

#Split the model, split the neuralnetwork_model into 5 Dense
def neuralnetwork_model(model,input_dim,hidden):
        hidden_dim = hidden
        model.add(keras.layers.Dense(input_shape=(input_dim,),output_dim=hidden_dim, activation = "relu"))
        model.add(keras.layers.Dense(input_dim, activation = "linear"))
        model.add(keras.layers.core.Dense(output_dim=2000, W_regularizer=l1(0.0001), \
activity_regularizer=activity_l1(0.001)))
        model.add(keras.layers.core.Dense(output_dim=500, activation="relu"))
        model.add(keras.layers.core.Dense(output_dim=1, activation="sigmoid"))
        model.compile(loss="binary_crossentropy", optimizer="adadelta", metrics=["accuracy"])

        #model.load_weights(weight_path,by_name=True)
        return(model)

#input_data
model_start = keras.models.Sequential()
model_here = neuralnetwork_model(model_start,input_dim_start,hidden_unit)
lay = model_here.layers

#Send the weights to the weights direct
weights_direct = dict()
weights_direct[lay[0].name] = [weights[weights.keys()[3]][weights[weights.keys()[3]].keys()[0]].value,weights[weights.keys()[3]][weights[weights.keys()[3]].keys()[1]].value]
weights_direct[lay[1].name] = [weights[weights.keys()[3]][weights[weights.keys()[3]].keys()[2]].value,weights[weights.keys()[3]][weights[weights.keys()[3]].keys()[3]].value]
weights_direct[lay[2].name] = [weights[weights.keys()[0]][weights[weights.keys()[0]].keys()[0]].value,weights[weights.keys()[0]][weights[weights.keys()[0]].keys()[1]].value]
weights_direct[lay[3].name] = [weights[weights.keys()[1]][weights[weights.keys()[1]].keys()[0]].value,weights[weights.keys()[1]][weights[weights.keys()[1]].keys()[1]].value]
weights_direct[lay[4].name] = [weights[weights.keys()[2]][weights[weights.keys()[2]].keys()[0]].value,weights[weights.keys()[2]][weights[weights.keys()[2]].keys()[1]].value]


def my_save_weights_to_hdf5_group(f, layers):
    from keras import __version__ as keras_version

    f.attrs['layer_names'] = [layer.name.encode('utf8') for layer in layers]
    f.attrs['backend'] = K.backend().encode('utf8')
    f.attrs['keras_version'] = str(keras_version).encode('utf8')

    for layer in layers:
        g = f.create_group(layer.name)
        symbolic_weights = layer.weights
        #weight_values = K.batch_get_value(symbolic_weights)
        weight_values = weights_direct[layer.name]
        weight_names = []
        for i, (w, val) in enumerate(zip(symbolic_weights, weight_values)):
            if hasattr(w, 'name') and w.name:
                name = str(w.name)
            else:
                name = 'param_' + str(i)
            weight_names.append(name.encode('utf8'))
        g.attrs['weight_names'] = weight_names
        for name, val in zip(weight_names, weight_values):
            param_dset = g.create_dataset(name, val.shape,
                                          dtype=val.dtype)
            if not val.shape:
                # scalar
                param_dset[()] = val
            else:
                param_dset[:] = val

def my_save_weights(laye, filepath, overwrite=True):
        """Dumps all layer weights to a HDF5 file.
        The weight file has:
            - `layer_names` (attribute), a list of strings
                (ordered names of model layers).
            - For every layer, a `group` named `layer.name`
                - For every such layer group, a group attribute `weight_names`,
                    a list of strings
                    (ordered names of weights tensor of the layer).
                - For every weight in the layer, a dataset
                    storing the weight value, named after the weight tensor.
        # Arguments
            filepath: String, path to the file to save the weights to.
            overwrite: Whether to silently overwrite any existing file at the
                target location, or provide the user with a manual prompt.
        # Raises
            ImportError: If h5py is not available.
        """
        if h5py is None:
            raise ImportError('`save_weights` requires h5py.')
        # If file exists and should not be overwritten:
        if not overwrite and os.path.isfile(filepath):
            proceed = ask_to_proceed_with_overwrite(filepath)
            if not proceed:
                return
        f = h5py.File(filepath, 'w')
        my_save_weights_to_hdf5_group(f,laye)
        f.flush()
        f.close()

my_save_weights(lay,"model_here_weights.h5")

# Use the deeplift the calculate the contribution.
model_here.load_weights("model_here_weights.h5")
deeplift_model = kc.convert_sequential_model(
                    model_here,
                    nonlinear_mxts_mode=deeplift.blobs.NonlinearMxtsMode.RevealCancel)

find_scores_layer_idx = 0
deeplift_contribs_func = deeplift_model.get_target_contribs_func(
                            find_scores_layer_idx=find_scores_layer_idx,
                            target_layer_idx=-2)

scores = np.array(deeplift_contribs_func(task_idx=0,
                                         input_data_list=[data_training],
                                         batch_size=10,
                                         progress_update=100))

scores_new = np.concatenate((scores,label),axis=1)	
np.savetxt(data_set_name+"_contribution_score.txt",scores_new)
