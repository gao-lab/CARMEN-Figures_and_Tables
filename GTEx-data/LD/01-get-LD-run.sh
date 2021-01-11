less CEU_rs_id.list | tr ';' '\t' | cut -f 1 | grep 'rs' > CEU_rs_id.list_use

ipython 01_LD_cal.py
