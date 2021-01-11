#!/usr/bin/python  
#-*- coding:utf-8 -*-  
############################  
#File Name: process-result.py
#Created Time: 2018-03-15 
############################  

import sys
import h5py
import numpy as np
import pandas as pd
from scipy import interp
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import sklearn
from sklearn import metrics
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import confusion_matrix


def confusion_matriloc_calculate(label,predict_label):

    def Find_Optimal_Cutoff( target, predicted):
        fpr, tpr, threshold = roc_curve(target, predicted)
        i = np.arange(len(tpr))
        roc = pd.DataFrame({'tf' : pd.Series(tpr-(1-fpr), index=i), 'threshold' : pd.Series(threshold, index=i)})
        roc_t = roc.ix[(roc.tf-0).abs().argsort()[:1]]
        return list(roc_t['threshold'])

    def confusion_matrix_ca( label, predict):
        threshold = Find_Optimal_Cutoff(target=label, predicted=predict) # Use get the best cutoff of the AUC curve
        fpr, tpr, thresholds = roc_curve(label, predict)
        auc_value = auc(fpr, tpr) # Calculate AUC
        precision, recall, thresholds_pr = precision_recall_curve(label, predict)
        prauc_value = auc(recall,precision)
        predict_label = (predict >= threshold[0]) + 0
        tn, fp, fn, tp = confusion_matrix(label,predict_label).ravel()
        sensitivity = float(tp)/(tp+fn)
        specificity = float(tn)/(fp+tn)
        precision = float(tp)/(tp+fp)
        FDR = float(fp)/(tp+fp)
        accuracy = float((tp+tn))/(tp+tn+fp+fn)
        matrix = [threshold[0],auc_value,prauc_value]
        return(matrix)
    matrix_result = confusion_matrix_ca(label,predict)
    return(matrix_result)


data_file = pd.read_csv('./FigS5/ExPecto.snplabel.csv')
label = data_file.iloc[:,6]
predict = data_file.iloc[:,11]
result = confusion_matriloc_calculate(label,predict)
result.append("ExPecto")
print result

data_file = pd.read_csv('./FigS5/CARMEN_filter_NULL.txt')
label = data_file.iloc[:,6]
predict = data_file.iloc[:,7]*data_file.iloc[:,8]/(data_file.iloc[:,7]*data_file.iloc[:,8]+(1-data_file.iloc[:,7])*(1-data_file.iloc[:,8]))
result = confusion_matriloc_calculate(label,predict)
result.append("CARMEN")
print result


data_file = pd.read_csv('./FigS5/EnsembleExpr_filter_NULL.txt',header=None,sep='\t')
label = data_file.iloc[:,5]
predict = data_file.iloc[:,6]
result = confusion_matriloc_calculate(label,predict)
result.append("EnembleExpr")
print result

data_file = pd.read_csv('./FigS5/CADD_filter_NULL.txt',header=None,sep='\t')
label = data_file.iloc[:,5]
predict = data_file.iloc[:,7]
result = confusion_matriloc_calculate(label,predict)
result.append("CADD")
print result

data_file = pd.read_csv('./FigS5/Deepsea_filter_NULL.txt',header=None,sep='\t')
label = data_file.iloc[:,5]
predict = 1-data_file.iloc[:,7]
result = confusion_matriloc_calculate(label,predict)
result.append("DeepSEA")
print result


data_file = pd.read_csv('./FigS5/Funseq2_filter_NULL.txt',header=None,sep='\t')
label = data_file.iloc[:,5]
predict = data_file.iloc[:,7]
result = confusion_matriloc_calculate(label,predict)
result.append("FunSeq2")
print result

data_file = pd.read_csv('./FigS5/Eigen_filter_NULL.txt',header=None,sep='\t')
label = data_file.iloc[:,5]
predict = data_file.iloc[:,7]
result = confusion_matriloc_calculate(label,predict)
result.append("Eigen")
predict = data_file.iloc[:,8]
result1 = confusion_matriloc_calculate(label,predict)
result1.append("Eigen-PC")

print result
print result1


data_file = pd.read_csv('./FigS5/GWAVA_filter_NULL.txt',header=None,sep='\t')
label = data_file.iloc[:,5]
predict = data_file.iloc[:,7]
result1 = confusion_matriloc_calculate(label,predict)
result1.append("GWAVA-Region")
predict = data_file.iloc[:,8]
result2 = confusion_matriloc_calculate(label,predict)
result2.append("GWAVA-TSS")
predict = data_file.iloc[:,9]
result3 = confusion_matriloc_calculate(label,predict)
result3.append("GWAVA-Unmatch")

print result1
print result2
print result3


data_file = pd.read_csv('./FigS5/BiT_LCL_DNase_result_final_merge.txt',header=None,sep='\t')
label = data_file.iloc[:,0]
predict = data_file.iloc[:,2].abs()
result = confusion_matriloc_calculate(label,predict)
result.append("DeepFIGV-DNase")
print result

data_file = pd.read_csv('./FigS5/BiT_LCL_H3K27AC_result_final_merge.txt',header=None,sep='\t')
label = data_file.iloc[:,0]
predict = data_file.iloc[:,2].abs()
result = confusion_matriloc_calculate(label,predict)
result.append("DeepFIGV-H3K27AC")
print result

data_file = pd.read_csv('./FigS5/BiT_LCL_H3K4ME1_result_final_merge.txt',header=None,sep='\t')
label = data_file.iloc[:,0]
predict = data_file.iloc[:,2].abs()
result = confusion_matriloc_calculate(label,predict)
result.append("DeepFIGV-H3K4ME1")
print result

data_file = pd.read_csv('./FigS5/BiT_LCL_H3K4ME3_result_final_merge.txt',header=None,sep='\t')
label = data_file.iloc[:,0]
predict = data_file.iloc[:,2].abs()
result = confusion_matriloc_calculate(label,predict)
result.append("DeepFIGV-H3K4ME3")
print result

data_file = pd.read_csv('./FigS5/BiT_ncER_result_final_merge.txt',header=None,sep='\t')
label = data_file.iloc[:,1]
predict = data_file.iloc[:,3]
result = confusion_matriloc_calculate(label,predict)
result.append("ncER")
print result



