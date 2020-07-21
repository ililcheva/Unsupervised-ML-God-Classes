import os
import javalang
import numpy as np
import pandas as pd

def get_java_files():
    java_files = []
    for root, dirs, files in os.walk("./xerces2-j-trunk/src/"):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.abspath(os.path.join(root, file)))
    return java_files

""" Getting class method count """
def parse_files(files):
    class_names = []
    class_method_counts = []
    for file in files:
        path, class_name = os.path.split(file)
        opened = open(file, 'r').read()
        tree = javalang.parse.parse(opened)
        for path, node in tree.filter(javalang.tree.ClassDeclaration):
            class_names.append(class_name[:-5])
            class_method_counts.append(len(node.methods))
    return class_names, class_method_counts



""" Computing condition variables for a god class """
def compute_mean_and_std(number_of_methods):
    return np.mean(number_of_methods, axis=0), np.std(number_of_methods, axis=0)


files = get_java_files()
class_names, number_of_methods = parse_files(files)
mean, standart_deviation = compute_mean_and_std(number_of_methods)


""" Creating a DataFrame for all classes """
classes_dict = {
    'Class name': class_names,
    'Number of methods': number_of_methods
}

classes_df = pd.DataFrame(classes_dict)

""" Retrieving a dictionary of god classes """
god_classes_dict = {
    'Class name': [],
    'Number of methods': []
}

for ind in classes_df.index:
    if classes_df['Number of methods'][ind] > (mean + 6*standart_deviation):
        god_classes_dict['Class name'].append(classes_df['Class name'][ind])
        god_classes_dict['Number of methods'].append(classes_df['Number of methods'][ind])


""" Visualizing god classes in a DataFrame """
god_classes_df = pd.DataFrame(god_classes_dict)


def get_god_classes_paths(files):
    god_classes_paths = []
    for file in files:
        class_name = file.split('/')[-1].split('.java')[0]
        if god_classes_dict['Class name'].count(class_name) > 0:
            god_classes_paths.append(file)
    return god_classes_paths
