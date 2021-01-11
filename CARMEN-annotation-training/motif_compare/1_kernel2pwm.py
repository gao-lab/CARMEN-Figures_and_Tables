#This is the script for converting kernels to PWMs
import os
import h5py
import numpy as np
import tensorflow as tf
import tensorflow.contrib.keras as keras
from tensorflow.contrib.keras import backend as K
from functools import reduce
import pandas as pd
from subprocess import *

#construct model file dict
para_dir="./para_tf_200/"
data_dir="./pos_data/"
model_file_dict={}
model_file_list=os.listdir(para_dir)
for model_file in model_file_list:
    model_file_dict[model_file.split("_")[0]]=model_file
print("construst model file dictionary successfully.")

'''load data'''    
def load_data(dataset_path):
    data = h5py.File(dataset_path)
    sequence_code = data['sequence_code'][:,:,:]
    print("Finish load data.")
    return sequence_code

    
'''model'''
def cnn_model(filter_num,filter_len,pool_len,units):
    model = keras.models.Sequential()
    model.add(keras.layers.Conv1D(
        filter_num,
        filter_len,
        strides=1,
        input_shape=(200,4),
        padding='same'))
    model.add(keras.layers.ThresholdedReLU(theta=1e-8))
    model.add(keras.layers.MaxPool1D(pool_size=pool_len,padding='valid'))
    model.add(keras.layers.Dropout(0.5))
    
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(units=units))
    model.add(keras.layers.ThresholdedReLU(theta=1e-8))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(units=1,activation='sigmoid'))
    return model

'''compute pwm'''
def compute_pwm(sequence_list):
    seq_length = sequence_list.shape[1]
    pwm = np.zeros((seq_length,4)) # fixed order  A C G T
    for i in range(seq_length):
        seq_list = sequence_list[:,i,:]
        base_count=reduce(np.add, sequence_list[:,i,:])
        pwm[i]=base_count/float(np.sum(base_count))
    return(pwm)

'''extract pwm for each kernel'''
def extract_pwm(model, x_train, OUT, kernel_size):
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    function = K.function([model.layers[0].input], [model.layers[0].output])
    conv_result = function([x_train])[0]
    out_kernel_file_path=OUT+"/kernels.txt"
    fw=open(out_kernel_file_path,'a')
    for i in range(conv_result.shape[2]): # for each kernel
        result=conv_result[:,:,i]
        max_score=np.max(result)
        if max_score<=0:
            continue
        position=np.where(result>(max_score/2))
        sequences=[]
        for j in range(position[0].shape[0]): # extract one-hot sequence
            seq_id=position[0][j]
            seq_pos=position[1][j]
            if seq_pos>200-kernel_size:
                continue
            sequences.append(x_train[seq_id,seq_pos:seq_pos+kernel_size,:])
        sequences=np.array(sequences)
        sequence_num=sequences.shape[0]
        if sequence_num==0:
            continue
        pwm=compute_pwm(sequences)
        pwm=pwm.astype(np.str)
        #write pwm to file
        for x in range(pwm.shape[0]):
            fw.write("\t".join(list(pwm[x])))
            fw.write("\n")
        fw.write("\n")
    fw.close()
    #comvert to meme format
    check_call(["less "+out_kernel_file_path+"| matrix2meme > "+out_kernel_file_path.replace(".txt",".meme")],shell=True)


def main(feature_id):
    #make out dictionary
    out_dir="./motif/"+feature_id
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
        #get para file
        model_para_file=model_file_dict[feature_id]
        #construct model
        model_para_path=para_dir+model_para_file
        fn=int(model_para_file.split("_")[4])
        fl=int(model_para_file.split("_")[5])
        pl=int(model_para_file.split("_")[6])
        un=int(model_para_file.split("_")[7])
        model=cnn_model(filter_num=fn,filter_len=fl,pool_len=pl,units=un)
        #load para file and data
        model.load_weights(model_para_path)
        x_train=load_data(data_dir+feature_id+".hdf5")
        #extract pwm
        extract_pwm(model, x_train, out_dir, kernel_size=fl)
        print("Finish %s" % feature_id)
    else:
        print("Already exists. Start next one.")


file_list=os.listdir(data_dir)
for file in file_list:
    main(file.split(".")[0])
print("Finished.")
