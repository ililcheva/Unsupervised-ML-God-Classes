import os
import javalang
import pandas as pd
from find_god_classes import *

# GOD_CLASSES_DICT = {
#     'Class name': ['XSDHandler', 'DTDGrammar', 'XIncludeHandler', 'CoreDocumentImpl'], 
#     'Number of methods': [118, 101, 116, 125]
# }

GOD_CLASSES_PATHS = get_god_classes_paths(files)

def get_fields(god_class):
    fields = []
    _, class_name = os.path.split(god_class)
    opened = open(god_class, 'r').read()
    tree = javalang.parse.parse(opened)
    for path, node in tree.filter(javalang.tree.ClassDeclaration):
        if node.name == class_name[:-5]:
            for member in node.body:
                if type(member) == javalang.tree.FieldDeclaration:
                    for declarator in member.declarators:
                        fields.append(declarator.name)
    return fields


def get_methods(god_class):
    methods = []
    methods_info = []
    _, class_name = os.path.split(god_class)
    opened = open(god_class, 'r').read()
    tree = javalang.parse.parse(opened)
    for path, node in tree.filter(javalang.tree.ClassDeclaration):
        if node.name == class_name[:-5]:
            for member in node.body:
                if type(member) == javalang.tree.MethodDeclaration:
                    if member.name not in methods:
                        fields = get_fields_accessed_by_method(member)
                        invoked_methods = get_methods_accessed_by_method(member)
                        methods.append(member.name)
                        methods_info.append({'name': member.name, 'accessed_fields': fields, 'invoked_methods': invoked_methods})
    return methods, methods_info

def get_fields_accessed_by_method(method):
    fields = []
    for path, node in method.filter(javalang.tree.MemberReference):
        if node.member not in fields:
            fields.append(node.member)
    return fields

def get_methods_accessed_by_method(method):
    methods = []
    for path, node in method.filter(javalang.tree.MethodInvocation):
        if node.member not in methods:
            methods.append(node.member)
    return methods


for god_class in GOD_CLASSES_PATHS:
    _, class_name = os.path.split(god_class)
    fields = get_fields(god_class)
    methods, methods_info = get_methods(god_class)
    columns = fields+methods
    feature_vector_df = pd.DataFrame(columns=['method_name']+columns)

    for method_info in methods_info:
        found_columns = method_info['accessed_fields'] + method_info['invoked_methods']
        vector = []
        for field in columns:
            if field not in found_columns:
                vector.append(0)
            else:
                vector.append(1)
        df = pd.DataFrame([[method_info['name']] + vector], columns=['method_name']+columns)
        feature_vector_df = feature_vector_df.append(df)

  
    if not os.path.exists('feature_vectors'):
        os.mkdir('feature_vectors')
    feature_vector_df.to_csv('feature_vectors/' + class_name[:-5] +'.csv')


