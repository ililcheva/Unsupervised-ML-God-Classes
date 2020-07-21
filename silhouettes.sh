mkdir -p silhouettes
for file in feature_vectors/*.csv
do
        for k in {2..80}
        do
                filename=`basename $file .csv`
                mkdir -p silhouettes/kmeans
                mkdir -p silhouettes/hierarchical
                python3 silhouette.py $filename $k '0'
        done
done