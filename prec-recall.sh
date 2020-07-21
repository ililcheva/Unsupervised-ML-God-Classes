mkdir -p precs_recalls
for file in ground_truths/*.csv
do
    for algo in 'kmeans' 'hierarchical'
    do
        filename=`basename $file .csv`
        python3 prec-recall.py $filename $algo
    done
done