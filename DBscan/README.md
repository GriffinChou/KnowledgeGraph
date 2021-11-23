#算法介绍
DBSCAN（Density-Based Spatial Clustering of Applications with Noise，具有噪声的基于密度的聚类方法）是一种基于密度的空间聚类算法。该算法将具有足够密度的区域划分为簇，并在具有噪声的空间数据库中发现任意形状的簇，它将簇定义为密度相连的点的最大集合。
#参数介绍
Ε邻域：给定对象半径为Ε内的区域称为该对象的Ε邻域；
核心对象：如果给定对象Ε邻域内的样本点数大于等于MinPts，则称该对象为核心对象；
直接密度可达：对于样本集合D，如果样本点q在p的Ε邻域内，并且p为核心对象，那么对象q从对象p直接密度可达。
密度可达：对于样本集合D，给定一串样本点p1,p2….pn，p= p1,q= pn,假如对象pi从pi-1直接密度可达，那么对象q从对象p密度可达。
密度相连：存在样本集合D中的一点o，如果对象o到对象p和对象q都是密度可达的，那么p和q密度相联。
#功能介绍
本项目算法提供对单一指标数据的聚类结果展示，第一个参数是数据的路径，第二个参数是选择的dbscan模型，不同的dbscan模型会做出不同聚类结果的图。
#依赖介绍
- python:3.8
- numpy:1.21.1
- sklearn:1.0
- pandas:1.3.3
- matplotlib:3.4.3
#程序调用
python readcsv_dbscan.py 数据path dbscan的type，如：python ./dataset/test.csv best

#案例截图
[Image description](./images/dbscan_model.png)

# 感谢
本项目知识个人的一个小demo。
