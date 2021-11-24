# -*- coding:utf-8 -*-
import os
import sys
import time
import logging
import datetime
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
# logging
warnings.filterwarnings("ignore")
program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
logging.root.setLevel(level=logging.INFO)
logger.info("running %s" % ' '.join(sys.argv))

# plot图像上显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']


# plot画布设置
fig, ax = plt.subplots(1, 1)
# rotation: 旋转方向
ax.xticks(rotation=45, fontsize=10)
# 给定title，并在图上显示，如title="未来五天天气预测"
title="未来五天天气预测"
ax.title('{}原始数据&重采样数据&预测数据趋势线'.format(title))
# 读取数据
def read_dataset(PATH):
    df = pd.read_csv(PATH, encoding='gbk')
    # 将数据中的gather_time转换为可统计的时间戳序列
    df['DateTime'] = pd.to_datetime(df['gather_time'])
    # 转换为pandas的DataFrame格式
    datas = pd.DataFrame(df)
    # 用pivot_table，将时间列设为index，将观察对象列设为value，aggfuc采用mean填充
    data_ = pd.pivot_table(data=datas, values='net_rate', index='DateTime', aggfunc='mean').reset_index()
    # 按照时间重新设置索引
    dataset = data_.set_index('DateTime', inplace=True)

    return dataset, df

# 重采样
def resample_data(dataset):
    # 按t时间取均值重采样，以t内均值填充，并去除空值,如t=3h
    train_data = dataset.resample('3h').mean().dropna()
    return train_data

# 将时间字符串转换为固定的时间格式
def string_toDatetime(string):
    return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")

# 模型训练
def train_arima(df, train_data, start_time, end_time, arima_params, start_index, end_index):
    # 初始化ARIMA模型
    arima = ARIMA(train_data, order=(arima_params[0], arima_params[1], arima_params[2]))
    model = arima.fit()
    # 给定起始位置和结束位置，预测该index内的数据
    pre = model.predict(start_index, end_index, typ='levels')
    # 预测时间，给定起始时间和终止时间
    x = pd.date_range(string_toDatetime(start_time), string_toDatetime(end_time), periods=(end_index-start_index))
    # 训练数据图像
    ax.plot(train_data, color='red', label='原始数据走势')
    # 预测数据图像
    ax.plot(x, pre, color='green', label='预测走势')
    ax.gcf().subplots_adjust(bottom=0.15)
    # plt.show()
    # 均值线
    y = np.mean(train_data)
    z = np.std(train_data)
    # 1.5倍均线
    y2 = 1.5 * y
    # xmin取原始数据第一个时间，假设已经按时间排好序
    ax.hlines(y=y2, xmin=df["DateTime"][0], xmax=x[-1], color="black", label="1.5倍均值")
    ax.hlines(y=y, xmin=df["DateTime"][0], xmax=x[-1], color="blue", label="均值")
    ax.hlines(y=z, xmin=df["DateTime"][0], xmax=x[-1], color="purple", label="标准差")

    # 重新对预测数据和时间处理
    pred_data = list(zip(x, pre))
    # 添加箭头标注，注明预测数据点超出给定值并添加文字
    for i in pred_data:
        if (i[1] > y2).values == True: # 预测值大于1.5倍均值
            ax.annotate('异常点',
                         xy=(i[0], i[1]),  # 箭头末端位置
                         xytext=(i[0], i[1]+20),  # 文本起始位置
                         # 箭头属性设置
                         arrowprops=dict(facecolor='blue',
                                         shrink=1,  # 箭头的收缩比
                                         alpha=0.4,
                                         width=2,  # 箭身宽
                                         headwidth=5,  # 箭头宽
                                         hatch='--',  # 填充形状
                                         frac=0.6,  # 身与头比
                                         # 其它参考matplotlib.patches.Polygon中任何参数
                                         ),
                         )
    # 自适应最佳位置放置图标
    ax.legend(loc='best')
    # 保存图像，假设已经存在当前目录下的images文件夹
    ax.savefig('./images/{}.jpg'.format(title))
    ax.show()

    return pre

start_time = time.strftime("%Y-%m-%d %H:%M:%S")
end_time = ""
start_index = 3
end_index = 34
def main():
    # 第一个参数是数据的路径
    PATH = sys.argv[1]
    # arima_params是一个列表或元祖
    arima_params = sys.argv[2]
    resample = "True"
    dataset, df = read_dataset(PATH)
    # 判断是否需要重采样
    if resample is True:
        train_data = resample_data(dataset)
    else:
        train_data = dataset
    train_arima(df, train_data, arima_params, start_time, end_time, start_index, end_index)




if __name__ == '__main__':
    main()