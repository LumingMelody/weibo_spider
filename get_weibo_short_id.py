import requests
import re
import pandas as pd
from openpyxl import Workbook

cookie = "SCF=ArJTlx5JAmfMMKsVG7OAs2l4yApmQVJhD9qWf4GqsANvbekL3SejvAW8yzcA-ca5fytwhAX0bdSURzuye5w2eDc.; SUB=_2A25Nz1uTDeRhGeFL61QY8SjLzzuIHXVvMGXbrDV6PUJbktB-LUj5kW1NQoYgCzzDgFyGLTd_TX2Wn694GrTYj_rQ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWndaMrC7jCK8pQ3JIVbkC45NHD95QNSK5c1K2cS0BNWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNS0-7So.pSoMXS7tt; _T_WM=61314815087; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4659607551345667%26luicode%3D20000061%26lfid%3D4659607551345667"
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
ws.append(['文章链接'])


def get_weibo_short_id(url):
    resp = requests.get(url, headers=headers)
    try:
        result = re.findall(r'"bid": (.*?),', resp.text, re.S)[0]
        # result = re.findall(r'"status": (.*?)"hotScheme"', resp.text, re.S)[0]
        # print(result)
        w_url = f'https://m.weibo.cn/status/{result}'
        ws.append([w_url])
        wb.save(r"D:\weibo\weibo_8月\weibo_08_31\weibo_short_url.xlsx")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    df = pd.read_excel(r"D:\weibo\weibo_8月\weibo_08_31\weibo_urls.xlsx")
    urls = df['文章链接']
    for url in urls:
        print(url)
        get_weibo_short_id(url)
