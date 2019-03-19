# -*- coding: utf-8 -*-
from BuildGraph import BuildGraph
import os
import pandas as pd
import sys
from Config import *

# 提取csv表格中数据
data_path = sys.argv[1]
invoice_data = pd.read_csv(data_path, encoding='utf8')
# print(invoice_data)
# print(invoice_data.shape)

def data_extraction():
    """节点数据抽取"""

    # 取出关键列数据到list
    node_list_key = invoice_data[Config['key_column_name']].values.tolist()
    
    # 去除重复的关键列数据
    node_list_key = list(set(node_list_key))

    # 取出其他非空数据值到list
    node_list_value = invoice_data.astype('str').iloc[:,1:].values.tolist()
    node_list_value = [k for l in node_list_value for v in l for k in v.split('/') if v!='Null']
    
    # 去除重复的数据值
    node_list_value = list(set(node_list_value))
  
    return node_list_key, node_list_value


def relation_extraction():
    """联系数据抽取"""

    links_dict = {}
    key_list = []
    relation_list = []
    value_list = []

    for i in range(0, len(invoice_data)):
        m = 0
        name_node = invoice_data[Config['key_column_name']][i]
        while m < len(invoice_data.columns)-1:
            column_name = invoice_data.columns[m+1]
            value = invoice_data.astype('str')[column_name][i]
            if value != "Null":
                # 对包含“/”的数据值进行切分
                for k in value.split('/'):
                    relation_list.append(column_name)
                    value_list.append(k)
                    key_list.append(name_node)
            m += 1


    # 整合数据，将三个list整合成一个dict
    links_dict['key'] = key_list
    links_dict['relation'] = relation_list
    links_dict['value'] = value_list
    # 将数据转成DataFrame
    df_data = pd.DataFrame(links_dict)
    return df_data

if __name__ == '__main__':
    # 实例化对象
    print('Extract data...')
    node = data_extraction()
#     print(len(node[0]),len(node[1]))
    print('Extract relation...')
    relation = relation_extraction()
#     print(relation)
    graph = BuildGraph()
    print('Create Nodes...')
    graph.create_node(node[0], node[1])
    print('Create Relationship...')
    graph.create_relation(relation)
    print('Finish!')
