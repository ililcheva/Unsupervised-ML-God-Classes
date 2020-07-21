for file in silhouettes/**/*.csv
do
        filename=`basename $file .csv`
        python3 most-optimal-k.py $filename
done

awk '! a[$0]++' most-optimal-k-source.csv > most-optimal-k.csv
rm most-optimal-k-source.csv