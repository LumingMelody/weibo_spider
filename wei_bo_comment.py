from lxml import etree
import requests
import re
import time
import pandas as pd

from openpyxl import Workbook

cookie = "SCF=ArJTlx5JAmfMMKsVG7OAs2l4yApmQVJhD9qWf4GqsANvbekL3SejvAW8yzcA-ca5fytwhAX0bdSURzuye5w2eDc.; SUB=_2A25Nz1uTDeRhGeFL61QY8SjLzzuIHXVvMGXbrDV6PUJbktB-LUj5kW1NQoYgCzzDgFyGLTd_TX2Wn694GrTYj_rQ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWndaMrC7jCK8pQ3JIVbkC45NHD95QNSK5c1K2cS0BNWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNS0-7So.pSoMXS7tt; _T_WM=61314815087; WEIBOCN_FROM=1110005030; MLOGIN=1; XSRF-TOKEN=4be350; M_WEIBOCN_PARAMS=oid%3D4659607551345667%26luicode%3D20000061%26lfid%3D4659607551345667%26uicode%3D20000061%26fid%3D4659607551345667"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'cookie': cookie,
    "Connection": "keep-alive",
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    "x-requested-with": "XMLHttpRequest",
    "x-xsrf-token": "4be350",
}
headers2 = {
    # ":authority": "m.weibo.cn",
    # ":method": "GET",
    # ":path": "/comments/hotflow?id=4659607551345667&mid=4659607551345667&max_id=144075673797694&max_id_type=0",
    # ":scheme": "https",
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9",
    "cookie": "SCF=ArJTlx5JAmfMMKsVG7OAs2l4yApmQVJhD9qWf4GqsANvbekL3SejvAW8yzcA-ca5fytwhAX0bdSURzuye5w2eDc.; SUB=_2A25Nz1uTDeRhGeFL61QY8SjLzzuIHXVvMGXbrDV6PUJbktB-LUj5kW1NQoYgCzzDgFyGLTd_TX2Wn694GrTYj_rQ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWndaMrC7jCK8pQ3JIVbkC45NHD95QNSK5c1K2cS0BNWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNS0-7So.pSoMXS7tt; _T_WM=61314815087; WEIBOCN_FROM=1110005030; MLOGIN=1; XSRF-TOKEN=4be350; M_WEIBOCN_PARAMS=oid%3D4659607551345667%26luicode%3D20000061%26lfid%3D4659607551345667%26uicode%3D20000061%26fid%3D4659607551345667",
    "mweibo-pwa": "1",
    "referer": "https://m.weibo.cn/detail/4659607551345667",
    # "sec-fetch-dest": " empty",
    "sec-fetch-mode": "cors",
    # "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Mobile Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
    "x-xsrf-token": "4be350",
}
wb = Workbook()
ws = wb.active
ws.append([
    "用户名",
    "评论内容"
])

# 代理服务器
proxyHost = "forward.apeyun.com"
proxyPort = "9082"
# 代理隧道验证信息
proxyUser = "2021040800226731834"
proxyPass = "pA7prxttyuCTFjwM"
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}
proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}

lst = ['小米MIX4' 'MIX', '漫画', '性能', '外观', '颜色', '小米平板5', '价格', '购买', '入手', '陶瓷', '影青灰']


def get_weibo_comments(w_url):
    resp = requests.get(url=w_url, headers=headers).json()
    print(w_url)
    print(resp)
    if resp['ok'] == 0:
        return
    # while "max_id" in resp['data']:
    try:
        items = resp['data']['data']
        for item in items:
            comment = re.sub(r'<.*?>', '', item['text'])
            user_name = item['user']['screen_name']
            for i in lst:
                if i in comment:
                    ws.append([user_name, comment])
        # max_id = resp['data']['max_id']
        # next_url = f"https://m.weibo.cn/comments/hotflow?id=4659607551345667&mid=4659607551345667&max_id={max_id}&max_id_type=0"
        # print(next_url)
        # response = requests.get(url=next_url, headers=headers2, proxies=proxies).json()
        # print(response)
        # items = response['data']['data']
    except Exception as e:
        print(e)
    wb.save(r"D:\weibo\weibo_8月\weibo_08_26\weibo_xiaomi.xlsx")


if __name__ == '__main__':
    wd = pd.read_excel(r"D:\weibo\weibo_7月\weibo_07_19\urls.xlsx")
    urls = wd['文章链接']
    for url in urls:
        n_id = url.split("/")[-1]
        api_url = f"https://m.weibo.cn/comments/hotflow?id={n_id}&mid={n_id}"
        get_weibo_comments(api_url)
    # api_url = "https://m.weibo.cn/comments/hotflow?id=4659607551345667&mid=4659607551345667&max_id_type=0"
    # get_weibo_comments(api_url)
