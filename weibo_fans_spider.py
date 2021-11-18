import time

import requests
import pandas as pd
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.append([
    "粉丝数",
    "评论数",
    "转发数"
])

cookie = "SINAGLOBAL=6527234529095.878.1632706024442; UOR=,,www.google.com.hk; ULV=1635232371340:4:2:1:9789622234864.035.1635232371337:1633676284515; SUB=_2A25Mc9rbDeRhGeNL61cZ8irPzDuIHXVvn-aTrDV8PUJbkNAKLWbNkW1NSOu9u3awWlaWQNVq8z7GNkaGzOBJb8V-; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWkQeOeXIa3Un.6dwp7CaYw5NHD95QfSK5f1hzXe0MNWs4Dqcjqi--RiK.XiKy2i--4i-zRi-20-c8uUPiy; XSRF-TOKEN=UhXN_cM0SjXroUGZ22q4LjUB; WBPSESS=784AcvWHjyhSLTMYqaBB2R0muMjGEdz8u8017ujja8B-rRUzTBnm7gsagnfGgQRZMwlpTaxKm8LttvPFZdErKii-SFpZiYXs46cBW0XsroeQSPX4pQNTxqD8G2kHL6OvMbuMCxTGgvCHnXX-mMo7LQ=="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'cookie': cookie,
    "Connection": "keep-alive",
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
}


def get_weibo(url, w_url):
    # p_total_num = ""
    fans = ""
    # z_total_num = ""
    rs = requests.get(headers=headers, url=w_url)
    if rs.content:
        rsp = rs.json()
        try:
            if rsp:
                fans = rsp["data"]["user"]["followers_count"]
                print(fans)
            # p_rsp = requests.get(url=p_url, headers=headers).json()
            # if p_rsp:
            #     p_total_num = p_rsp["data"]["total_number"]
            # z_rsp = requests.get(headers=headers, url=z_url).json()
            # if z_rsp:
            #     z_total_num = z_rsp["data"]["total_number"]
        except Exception as e:
            print(e)
    ws.append([url, fans])
    wb.save("D:/weibo/weibo_11月/p2结案数据双11月88VIP项目项目谦玛1.xlsx")


if __name__ == '__main__':
    df = pd.read_excel("D:/weibo/weibo_11月/p2结案数据双11月88VIP项目项目谦玛.xlsx", sheet_name="微博赠送")
    f_urls = df["发布链接"]
    # print(urls)
    for f_url in f_urls:
        # if "https://weibo.com/u/" in url:
        uid = f_url.split("/")[3]
        nid = f_url.split("/")[-1]
        info_url = "https://m.weibo.cn/profile/info?uid={}".format(uid)
        # p_url = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0".format(nid, nid)
        # z_url = "https://m.weibo.cn/api/statuses/repostTimeline?id={}&page=1".format(nid)
        # print(info_url)
        # get_weibo(info_url, z_url, p_url)
        get_weibo(f_url, info_url)
        time.sleep(3)
