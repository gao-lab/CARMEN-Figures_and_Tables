#This is the script for dealing with tomtom results
import numpy as np
import os

#construct motif_id <-> tf name
motif_name_id_file="./ref/motif_id_name_list_TRANSFAC.txt"
motif_name_id=np.loadtxt(open(motif_name_id_file,'r'),delimiter="\t",dtype=np.str)
motif_id_dict={}
motif_list=[]
for x in range(motif_name_id.shape[0]):
    motif_id_dict[motif_name_id[x][0]]=motif_name_id[x][1]
    motif_list.append(motif_name_id[x][1].lower())
print("Construct dict for motif id and name successfully.")

#filter results with q value < 0.05
def deal_tomtom_result(feature):
    result_file_path="./result/transfac/"+feature+"/tomtom.tsv"
    temp=np.loadtxt(open(result_file_path,'r'),delimiter="\t",dtype=np.str,skiprows=1)
    match_motif_list=[]
    tf_name_list=[]
    for x in range(temp.shape[0]):
        if float(temp[x][5])<0.05:
            tf_name=motif_id_dict[temp[x][1]]
            tf_name_list.append(tf_name)
            match_motif_list.append(temp[x])
    match_motif_list=np.array(match_motif_list)
    tf_name_list=np.array(tf_name_list)
    tf_name_list=tf_name_list.reshape((tf_name_list.shape[0],1))
    match_motif_list=np.hstack((match_motif_list,tf_name_list))
    match_motif_list=match_motif_list[match_motif_list[:,5].astype(np.float).argsort()] #sort by q value
    np.savetxt(result_file_path.replace("tomtom.tsv","tomtom_sig_motif.txt"),match_motif_list,delimiter="\t",fmt="%s")
    print("Finish %s" % feature)

def main():
    for file in os.listdir("./result/transfac/"):
        deal_tomtom_result(file)
    print("Finished ALL.")

main()