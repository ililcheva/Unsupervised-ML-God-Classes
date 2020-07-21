mkdir -p kmeans
mkdir -p hierarchical
for file in feature_vectors/*.csv
do
        for k in {2..80}
        do
                filename=`basename $file .csv`
                mkdir -p kmeans/$filename
                mkdir -p hierarchical/$filename
                python3 k-means.py $filename $k > "kmeans/$filename/kmeans-$k.csv"
                python3 hierarchical.py $filename $k > "hierarchical/$filename/hierarchical-$k.csv"
        done
done

