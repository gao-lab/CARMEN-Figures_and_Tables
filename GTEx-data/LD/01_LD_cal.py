import pandas as pd
import requests, sys
import json
from pandas.io.json import json_normalize
import multiprocessing

def LD_score(rs_id):
    server = "https://rest.ensembl.org"
    ext = "/ld/human/"+str(rs_id)+"/1000GENOMES:phase_3:"+str(population)+"?r2=0.75;window_size=500"
    r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})

    if r.ok:
        decoded = r.json()
        if decoded:
            decoded_out = json_normalize(decoded)
            decoded_out.to_csv(str(population)+'-LD-pairs-point75', mode='a', header=False)

input_vcf = pd.read_table('CEU_rs_id.list_use',header=None)
vcf_id = input_vcf.ix[:,0]

population = "CEU"
pool = multiprocessing.Pool(20)
result = pool.map(LD_score,vcf_id.ix[0:])

