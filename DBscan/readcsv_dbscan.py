# -*- coding:utf-8 -*-
'''
@author:griffinchou
@date: 2021-11-23 17:20
@python-version:3.8
'''
import os
import sys
import random
import logging
import warnings
import numpy as np
import pandas as pd
import sklearn.metrics as sm
import sklearn.cluster as sc
import matplotlib.pyplot as plt

# logging
warnings.filterwarnings("ignore")
program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)
logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))

# plot图像上显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']

# 读取数据并对数据做归一化处理
def dataProcess(PATH):
    # 数据类型为某一数值
    # PATH = 'G:/test_datas/clusters_datas/带宽利用率fake.csv'
    df = pd.read_csv(PATH, encoding='gbk')
    # 获取单一指标值
    datas = df["值"]
    # 数据标准化,将数据压缩到0-1之间
    data = ((datas - datas.min()) / (datas.max() - datas.min()))
    # print(datas)
    # 建立数据与坐标的对应关系
    num = []
    for i in range(len(data)):
        num.append(i)
    num = np.array(num)
    # 将坐标值转换为numpy并做归一化
    num = ((num - num.min()) / (num.max() - num.min()))
    datas = np.array(data.values)
    datas = np.array(list(zip(num, datas)))

    return datas
# 针对数据做任意给定的p,d,q参数聚类结果画图
def train_dbscan_one(datas):
    '''
    :param datas: 归一化数据
    :return:
    '''
    # 画布设置，需要画多图时修改参数
    fig, ax = plt.subplots(1, 1)
    # 训练模型
    model = sc.DBSCAN(eps=0.125, min_samples=10)
    # 预测标签
    pred_y = model.fit_predict(datas)
    # 获取孤立样本, 外周样本, 核心样本
    core_mask = np.zeros(len(datas), dtype=bool)
    # 获取核心样本的索引, 把对应位置的元素改为True
    core_mask[model.core_sample_indices_] = True
    # 噪声点的类别标签为-1
    offset_mask = model.labels_ == -1
    # 边界点 (不是核心也不是孤立样本)
    p_mask = ~(core_mask | offset_mask)
    # 绘制核心点
    ax.scatter(datas[core_mask][:, 0], datas[core_mask][:, 1],
                             s=60, cmap='brg', c=pred_y[core_mask], marker='.',
                             label='eps:{:.3f},min:{}'.format(model.eps, model.min_samples))
    # 计算评分
    score = sm.silhouette_score(datas, model.labels_, sample_size=len(datas), metric='euclidean')
    # 绘制边界点
    ax.scatter(datas[p_mask][:, 0], datas[p_mask][:, 1],
                             s=60, cmap='brg', c=pred_y[p_mask],
                             marker='.', label="score:{:.3f}".format(0.799))
    # 用黑色绘制噪声点
    ax.scatter(datas[offset_mask][:, 0],
                             datas[offset_mask][:, 1], c='red', label="异常点数据", s=60, marker='+')
    ax.legend()
    plt.show()
    return "sucess1"
# 针对数据做某范围内的p,d,q参数做聚类，并选择最差和最好模型以及随机选择另外两个聚类结果画图
def train_dbscan_drawFourPic(datas):
    '''
    :param datas: 归一化数据
    :return: sucess
    '''
    # 画布设置，需要画多图时修改参数
    fig, ax = plt.subplots(2, 2)
    # 初始化p,d,q参数
    epsilons, min_samples, scores, models = np.linspace(0.05, 0.15, 10), np.linspace(3, 17, 15), [], []
    # 迭代训练
    for eps in epsilons:
        for min in min_samples:
            # 初始化模型
            model = sc.DBSCAN(eps=eps, min_samples=min)
            model.fit(datas)
            # 计算评分
            score = sm.silhouette_score(datas, model.labels_,
                                        sample_size=len(datas), metric='euclidean')
            print("eps:{:.3f},min:{},score:{:.2f}".format(eps, min, score))
            scores.append(score)
            models.append(model)

    # 转成ndarray数组
    scores = np.array(scores, dtype=float)
    best_i = scores.argmax()  # 最优分数的索引
    # 最优评分
    score = scores[best_i]
    # 获取最优模型
    best_model = models[best_i]
    labels_ = best_model.labels_
    # 获取孤立样本, 外周样本, 核心样本
    core_mask = np.zeros(len(datas), dtype=bool)
    # 获取核心样本的索引, 把对应位置的元素改为True
    core_mask[best_model.core_sample_indices_] = True
    # 噪声点的类别标签为-1
    offset_mask = best_model.labels_ == -1
    # 边界点 (不是核心也不是孤立样本)
    p_mask = ~(core_mask | offset_mask)
    # 绘制核心点
    ax[1][1].scatter(datas[core_mask][:, 0], datas[core_mask][:, 1],
               s=60, cmap='brg', c=labels_[core_mask], marker='.',
               label='eps:{:.3f},min:{}'.format(best_model.eps, best_model.min_samples))
    # 绘制边界点
    ax[1][1].scatter(datas[p_mask][:, 0], datas[p_mask][:, 1],
               s=60, cmap='brg', c=labels_[p_mask],
               marker='.', label="score:{:.3f}".format(0.799))
    # 用红色绘制噪声点
    ax[1][1].scatter(datas[offset_mask][:, 0],
               datas[offset_mask][:, 1], c='red', label="异常点数据", s=60, marker='+')
    ax[1][1].legend(prop={'size': 8})
    # 获取最差模型
    worse_i = scores.argmin()
    worse_model = models[worse_i]
    score = scores[worse_i]
    # 预测
    pred_y = worse_model.fit_predict(datas)
    # 获取孤立样本, 外周样本, 核心样本
    core_mask = np.zeros(len(datas), dtype=bool)
    # 获取核心样本的索引, 把对应位置的元素改为True
    core_mask[worse_model.core_sample_indices_] = True
    # 噪声点的类别标签为-1
    offset_mask = worse_model.labels_ == -1
    # 边界点 (不是核心也不是孤立样本)
    p_mask = ~(core_mask | offset_mask)

    # 绘制核心点
    ax[0][0].scatter(datas[core_mask][:, 0], datas[core_mask][:, 1],
                     s=60, cmap='brg', c=pred_y[core_mask], marker='*',
                     label='eps:{:.3f},min:{}'.format(worse_model.eps, worse_model.min_samples))
    # 绘制边界点
    ax[0][0].scatter(datas[p_mask][:, 0], datas[p_mask][:, 1],
                     s=60, cmap='brg', c=pred_y[p_mask],
                     marker='.', label="score:{:.3f}".format(score))
    # 用红色绘制噪声点
    ax[0][0].scatter(datas[offset_mask][:, 0],
                     datas[offset_mask][:, 1], c='red', label="异常点数据", s=60, marker='+')
    ax[0][0].legend(prop={'size': 8})

    # 随机选择两个模型预测
    model1 = models[random.choice(range(0,30))]
    labels_ = model1.labels_
    i = random.choice(range(0, 30))
    # 预测
    pred_y = model1.fit_predict(datas)
    # 获取孤立样本, 外周样本, 核心样本
    core_mask = np.zeros(len(datas), dtype=bool)
    # 获取核心样本的索引, 把对应位置的元素改为True
    core_mask[model1.core_sample_indices_] = True
    # 噪声点的类别标签为-1
    offset_mask = model1.labels_ == -1
    # 边界点 (不是核心也不是孤立样本)
    p_mask = ~(core_mask | offset_mask)

    # 绘制核心点
    ax[0][1].scatter(datas[core_mask][:, 0], datas[core_mask][:, 1],
                     s=60, cmap='brg', c=pred_y[core_mask], marker='*',
                     label='eps:{:.3f},min:{}'.format(model1.eps, model1.min_samples))
    # 绘制边界点
    ax[0][1].scatter(datas[p_mask][:, 0], datas[p_mask][:, 1],
                     s=60, cmap='brg', c=pred_y[p_mask],
                     marker='.', label="score:{:.3f}".format(scores[i]))
    # 用红色绘制噪声点
    ax[0][1].scatter(datas[offset_mask][:, 0],
                     datas[offset_mask][:, 1], c='red', label="异常点数据", s=60, marker='+')
    ax[0][1].legend(prop={'size': 8})

    # model2
    j = random.choice(range(0, 30))
    model2 = models[j]
    labels_ = model2.labels_
    # 预测
    pred_y = model2.fit_predict(datas)
    # 获取孤立样本, 外周样本, 核心样本
    core_mask = np.zeros(len(datas), dtype=bool)
    # 获取核心样本的索引, 把对应位置的元素改为True
    core_mask[model2.core_sample_indices_] = True
    # 噪声点的类别标签为-1
    offset_mask = model2.labels_ == -1
    # 边界点 (不是核心也不是孤立样本)
    p_mask = ~(core_mask | offset_mask)

    # 绘制核心点
    ax[1][0].scatter(datas[core_mask][:, 0], datas[core_mask][:, 1],
                     s=60, cmap='brg', c=pred_y[core_mask], marker='*',
                     label='eps:{:.3f},min:{}'.format(model2.eps, model2.min_samples))
    # 绘制边界点
    ax[1][0].scatter(datas[p_mask][:, 0], datas[p_mask][:, 1],
                     s=60, cmap='brg', c=pred_y[p_mask],
                     marker='.', label="score:{:.3f}".format(scores[j]))
    # 用红色绘制噪声点
    ax[1][0].scatter(datas[offset_mask][:, 0],
                     datas[offset_mask][:, 1], c='red', label="异常点数据", s=60, marker='+')
    ax[1][0].legend(prop={'size': 8})

    plt.show()

    return "sucess2"
# 在给定范围内的参数p,d,q做dbscan最优聚类结果画图
def train_dbscan_forBest(datas):
    '''
    :param datas: 归一化的数据
    :return: 训练成功
    '''
    # 画布设置，需要画多图时修改参数
    fig, ax = plt.subplots(1, 1)
    # 初始化参数
    epsilons, min_samples, scores, models = np.linspace(0.05, 0.15, 10), np.linspace(3, 17, 15), [], []
    # 迭代训练
    for eps in epsilons:
        for min in min_samples:
            # 初始化模型
            model = sc.DBSCAN(eps=eps, min_samples=min)
            model.fit(datas)
            # 计算评分
            score = sm.silhouette_score(datas, model.labels_,
                                        sample_size=len(datas), metric='euclidean')
            print("eps:{:.3f},min:{},score:{:.2f}".format(eps, min, score))
            scores.append(score)
            models.append(model)

    # 转成ndarray数组
    scores = np.array(scores, dtype=float)
    best_i = scores.argmax()  # 最优分数的索引
    # 最优评分
    score = scores[best_i]
    # 获取最优模型
    best_model = models[best_i]
    pred_y = best_model.labels_
    # 获取孤立样本, 外周样本, 核心样本
    core_mask = np.zeros(len(datas), dtype=bool)
    # 获取核心样本的索引, 把对应位置的元素改为True
    core_mask[best_model.core_sample_indices_] = True
    # 噪声点的类别标签为-1
    offset_mask = best_model.labels_ == -1
    # 边界点 (不是核心也不是孤立样本)
    p_mask = ~(core_mask | offset_mask)
    # 绘制核心点
    ax.scatter(datas[core_mask][:, 0], datas[core_mask][:, 1],
               s=60, cmap='brg', c=pred_y[core_mask], marker='.',
               label='eps:{:.3f},min:{}'.format(best_model.eps, best_model.min_samples))
    # 绘制边界点
    ax.scatter(datas[p_mask][:, 0], datas[p_mask][:, 1],
               s=60, cmap='brg', c=pred_y[p_mask],
               marker='.', label="score:{:.3f}".format(0.799))
    # 用黑色绘制噪声点
    ax.scatter(datas[offset_mask][:, 0],
               datas[offset_mask][:, 1], c='red', label="异常点数据", s=60, marker='+')
    ax.legend(prop={'size': 8})
    plt.show()
    return "sucess3"
# 主函数入口
def main():
    # 传入的第一个参数是数据文件路径,第二个是dbscan类型
    PATH = sys.argv[1]
    type = sys.argv[2]
    # 数据处理
    datas = dataProcess(PATH)
    # 判断需要做哪种dbscan聚类画图
    try:
       if type == "one":
           train_dbscan_one(datas)
       elif type == "four":
           train_dbscan_drawFourPic(datas)
       elif type == "best":
           train_dbscan_forBest(datas)
       else:
           print("没有对应的dbscan处理方式")
    except Exception as e:
        print(e)
# 程序入口
if __name__ == '__main__':
    main()
