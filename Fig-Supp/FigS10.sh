
cat ./FigS10/rs705698-deepocean-top-result/ref_list | while read s
do
ipython FigS10-ref.py ${s}
done


cat ./FigS10/rs705698-deepocean-top-result/alt_list | while read s
do
ipython FigS10-alt.py ${s}
done
