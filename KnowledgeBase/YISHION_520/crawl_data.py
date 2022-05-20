# -*- coding:utf-8 -*-
import requests
import pandas as pd

url = "https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&appmsgid=2652393753&idx=1&comment_id=2405158113856290817&offset=0&limit=100&send_time=&sessionid=svr_eae7026d919&enterid=1653039686&uin=OTUzMDgyNzc1&key=99f14a33612c199098d149dd882675b3834a190f349ad935471967024fcb967a0b431be02843788af1d8901e20ced7e1c0408658586d1ded05c0f8f961c25df0d21b6bda22e16827f1fb1561974dcea6daac12553cee0437cefbd5e767046eab74df524846a1489878a650553768a13541b95fec8e1dbd8e40c989ea9409a92d&pass_ticket=hNTXDrUj7i7oSQdiySWmZBTQJI09PGWrLQp6J7kHIFyQYXZFXzBSUmlnHn2Z8n3C&wxtoken=777&devicetype=Windows%26nbsp%3B10%26nbsp%3Bx64&clientversion=6305002e&__biz=MjM5MDQ1NzQ0MA%3D%3D&appmsg_token=1166_RCKr66ofHPFhea77r-oNKKg3QxZmXNiWmvzQ8a8bWpk9rwlM6pIwniI5j2d9RADf4igQUYbujbm3svWx&x5=0&f=json"
headers = {"Cookie":"RK=HUBI+0tfdq; ptcz=3e1bdd5d8b6f94003309faff6d7c5377918efc51e0aad1d14b15f3230955c56d; pgv_pvid=5837567018; ied_qq=o0977085860; uin_cookie=o0977085860; _ga_0EKMG65RQ9=GS1.1.1622384269.3.1.1622384921.0; o_cookie=977085860; pac_uid=1_977085860; LW_sid=P1x6D2d2D839G0t5d974d2v2f3; tvfe_boss_uuid=9eceba8b00f5b09f; mobileUV=1_17a33d1fbc9_d1d25; _ga=GA1.2.617702023.1621348679; fqm_pvqid=b4b58042-b267-456b-b837-b3f5df9c2f2a; wwapp.vid=; wwapp.cst=; wwapp.deviceid=; rewardsn=; wxtokenkey=777; appmsg_token=1166_Iulo%2BlY33fDXi%2Femr-oNKKg3QxZmXNiWmvzQ8Va07v39MFCCfI0d487CLjcw2z1bLbVX2tKX9etOc2lT; wxuin=953082775; devicetype=Windows10x64; version=6305002e; lang=zh_CN; pass_ticket=hNTXDrUj7i7oSQdiySWmZBTQJI09PGWrLQp6J7kHIFyQYXZFXzBSUmlnHn2Z8n3C; wap_sid2=CJfHu8YDEooBeV9IQ1BlNWNPLU1KbmVOQ1NFNkpsYm1rSXJTaUtOYWdsNFdGLTRXTVdNaGI3b0REclhjSHJZRjlvblgtMTlQRlhsSEY0UzJaejd2d0Q0bl90RWhrRGZ4UDZBM2RXN0djRUZHNVBjczFwYXhUOURka2M5NWxSX3kxWldYQ1phektGZjcyc1NBQUF+MNWDnZQGOA1AAQ=="}

response = requests.get(url, headers=headers)
content = response.json()
datas = list(content.values())[6]
# print(datas)
nick_name, content, ip_wording = [], [], []
for data in datas:
    nick_name.append(data["nick_name"])
    content.append(data["content"])
    ip_wording.append([data["ip_wording"]["country_name"], data["ip_wording"]["province_name"], data["ip_wording"]["city_name"]])

df = {"微信昵称": nick_name,
      "评论内容": content,
      "ip地址": [[i] for i in ip_wording]}
dataset = pd.DataFrame(df).to_csv("./datas/yishion.csv")
