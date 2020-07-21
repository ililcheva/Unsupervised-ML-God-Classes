import sys
from sklearn.cluster import KMeans
import pandas as pd

k = int(sys.argv[2])
god_class = str(sys.argv[1])

god_class_csv = pd.read_csv("./feature_vectors/{0}.csv".format(god_class), sep=',', header=0, index_col="Unnamed: 0")
# print(XSDHandler.head(2))

god_class_csv_without_method_name = god_class_csv.drop(['method_name'], axis=1)
# print(XSDHandler_without_method_name.head(10))
god_class_csv_arr = god_class_csv_without_method_name.values
# print(XSDHandler.isin(["method_name"]))
# print(XSDHandlerArr)

kmeans = KMeans(n_clusters=k).fit_predict(god_class_csv_arr)
# print(kmeans)

method_names = god_class_csv['method_name'].values
# print(method_names)

kmeans_dict = {
    'cluster_id': kmeans,
    'method_name': method_names
}

kmeans_results = pd.DataFrame(kmeans_dict)
print(kmeans_results.to_csv(sep=',',index=False))

# kmeans_results.to_csv("kmeans/kmeans-{}.csv".format(k), index=False)