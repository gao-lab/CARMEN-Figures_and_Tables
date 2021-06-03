
cat ./FigS11/rs705698-deepocean-top-result/ref_list | while read s
do
ipython FigS11-ref.py ${s}
done


cat ./FigS11/rs705698-deepocean-top-result/alt_list | while read s
do
ipython FigS11-alt.py ${s}
done
