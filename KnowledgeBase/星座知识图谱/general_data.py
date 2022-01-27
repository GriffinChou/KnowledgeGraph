# -*- coding:utf-8 -*-
"""
@author:griffinchou
@date: 2022.01.27
@function:将爬取的几个csv数据处理为一个csv文件
"""
import pandas as pd
def data_process():
    path1 = "./dataset/fuhao.scv"
    path2 = "./dataset/guanxi.csv"
    path3 = "./dataset/pipei.csv"
    path4 = "./dataset/xingzuo_detail.csv"
    dt1 = pd.read_csv(path1)
    dt2 = pd.read_csv(path2)
    dt3 = pd.read_csv(path3)
    dt4 = pd.read_csv(path4)
    dt1_df1 = {"实体": dt1["星座名"],
         "属性": dt1.columns[2],
         "属性值": dt1["符号"]}
    dt1_df2 = {"实体": dt1["星座名"],
         "属性": dt1.columns[3],
         "属性值": dt1["符号能量"]}
    dt1_df3 = {"实体": dt1["星座名"],
         "属性": dt1.columns[4],
         "属性值": dt1["特点"]}


    dt2_df1 = {"实体": dt2["星座"],
               "属性": dt2.columns[2],
              "属性值": dt2["最佳好友"]}
    dt2_df2 = {"实体": dt2["星座"],
               "属性": dt2.columns[3],
              "属性值": dt2["最佳同事"]}
    dt2_df3 = {"实体": dt2["星座"],
               "属性": dt2.columns[4],
              "属性值": dt2["敌人"]}
    dt2_df4 = {"实体": dt2["星座"],
               "属性": dt2.columns[5],
              "属性值": dt2["暧昧星座"]}
    dt2_df5 = {"实体": dt2["星座"],
               "属性": dt2.columns[6],
              "属性值": dt2["最不配"]}


    dt3_df1 = {"实体": dt3["星座最配"],
               "属性": dt3["排名"],
              "属性值": dt3["星座名"]}
    dt3_df5 = {"实体": dt3["星座最配"],
               "属性": dt3.columns[4],
              "属性值": dt3["点评"]}

    dt4_df1 ={"实体": dt4["星座"],
         "属性": dt4.columns[2],
         "属性值": dt4["拉丁名"]}
    dt4_df2 ={"实体": dt4["星座"],
         "属性": dt4.columns[3],
         "属性值": dt4["日期"]}
    dt4_df3 ={"实体": dt4["星座"],
         "属性": dt4.columns[4],
         "属性值": dt4["别名"]}

    # d = (dt1_df1, dt1_df2, dt1_df3, dt2_df4,
    #      dt2_df2, dt2_df3, dt2_df4, dt2_df5,
    #      dt3_df1, dt3_df5,
    #      dt4_df1, dt4_df2, dt4_df3)

    dd = pd.DataFrame(dt1_df1).append(pd.DataFrame(dt1_df2)).append(pd.DataFrame(dt1_df3))
    dd2 = dd.append(pd.DataFrame(dt2_df1)).append(pd.DataFrame(dt2_df2)).append(pd.DataFrame(dt2_df3)).append(pd.DataFrame(dt2_df4)).append(pd.DataFrame(dt2_df5))
    dd3 = dd2.append(pd.DataFrame(dt3_df1)).append(pd.DataFrame(dt3_df5))
    dd4 = dd3.append(pd.DataFrame(dt4_df1)).append(pd.DataFrame(dt4_df2)).append(pd.DataFrame(dt4_df3))
    dd4.to_csv("./dataset/data.csv")

    return ""

if __name__ == "__main__":
    data_process()
