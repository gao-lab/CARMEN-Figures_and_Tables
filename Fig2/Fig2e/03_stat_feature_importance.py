import pandas as pd

feature_689 = pd.read_csv("features_689.odds.csv")
feature_689_use = feature_689[['feature-type','importance']]
feature_689_use_group = feature_689_use.groupby('feature-type').sum()

feature_1190 = pd.read_csv("features_1190.odds.csv")
feature_1190_use = feature_1190[['feature-type','importance']]
feature_1190_use_group = feature_1190_use.groupby('feature-type').sum()

feature_importance = pd.concat([feature_689_use_group,feature_1190_use_group],axis=1)

feature_importance = feature_importance.rename(index={"TF":"Transcription Factor Binding","Histone":"Histone Markers","Metylation":"Methylation Profiles","Conservation":"Evolutionary Features","DNase":"DNase Accessibility","PC":"Pysicochemical Properties"})
feature_importance.columns=['CARMEN-E','CARMEN-F']
feature_importance.index.names = ['name_list']

feature_importance.to_csv("04_plot_use_file.txt")


