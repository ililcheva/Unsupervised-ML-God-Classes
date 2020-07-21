import pandas as pd
import sys
from itertools import permutations

god_class = str(sys.argv[1])
algorithm = str(sys.argv[2])

''' GROUND TRUTH INTRA PAIRS '''
KEYWORDS = [
    'create',
    'object',
    'cache',
    'uri',
    'standalone',
    'encoding',
    'identifier',
    'user',
    'error',
    'content',
    'parameter',
    'subset',
    'global',
    'component',
    'none'
]

KEYWORDS = sorted(KEYWORDS, key=str.lower)

ground_truth_pairs = pd.read_csv('./ground_truths/{0}.csv'.format(god_class), sep=',',
                                 header=0)

ground_truth_clusters = []

for keyword_number in range(len(KEYWORDS)):
    ground_truth_clusters.append(list(
        ground_truth_pairs[ground_truth_pairs['Keyword'] == keyword_number]['Method name']))

ground_truth_clusters = [x for x in ground_truth_clusters if x != []]
ground_truth_intra_pairs = set()
for cluster in ground_truth_clusters:
    if len(cluster) > 1:
        ground_truth_intra_pairs.update(list(permutations(cluster, 2)))


''' RETRIEVING THE MOST OPTIMAL K FOR EACH ALGORITHM'''
most_optimal_k_df = pd.read_csv('most-optimal-k.csv', sep=',', header=0)

num_clusters_kmeans = int(most_optimal_k_df.loc[most_optimal_k_df['class_name'] == god_class, 'kmeans'])
num_clusters_hierarchical = int(most_optimal_k_df.loc[most_optimal_k_df['class_name'] == god_class, 'hierarchical'])


''' ALGORITHM INTRA PAIRS '''
k = num_clusters_kmeans if algorithm == 'kmeans' else num_clusters_hierarchical
algorithm_pairs = pd.read_csv(r'./{0}/{2}/{0}-{1}.csv'.format(algorithm,k,god_class), sep=',',
                            header=0, encoding='utf-8')

algorithm_clusters = []

for cluster_id in range(k):
    algorithm_clusters.append(
        list(algorithm_pairs[algorithm_pairs['cluster_id'] == cluster_id]['method_name']))

algorithm_clusters = [x for x in algorithm_clusters if x != []]
algorithm_intra_pairs = set()
for cluster in algorithm_clusters:
    if len(cluster) > 1:
        algorithm_intra_pairs.update(list(permutations(cluster, 2)))


''' CALCULATING THE PRECISION AND RECALL '''
precision= len(ground_truth_intra_pairs.intersection(
    algorithm_intra_pairs))/len(algorithm_intra_pairs)
recall= len(ground_truth_intra_pairs.intersection(
    algorithm_intra_pairs))/len(ground_truth_intra_pairs)



k_df = pd.DataFrame([[algorithm, precision, recall]], columns=['algorithm','precision', 'recall'])
with open('./precs_recalls/{0}.csv'.format(god_class), 'a') as f:
    k_df.to_csv(f, sep=',', index=False, header=f.tell()==0)

