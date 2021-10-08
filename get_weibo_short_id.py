import requests
import re
import pandas as pd
from openpyxl import Workbook

cookie = "WEIBOCN_FROM=1110006030; SUB=_2A25MVWzrDeRhGeFL61QY8SjLzzuIHXVvtnSjrDV6PUJbkdCOLXXykW1NQoYgCxNiYIQl0Y1yMkPkkWSYZOkYnU9h; _T_WM=94010261841; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4683893300528575%26luicode%3D20000061%26lfid%3D4683893300528575%26uicode%3D20000061%26fid%3D4683893300528575; XSRF-TOKEN=8e6ce5"
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
        result = re.findall(r'"id": (.*?),', resp.text, re.S)[1].strip()
        n_url = url.replace("status", result)
        print(n_url)
        # result = re.findall(r'"status": (.*?)"hotScheme"', resp.text, re.S)[0]
        # print(result)
        # w_url = f'https://m.weibo.cn/status/{result}'
        # ws.append([w_url])
        # wb.save(r"D:\weibo\weibo_8月\weibo_08_31\w_urls.xlsx")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    df = pd.read_excel(r"D:\weibo\weibo_9月\w_urls.xlsx")
    urls = df['文章链接']
    for url in urls:
        # note_id = url.split("/")[-1]
        # n_url = f"https://m.weibo.cn/status/{note_id}"
        # ws.append([n_url])
        # wb.save(r"D:\weibo\weibo_9月\long_url.xlsx")
        # print(url)
        get_weibo_short_id(url)
