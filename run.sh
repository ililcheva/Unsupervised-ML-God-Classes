#!/bin/bash
echo 'Extracting the feature vectors...'
sh ./extract-feature-vectors.sh
echo 'Finished!'
echo 'Clustering god classes with kmeans and hierarchical algorithms...'
sh ./clustering.sh
echo 'Finished!'
echo 'Computing silhouette metric for k = {2 .. 80} for both algorithms...'
sh ./silhouettes.sh
echo 'Finished!'
echo 'Computing the best k for both algorithms individually...'
sh ./most-optimal-k.sh
echo 'Finished!'
echo 'Defining the ground truth...'
sh ./ground-truth.sh
echo 'Finished!'
echo 'Computing the precision and recall...'
sh ./prec-recall.sh
echo 'Finished'