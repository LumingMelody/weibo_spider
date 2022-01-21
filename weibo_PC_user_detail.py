import time

import requests
import pandas as pd
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.append([
    '用户名',
    '粉丝数',
    '用户认证信息',
    '主页链接'
])

cookie = "_ga=GA1.2.954032487.1637046479; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWndaMrC7jCK8pQ3JIVbkC45NHD95QNSK5c1K2cS0BNWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNS0-7So.pSoMXS7tt; _T_WM=25809315740; MLOGIN=1; SCF=Ak_bWPSqvc6NA3_kw05YbeE72JbVSXImnZcdfWZTqbwguRl-7t5hqVSgx9M-bJLM4ja_AfykUjSZrhqAbjwV880.; SUB=_2A25M4kfCDeRhGeFL61QY8SjLzzuIHXVsLWmKrDV6PUJbktCOLUrkkW1NQoYgC00_veM5ruTOMydcyf09PR4zgJHD; SSOLoginState=1642477458; WEIBOCN_FROM=1110106030; _gid=GA1.2.107700197.1642490934; XSRF-TOKEN=099369; M_WEIBOCN_PARAMS=oid%3D4724070970820638%26luicode%3D20000174%26lfid%3D4724070970820638%26uicode%3D20000174"
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


def get_weibo_user(u_id, w_url):
    try:
        resp = requests.get(url=w_url, headers=headers).json()
        user_info = resp['data']['user']
        print(user_info)
        user_name = user_info['screen_name']
        user_desc = user_info['description']
        user_fans = user_info['followers_count']
        user_url = f"https://weibo.com/u/{u_id}"
        if 'verified_reason' in user_info.keys():
            user_verified = user_info['verified_reason']
        else:
            user_verified = ""
        user_desc_verified = str(user_desc) + str(user_verified)
        ws.append([user_name, u_id, user_fans, user_desc_verified, user_url])
    except Exception as e:
        print(e)
    wb.save(r"D:\weibo\weibo22_1月\weibo_01_20\weibo_index_result_.xlsx")


if __name__ == '__main__':
    df = pd.read_excel(r"D:\weibo\weibo22_1月\weibo_01_20\weibo_urls.xlsx")
    urls = df['发布链接']
    for url in urls:
        # if '?' in url:
        #     u_id = url.split("/")[-1].split('?')[0]
        # else:
        u_id = url.split("/")[-2]
        u_url = f"https://weibo.com/ajax/profile/info?uid={u_id}"
        print(u_url)
        get_weibo_user(u_id, u_url)
        time.sleep(1)
