import sys
import pandas as pd


file = sys.argv[1]

''' Retrieving the k that maximizes the silhouette for each god class and algorithm '''
kmeans_silhouettes_dt = pd.read_csv('silhouettes/kmeans/{0}.csv'.format(file), sep=',', header=0)
kmeans_opt_k = int(kmeans_silhouettes_dt.loc[kmeans_silhouettes_dt['silhouette'].idxmax()]['k'])
hierarchical_silhouettes_dt = pd.read_csv('silhouettes/hierarchical/{0}.csv'.format(file), sep=',', header=0)
hierarchical_opt_k = int(hierarchical_silhouettes_dt.loc[hierarchical_silhouettes_dt['silhouette'].idxmax()]['k'])

''' Recording the findings in a temporary csv file that is being processed further by the shell script '''
''' Final values can be found in most-optimal-k.csv'''
k_df = pd.DataFrame([[file, kmeans_opt_k, hierarchical_opt_k]], columns=['class_name', 'kmeans', 'hierarchical'])
with open('most-optimal-k-source.csv', 'a') as f:
    k_df.to_csv(f, sep=',', index=False, header=f.tell()==0)

