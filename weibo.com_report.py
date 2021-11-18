import time

import pandas as pd
import re

import requests
from openpyxl import Workbook

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

wb = Workbook()
ws = wb.active
ws.append(['文章链接', '转发', '评论', '点赞'])


def get_report(url, w_id):
    w_url = f"https://weibo.com/ajax/statuses/show?id={w_id}"
    resp_ = requests.get(url=w_url, headers=headers).text
    print(resp_)
    if "400 Bad Request" not in resp_:
        resp = requests.get(url=w_url, headers=headers).json()
        print(resp)
        reposts_count = resp['reposts_count']
        comments_count = resp['comments_count']
        attitudes_count = resp['attitudes_count']
        print([url, reposts_count, comments_count, attitudes_count])
        ws.append([url, reposts_count, comments_count, attitudes_count])
        wb.save(r"D:\weibo\weibo_11月\双11视频定人转评赞1.xlsx")
    else:
        ws.append([url, 0, 0, 0])
        wb.save(r"D:\weibo\weibo_11月\weibo_11_16\weibo_11_16_1.xlsx")


if __name__ == '__main__':
    df = pd.read_excel(r"D:\weibo\weibo_11月\weibo_11_16\weibo_urls_1.xlsx")
    urls = df['发布链接']
    for url in urls:
        print(url)
        w_id = url.split('/')[-1].split('?')[0]
        get_report(url, w_id)
        time.sleep(3)

