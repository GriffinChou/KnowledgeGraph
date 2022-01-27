# -*- coding:utf-8 -*-
"""
@author:griffinchou
@date: 2022.01.27
@function:爬取星座知识数据
"""
import requests
from lxml import etree
import pandas as pd
import re
base_url = "http://114.xixik.com/12xingzuo/"

# 爬取星座名称
def get_xingzuo_name(base_url):
    response = requests.get(base_url)
    response.encoding = "gbk"
    xingzuo_name = etree.HTML(response.text).xpath("/html/body/div[3]/div[2]/div/div/p/text()")
    # print(xingzuo_name)
    # for i in xingzuo_name:
    zh_name = re.findall(r"([\w] *.?座)", str(xingzuo_name), re.S)
    en_name = re.findall(r"[（](.*?)[）]", str(xingzuo_name), re.S)
    dataframe = {"星座名": zh_name,
                 "英文名": en_name}
    name_ = pd.DataFrame(dataframe)
    name_.to_csv("./dataset/xingzuo_name.csv")

    return ""

# 爬取星座的详细介绍
def get_xingzuo_data(base_url):
    zh_name = []
    latin_name = []
    date = []
    alia_name = []
    response = requests.get(base_url)
    response.encoding = "gbk"
    for i in range(2, 14):
        xingzuo_data = etree.HTML(response.text.replace("\t", "").replace("?", "")).xpath("/html/body/div[3]/div[5]/div[2]/div/table/tbody/tr[{}]/td/text()".format(i))
        zh_name.append(xingzuo_data[0])
        latin_name.append(xingzuo_data[1])
        date.append(xingzuo_data[2])
        alia_name.append(xingzuo_data[3])
    DF = {"星座":zh_name,
    "拉丁名":latin_name,
    "日期":date,
    "别名":alia_name}
    xingzuo_data = pd.DataFrame(DF)
    xingzuo_data.to_csv("./dataset/xingzuo_detail.csv")

    return ""

# 爬取星座的某一类（符号信息）数据
def get_xingzuo_fuhao(base_url):
    response = requests.get(base_url)
    response.encoding = "gbk"
    zh_name = []
    fuhao_ = []
    nengliang_ = []
    tedian_ = []
    for i in range(0, 12):
        fuhao = etree.HTML(response.text.replace("\t", "").replace("。", "")).xpath(
            "/html/body/div[3]/div[7]/div[2]/div/p[3+{}]/text()".format(4*i))
        nengliang = etree.HTML(response.text.replace("\t", "")).xpath(
            "/html/body/div[3]/div[7]/div[2]/div/p[4+{}]/text()".format(4*i))
        for iters in fuhao:
            zh_name.append(str(iters).split("符号")[0])
            fuhao_.append(str(iters).split("符号")[1])
        for iters in nengliang:
            nengliang_.append(str(iters).split("：")[1].split("。")[0])
            tedian_.append(str(iters).split("：")[1].split("。")[1])

    DF = {"星座名": zh_name,
    "符号": fuhao_,
    "符号能量": nengliang_,
          "特点": tedian_}
    pd.DataFrame(DF).to_csv("./dataset/fuhao.scv")

    return ""

# 爬取与某一星座匹配相关的数据
def get_peidui(base_url):
    response = requests.get(base_url)
    response.encoding = "gbk"
    a, b, c = [], [], []
    zhishu, bizhong, dianping = [], [], []
    friend_g, tongshi_g, diren_g, aimei_g, bupei_g = [], [], [], [], []

    pipei_data = etree.HTML(response.text.replace("\u3000", "").replace("\t", "").replace("\xa0", "")).xpath("/html/body/div[3]/div[8]/div[2]/div/p/strong/text()")
    for i in range(len(pipei_data)):
        if i % 4 != 0:
            zh_name = str(pipei_data[i]).split("星座")[0]
            dd = str(pipei_data[i]).split("星座")[1].split("：")
            # print((zh_name, dd[0], dd[1]))
            a.append(zh_name)
            b.append(dd[0])
            c.append(dd[1])

    data_detail = etree.HTML(response.text.replace("\u3000", "").replace("\t", "").replace("\xa0", "")).xpath(
        "/html/body/div[3]/div[8]/div[2]/div/p/text()")
    for i in data_detail:
        # if "指数：" in i or "评分：" in i:
        #     zhishu.append(str(i).split("：")[1])
        # elif "比重：" in i:
        #     # print(i)
        #     # print(str(i).split("比重："))
        #     bizhong.append(str(i).split("比重：")[1])
        if "点评：" in i:
            # print(i)
            # print("==========================", str(i).split("："))
            dianping.append(str(i).split("：")[1])
        elif "朋友组合：" in i:
            friend_g.append(str(i).split("：")[1])
        elif "同事组合：" in i:
            tongshi_g.append(str(i).split("：")[1])
        elif "敌人组合：" in i:
            diren_g.append(str(i).split("：")[1])
        elif "暧昧星座组合：" in i:
            aimei_g.append(str(i).split("：")[1])
        elif "最不配：" in i:
            bupei_g.append(str(i).split("：")[1])


    DF = {"星座最配": a,
    "排名": b,
    "星座名": c,
    "点评": dianping,
    }
    DF1 = {
    "星座":["白羊座", "金牛座", "双子座", "巨蟹座", "狮子座", "处女座", "天秤座", "天蝎座", "射手座", "摩羯座", "水瓶座", "双鱼座"],
    "最佳好友": friend_g,
    "最佳同事": tongshi_g,
    "敌人": diren_g,
    "暧昧星座": aimei_g,
    "最不配": bupei_g}

    # 存储数据
    pd.DataFrame(DF).to_csv("./dataset/pipei.csv")
    pd.DataFrame(DF1).to_csv("./dataset/guanxi.csv")

    return ""
if __name__ == "__main__":
    get_xingzuo_name(base_url)
    get_xingzuo_data(base_url)
    get_xingzuo_fuhao(base_url)
    get_peidui(base_url)