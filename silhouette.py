import sys
from sklearn.metrics import silhouette_score
import pandas as pd

wants_value = int(sys.argv[3])
k = int(sys.argv[2])
god_class = str(sys.argv[1])

feature_vector_dt = pd.read_csv("./feature_vectors/{0}.csv".format(god_class), sep=',', header=0, index_col="Unnamed: 0")
kmeans_dt = pd.read_csv('./kmeans/{0}/kmeans-{1}.csv'.format(god_class, k), sep=',', header=0)
hierarchical_dt = pd.read_csv('./hierarchical/{0}/hierarchical-{1}.csv'.format(god_class, k), sep=',', header=0)

feature_vector_dt_without_method_name = feature_vector_dt.drop(['method_name'], axis=1)

feature_vector_dt_arr = feature_vector_dt_without_method_name.values



''' Kmeans silhouettes for various k '''
kmeans_clusters = kmeans_dt['cluster_id'].values
kmeans_silhouette = silhouette_score(feature_vector_dt_arr, kmeans_clusters)

''' Hierarchical silhouettes for various k '''
hierarchical_clusters = hierarchical_dt['cluster_id'].values
hierarchical_silhouette = silhouette_score(feature_vector_dt_arr, hierarchical_clusters)
   
if wants_value == 0:
    kmeans_df = pd.DataFrame([[k, kmeans_silhouette]], columns=['k', 'silhouette'])
    with open('silhouettes/kmeans/{0}.csv'.format(god_class), 'a') as f:
        kmeans_df.to_csv(f, sep=',', index=False, header=f.tell()==0)
    
    hierarchical_df = pd.DataFrame([[k, hierarchical_silhouette]], columns=['k', 'silhouette'])
    with open('silhouettes/hierarchical/{0}.csv'.format(god_class), 'a') as f:
        hierarchical_df.to_csv(f, sep=',', index=False, header=f.tell()==0)

else:
    print('Silhouette for {0} class and {1} clusters is {2} with kMeans.'.format(god_class, k, silhouette_score(feature_vector_dt_arr, kmeans_clusters)))
    print('Silhouette for {0} class and {1} clusters is {2} with Hierarchical.'.format(god_class, k, silhouette_score(feature_vector_dt_arr, hierarchical_clusters)))
