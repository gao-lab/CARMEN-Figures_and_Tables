#!/usr/bin/python  
#-*- coding:utf-8 -*-  
############################  
#File Name: process-result.py
#Author: ShiFY
#Mail: shify@mail.cbi.pku.edu.cn  
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

def confusion_matriloc_calculate(label,predict_label):

	tp = (((label + predict_label) == 2) + 0).sum()
	tn = (((label + predict_label) == 0) + 0).sum()
	fp = (((label - predict_label) == -1) + 0).sum()
	fn = (((label - predict_label) == 1) + 0).sum()

	sensitivity = float(tp)/(tp+fn)
	specificity = float(tn)/(fp+tn)

	precision = float(tp)/(tp+fp)
	FDR = float(fp)/(tp+fp)

	accuracy = float((tp+tn))/(tp+tn+fp+fn)
	weighted_acc = float((5*tp+tn))/(5*tp+tn+fp+5*fn)
	F1score = 2*sensitivity*precision/(sensitivity+precision) 
	matriloc = [sensitivity,weighted_acc,F1score]
	return(matriloc)


data_file = pd.read_csv('ExPecto_filter_NULL.txt')
label = (data_file.iloc[:,6] != "Inactive")+0
predict = (data_file.iloc[:,10]  != 0 )+0
result = confusion_matriloc_calculate(label,predict)
result.append("ExPecto")
print result

data_file = pd.read_csv('CARMEN_filter_NULL.txt')
label = data_file.iloc[:,6]
predict = ((data_file.iloc[:,7]*data_file.iloc[:,8]/(data_file.iloc[:,7]*data_file.iloc[:,8]+(1-data_file.iloc[:,7])*(1-data_file.iloc[:,8]))) > 0.005 )+0
result = confusion_matriloc_calculate(label,predict)
result.append("CARMEN")
print result

data_file = pd.read_csv('CARMEN_filter_NULL.txt')
label = data_file.iloc[:,6]
predict = (data_file.iloc[:,7] > 0.5 )+0
result = confusion_matriloc_calculate(label,predict)
result.append("CARMEN-E")
print result

data_file = pd.read_csv('CARMEN_filter_NULL.txt')
label = data_file.iloc[:,6]
predict = (data_file.iloc[:,8] > 0.005 )+0
result = confusion_matriloc_calculate(label,predict)
result.append("CARMEN-F")
print result


data_file = pd.read_csv('EnsembleExpr_filter_NULL.txt')
label = data_file.iloc[:,1]
predict = ( data_file.iloc[:,2] > 0.049860000000000002)+0
result = confusion_matriloc_calculate(label,predict)
result.append("EnembleExpr")
print result

data_file = pd.read_csv('CADD_filter_NULL.txt',header=None,sep='\t')
label = (data_file.iloc[:,0] != "Inactive")+0
predict = (data_file.iloc[:,1] >= 10)+0
result = confusion_matriloc_calculate(label,predict)
result.append("CADD")
print result

data_file = pd.read_csv('deepsea_filter_NULL.txt',header=None,sep='\t')
label = (data_file.iloc[:,0] != "Inactive")+0
predict = (data_file.iloc[:,1] < 0.01)+0
result = confusion_matriloc_calculate(label,predict)
result.append("DeepSEA")
print result


data_file = pd.read_csv('funseq2_filter_NULL.txt',header=None,sep='\t')
label = (data_file.iloc[:,0] != "Inactive")+0
predict = (data_file.iloc[:,2] > 2)+0
result = confusion_matriloc_calculate(label,predict)
result.append("FunSeq2")
print result

data_file = pd.read_csv('Eigen_filter_NULL.txt',header=None,sep='\t')
label = (data_file.iloc[:,0] != "Inactive")+0
predict = (data_file.iloc[:,1] > 5)+0
result = confusion_matriloc_calculate(label,predict)
result.append("Eigen")
predict = (data_file.iloc[:,2] > 9)+0
result1 = confusion_matriloc_calculate(label,predict)
result1.append("Eigen-PC")

print result
print result1


data_file = pd.read_csv('GWAVA_filter_NULL.txt',header=None,sep='\t')
label = (data_file.iloc[:,0] != "Inactive")+0
predict = (data_file.iloc[:,1] > 0.5)+0
result1 = confusion_matriloc_calculate(label,predict)
result1.append("GWAVA-Region")
predict = (data_file.iloc[:,2] > 0.5)+0
result2 = confusion_matriloc_calculate(label,predict)
result2.append("GWAVA-TSS")
predict = (data_file.iloc[:,3] > 0.5)+0
result3 = confusion_matriloc_calculate(label,predict)
result3.append("GWAVA-Unmatch")

print result1
print result2
print result3


data_file = pd.read_csv('DeepFIGV_LCL_DNase.txt',header=None,sep='\t')
label = (data_file.iloc[:,0] != "Inactive")+0
predict = (data_file.iloc[:,2].abs() >= 0.3325)+0
result = confusion_matriloc_calculate(label,predict)
result.append("DeepFIGV-DNase")
print result

data_file = pd.read_csv('DeepFIGV_LCL_H3K27AC.txt',header=None,sep='\t')
label = (data_file.iloc[:,0] != "Inactive")+0
predict = (data_file.iloc[:,2].abs() >= 0.22989999999999999)+0
result = confusion_matriloc_calculate(label,predict)
result.append("DeepFIGV-H3K27AC")
print result

data_file = pd.read_csv('DeepFIGV_LCL_H3K4ME1.txt',header=None,sep='\t')
label = (data_file.iloc[:,0] != "Inactive")+0
predict = (data_file.iloc[:,2].abs() >= 0.46949999999999997)+0
result = confusion_matriloc_calculate(label,predict)
result.append("DeepFIGV-H3K4ME1")
print result

data_file = pd.read_csv('DeepFIGV_LCL_H3K4ME3.txt',header=None,sep='\t')
label = (data_file.iloc[:,0] != "Inactive")+0
predict = (data_file.iloc[:,2].abs() >= 0.52070000000000005)+0
result = confusion_matriloc_calculate(label,predict)
result.append("DeepFIGV-H3K4ME3")
print result

data_file = pd.read_csv('ncER_result.txt',header=None,sep='\t')
label = (data_file.iloc[:,0] != "Inactive")+0
predict = (data_file.iloc[:,2] >= 56.473199999999999)+0
result = confusion_matriloc_calculate(label,predict)
result.append("ncER")
print result



