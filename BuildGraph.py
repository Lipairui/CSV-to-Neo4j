# -*- coding: utf-8 -*-
from py2neo import Node, Graph, Relationship, NodeMatcher
from Config import *

class BuildGraph(object):
    """将csv中数据存入neo4j"""

    def __init__(self):
        """建立连接"""
        # 设定Neo4j数据库链接地址和用户名密码
        link = Graph(Config['Neo4j_link'], username=Config['Neo4j_graph_username'], password=Config['Neo4j_graph_password'])
        self.graph = link
        # 定义label
        self.key_label = Config['key_label']
        self.value_label = Config['value_label']
        # 初始化清空图数据库
        self.graph.delete_all()

    def create_node(self, node_list_key, node_list_value):
        """建立节点"""
        
        for name in node_list_key:       
#             print('Create node for ',name)
            name_node = Node(self.key_label, name=name)
            self.graph.create(name_node)
            
        for name in node_list_value:
#             print('Create node for ',name)
            value_node = Node(self.value_label, name=name)
            self.graph.create(value_node)
        print('Create %d nodes...' %(len(node_list_key)+len(node_list_value)))
        
    def create_relation(self, df_data):
        """建立联系"""
        matcher = NodeMatcher(self.graph)
        m = 0
        for m in range(0, len(df_data)):
            try:
                rel = Relationship(matcher.match(self.key_label, name=df_data['key'][m]).first(),
                                   df_data['relation'][m], matcher.match(self.value_label, name=df_data['value'][m]).first())
                self.graph.create(rel)
            except AttributeError as e:
                print(e, m)
        print('Create %d relationships...' %len(df_data))