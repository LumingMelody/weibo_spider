import datetime
import time

import pandas as pd
import re

import requests
from openpyxl import Workbook

from mweibo_topic_spider_helper import format_weibo_posttime

cookie = "SINAGLOBAL=6527234529095.878.1632706024442; UOR=,,www.google.com.hk; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWkQeOeXIa3Un.6dwp7CaYw5JpX5KMhUgL.Fo-feh-ReoB0S0M2dJLoIpnLxKnL1KBL12BLxK.LBonLBKSKqg_fMJ2t; ULV=1641960628527:8:2:1:3925243501454.585.1641960628407:1641542345529; ALF=1673951518; SSOLoginState=1642415519; SCF=Ak_bWPSqvc6NA3_kw05YbeE72JbVSXImnZcdfWZTqbwgt88ZgamfIl4h6KA6rRGXMIx1bb-edzYLYB9LfGBz80E.; SUB=_2A25M4TXwDeRhGeNL61cZ8irPzDuIHXVvlyA4rDV8PUNbmtAKLVfDkW9NSOu9uyF74SQbis0zVQctLG4C5FgMBhJM; XSRF-TOKEN=pO3578lR5PjwK-DrU3d5lq4r; WBPSESS=784AcvWHjyhSLTMYqaBB2R0muMjGEdz8u8017ujja8B-rRUzTBnm7gsagnfGgQRZMwlpTaxKm8LttvPFZdErKpT6UbbLzZkv3MXGAJdUdoIN83Ipc-S4s7UxpnDVxK3FYBBgz75clFMZOEXjDvKqLQ=="

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
ws.append(['文章链接', '转发', '评论', '点赞', '发布时间', '播放量'])


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
        # 文章创建时间
        create_time = format_weibo_posttime(resp["created_at"]).replace("+0800", "")
        # print(create_time)
        article_time = datetime.datetime.strptime(create_time, "%a %b %d %H:%M:%S %Y")
        online_users = ""
        # if 'page_info' in resp.keys():
        #     if "media_info" in resp['page_info'].keys():
        #         online_users = resp['page_info']['media_info']['online_users']
        #     else:
        #         online_users = "Null"
        print([url, reposts_count, comments_count, attitudes_count, article_time, online_users])
        ws.append([url, reposts_count, comments_count, attitudes_count, article_time, online_users])
        # wb.save(r"D:\weibo\weibo_11月\weibo_11_19\weibo_result.xlsx")
    else:
        ws.append([url, 0, 0, 0])
    wb.save(r"D:\weibo\weibo22_1月\weibo_01_21\01_21_weibo_result.xlsx")


if __name__ == '__main__':
    df = pd.read_excel(r"D:\weibo\weibo22_1月\weibo_01_21\weibo_urls.xlsx")
    urls = df['发布链接']
    for url in urls:
        print(url)
        if '?' in url:
            w_id = url.split('/')[-1].split('?')[0]
        else:
            w_id = url.split('/')[-1]
        get_report(url, w_id)
        time.sleep(1)
