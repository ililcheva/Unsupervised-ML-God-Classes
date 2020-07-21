import sys
from sklearn.cluster import AgglomerativeClustering
import pandas as pd

k = int(sys.argv[2])
god_class = str(sys.argv[1])

god_class_csv = pd.read_csv('./feature_vectors/{0}.csv'.format(god_class), sep=',', header=0, index_col="Unnamed: 0")

god_class_csv_without_method_name = god_class_csv.drop(['method_name'], axis=1)

god_class_csv_arr = god_class_csv_without_method_name.values

hierarchical = AgglomerativeClustering(n_clusters=k).fit_predict(god_class_csv_arr)

method_names = god_class_csv['method_name'].values

hierarchical_dict = {
    'cluster_id': hierarchical,
    'method_name': method_names
}

hierarchical_results = pd.DataFrame(hierarchical_dict)
print(hierarchical_results.to_csv(sep=',', index=False))
