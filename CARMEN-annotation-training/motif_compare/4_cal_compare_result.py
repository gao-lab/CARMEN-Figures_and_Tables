#This is the script for calculate motif comparison results.
import os
import numpy as np

# dir of tomtom compare results with q value < 0.05
transfac_result_path="./result/transfac/"
jaspar_result_path="./result/jaspar/"

#output result
output_path="./result/all/"

#contruct feature_id <-> tf name
feature_name_file="./ref/feature_tf_list.txt"
feature_name=np.loadtxt(open(feature_name_file,'r'),delimiter="\t",dtype=np.str)
feature_name_dict={}
for x in range(feature_name.shape[0]):
    tf_name=feature_name[x][1].split("|")[1]
    if tf_name.split("-")[0]=="eGFP" or tf_name.split("-")[0]=="FLAG":
        tf_name=tf_name.split("-")[1].lower()
    else:
        tf_name=tf_name.lower()
    feature_name_dict[feature_name[x][0]]=tf_name
    feature_name_dict[feature_name[x][0]+"_Full"]=feature_name[x][1]
#motif_list for 803 models
motif_list=np.loadtxt(open("./ref/motif_match.txt",'r'),delimiter="\t",dtype=np.str,skiprows=1)

#merge results based on transfac and jaspar database 
def merge_result(feature):
    transfac_result=transfac_result_path+feature+"/tomtom_sig_motif.txt"
    jaspar_result=jaspar_result_path+feature+"/tomtom_sig_motif.txt"
    #merge
    transfac_tmp=np.loadtxt(open(transfac_result,'r'),delimiter="\t",dtype=np.str)
    jaspar_tmp=np.loadtxt(open(jaspar_result,'r'),delimiter="\t",dtype=np.str)
    merge_tmp=np.vstack((transfac_tmp,jaspar_tmp))
    merge_tmp=merge_tmp[merge_tmp[:,5].astype(np.float).argsort()]
    #remove repeat
    kernel_tf_list=[]
    for x in range(merge_tmp.shape[0]):
        kernel_tf_list.append((merge_tmp[x][0]+"|"+merge_tmp[x][10]).lower())
    new_kernel_tf_list=list(set(kernel_tf_list))
    non_repeat_list=[]
    for x in range(len(new_kernel_tf_list)):
        match_result=np.argwhere(np.array(kernel_tf_list)==new_kernel_tf_list[x])
        non_repeat_list.append(merge_tmp[match_result[0][0]])
    non_repeat_list=np.array(non_repeat_list)
    non_repeat_list=non_repeat_list[non_repeat_list[:,5].astype(np.float).argsort()]
    np.savetxt(output_path+feature+".txt",non_repeat_list,delimiter="\t",fmt="%s")
    return non_repeat_list

#cal the matched kernel number of each model
def compare_result(feature,motif_match_list):
    out=[]
    tf=feature_name_dict[feature]
    print tf   
    for x in range(motif_match_list.shape[0]):
        if motif_match_list[x][10].lower()==tf:
            out.append(motif_match_list[x])
    out=np.array(out)
    if out.shape[0]!=0:
        result_return=[feature,feature_name_dict[feature+"_Full"],out[0][4],out[0][5],out.shape[0]]
    else:
        result_return=[feature,feature_name_dict[feature+"_Full"],"NA","NA","0"]
    return result_return

#main function    
def main():
    output=[]
    for x in range(motif_list.shape[0]):
        feature=motif_list[x]
        non_repeat_list=merge_result(feature)
        output.append(compare_result(feature,non_repeat_list))
    output=np.array(output)
    np.savetxt("./result/motif_match_result.txt",output,delimiter="\t",fmt="%s")
    print("Finished.")

main()
