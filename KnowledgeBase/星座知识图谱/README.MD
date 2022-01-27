# 星座知识图谱
网上爬取与星座有关的数据，然后进行数据处理，并以三元组的形式保存为csv文件，然后将不同的csv文件合并成一个csv，并用neo4j图数据库存储和显示。


## 用法
`python crawl_datas.py`爬取数据，`python general_data.py`处理数据，`python neo4j_vision.py`存储并可视化数据。

## 数据
爬取的数据保存在当前目录下的dataset目录下。

## 结果
! [text ](./images/demo.png)

## 环境

Python 3.8+

pandas

py2neo

requests

lxml

re








## 链接
- https://pypi.org/project/py2neo/
