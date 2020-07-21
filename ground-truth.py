import sys
import pandas as pd

file = sys.argv[1]

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

god_class_df = pd.read_csv('./feature_vectors/{0}.csv'.format(file), sep=',',
                         header=0, index_col="Unnamed: 0")
methods = god_class_df['method_name'].values

methods_to_keywords = []


for method_name in methods:
    method_to_keyword = [method_name]
    for keyword in KEYWORDS:
        if method_name.lower().find(keyword) != -1:
            method_to_keyword.append(KEYWORDS.index(keyword))
            methods_to_keywords.append(method_to_keyword)
            break
    if len(method_to_keyword) != 2:
        method_to_keyword.append(len(KEYWORDS) - 1)
        methods_to_keywords.append(method_to_keyword)

ground_truth_df = pd.DataFrame(methods_to_keywords, columns=['Method name', 'Keyword'])
ground_truth_df.to_csv("./ground_truths/{0}.csv".format(file), sep=',', index=False)


