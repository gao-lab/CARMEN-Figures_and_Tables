# This is the script for compare motif using tomtom
import os
from subprocess import *
import multiprocessing

#motif dir
motif_dir="./motif"

#run motif compare script
def compare_motif(feature):
    check_call(["bash compare_motif.sh " +feature],shell=True)

def main():    
    file_list=os.listdir(motif_dir)
    pool = multiprocessing.Pool(processes = 32)
    for file in file_list:
        pool.apply_async(compare_motif,(file,))
    pool.close()
    pool.join()
    print("Finished")

main()