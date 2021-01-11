#Date: 2018-03-29
#Contact: carmen@mail.cbi.pku.edu.cn

from numpy.random import seed
from sklearn.model_selection import ShuffleSplit
from sklearn.metrics import roc_auc_score
import h5py
import tensorflow as tf
import tensorflow.contrib.keras as keras
from tensorflow.contrib.keras import regularizers as regularizers
import numpy as np
import time
import os
import sys

feature=sys.argv[-1]

model_output_prefix = "./result/"+feature+"/"
data_path="./dataset/"+feature+".hdf5"
model_para_prefix="./result/"+feature+"/model_para/"

'''build model'''
def cnn_model(filter_num,filter_len,pool_len,lr,units):
    model = keras.models.Sequential()    
    model.add(keras.layers.Conv1D(
        filter_num,
        filter_len,
        strides=1,
        input_shape=(200,4),
        padding='same'))
    model.add(keras.layers.ThresholdedReLU(theta=1e-8))
    model.add(keras.layers.MaxPool1D(pool_size=pool_len,padding='valid'))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Conv1D(
        256,
        filter_len,
        strides=1,
        padding='same'))
    model.add(keras.layers.ThresholdedReLU(theta=1e-8))
    model.add(keras.layers.MaxPool1D(pool_size=pool_len,padding='valid'))
    model.add(keras.layers.Dropout(0.5))
    
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(units=units))
    model.add(keras.layers.ThresholdedReLU(theta=1e-8))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.Dense(units=1,activation='sigmoid'))
    sgd = keras.optimizers.SGD(lr=lr, momentum=0.9, decay=8e-7, nesterov=False)
    model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['acc'])
    return model

def cross_validation(data_num):
    total_num=np.arange(data_num)
    split_iterator=ShuffleSplit(n_splits=5, test_size=0.15,random_state=0)
    split_train_index_and_test_index_list = [(train_index, test_index) for train_index, test_index in split_iterator.split(total_num)]
    return(split_train_index_and_test_index_list)


def split_dataset(split_index_list, fold, data_x, data_y):
	x_train=data_x[split_index_list[fold][0].tolist()]
	y_train=data_y[split_index_list[fold][0].tolist()]
    
	x_test=data_x[split_index_list[fold][1].tolist()]
	y_test=data_y[split_index_list[fold][1].tolist()]
	return x_train, y_train, x_test, y_test

   
'''load data'''    
def load_v_t_data(dataset_path):
    data = h5py.File(dataset_path,"r")
    sequence_code = data['sequence_code'][:,:,:]
    label = data['label'][:,:]
    data_number=label.shape[0]
    return sequence_code, label, data_number

'''creat directory'''
def makir(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        return(True)
    else :
        return(False)

'''prediction'''
def prediction(model, test_data, test_label,path):
    predicted = model.predict(test_data, batch_size=200, verbose=2)
    out = h5py.File(path)
    out.create_dataset("predict",data=predicted)
    out.create_dataset("label",data=test_label)
    out.close()
    print("AUC=%s" % (roc_auc_score(test_label,predicted)))
        
'''training'''
def training(X_train,Y_train,X_test,Y_test,fold_num,sd,batch_size, number_of_epoch,filter_num,lr,units,filter_len,pool_len):
    #generate para-id
    id_key="split_"+str(fold_num)+"_"+str(sd)+"_"+str(filter_num)+"_"+str(filter_len)+"_"+str(pool_len)+"_"+str(units)+"_"+str(lr)+"_"+str(number_of_epoch)
    print("###############################################\t")
    print(id_key)
    #random numpy seed
    seed(sd)
    #create folder for prediction result and params
    output_path = model_output_prefix
    para_path = model_para_prefix
    makir(output_path)
    makir(para_path)
    predict_output_filename = output_path + "predict_"+id_key+".hdf5"
    model_para_filename = para_path + "para_"+id_key+".hdf5"
    #create model and train the model
    model=cnn_model(filter_num,filter_len,pool_len,lr,units)
    stopper=keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, verbose=0, mode='auto')    
    model.fit(X_train, Y_train, batch_size=batch_size, epochs=number_of_epoch, shuffle=True, verbose=2, validation_split=0.15, callbacks=[stopper])
    #evaluate the model
    score=model.evaluate(X_test, Y_test, batch_size = 200, verbose=2)
    print('Test loss:',score[0])
    print('Test accuracy:',score[1])
    #save the params
    model.save_weights(model_para_filename)
    #prediction
    test_prediction = prediction(model, X_test, Y_test, predict_output_filename)

    
def main():
    #load data
    w_sequence,w_label,w_data_num=load_v_t_data(data_path)
    data_split_list=cross_validation(w_data_num)
        
    for fdn in [0,1,2,3,4]:
        x_train, y_train, x_test, y_test=split_dataset(data_split_list, fdn, w_sequence, w_label)
        training(x_train, y_train, x_test, y_test,fold_num=fdn,sd=1,batch_size=200, number_of_epoch=50,filter_num=128,lr=0.01,units=512,filter_len=10,pool_len=4)
    print("Training finished.")
'''main function'''
t0 = time.time()
main()
print("Model training took %f hours" % ((time.time()-t0)/3600))
