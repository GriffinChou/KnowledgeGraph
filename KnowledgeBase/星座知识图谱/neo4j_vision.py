# -*- coding:utf-8 -*-
from py2neo import Graph, Node, Relationship, NodeMatcher
import csv
"""
@author:griffinchou
@date: 2022.01.27
@function:将三元组数据用neo4j存储并可视化
"""

path = "./dataset/data.csv"
# 链接图数据库
graph = Graph("http://localhost:7474", user="neo4j", password="root")
def neo4j2vision():
    with open(path, 'r', encoding='utf-8') as f:
        data = csv.reader(f)
        for i in data:
            # 跳过标题行
            if data.line_num == 1:
                continue
            # print(i[1], i[2], i[3])
            # 定义节点
            start_node = Node("xingzuo", name=i[1])
            end_node = Node("value", name=i[3])
            # 定义关系
            guanxi = Relationship.type(i[2])
            ralationship = Relationship(start_node, i[2], end_node)
            # 画图
            graph.merge(guanxi(start_node, end_node), "xingzuo", "name")

    f.close()

if __name__ == "__main__":
    neo4j2vision()