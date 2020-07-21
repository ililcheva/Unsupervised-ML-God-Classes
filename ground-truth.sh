mkdir -p ground_truths
for file in feature_vectors/*.csv
do
    filename=`basename $file .csv`
    python3 ground-truth.py $filename
done