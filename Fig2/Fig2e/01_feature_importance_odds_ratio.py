import os
import sys
import h5py
import numpy as np
import pandas as pd
import time
import itertools
from scipy import interp
from itertools import cycle
import sklearn.cross_validation
from sklearn.externals import joblib
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
import brewer2mpl



clf = joblib.load('AdaBoost_800_estimators2.pkl')
feature_importance_score = pd.DataFrame(clf.feature_importances_)
feature_list = pd.read_table('689_feature_list.txt',sep=' ',header=None)
feature_importance_score = pd.DataFrame(clf.feature_importances_)
features = pd.concat([feature_list,feature_importance_score],axis=1)
features.columns = range(0,4)

#============Calculate the odds ration of each features ==========
grouped = features.ix[:,3].groupby(features.ix[:,2])
g_rank = np.array(grouped.rank()) # calculate the rank in each group
g_num = np.array(grouped.count()[features.ix[:,2]]) # count the number of each group
g_ratio = pd.DataFrame(g_rank / g_num)
f_ratio = features.ix[:,3].rank() / float(features.shape[0]) # the feature importance in all features

features = pd.concat([features,g_ratio,f_ratio],axis=1)
features.columns = ['index-num','feature-name','feature-type','importance','group-ratio','features-ratio']
features['odds'] = features['features-ratio'] / features['group-ratio']

features.to_csv('features_689.odds.csv',index=None)


