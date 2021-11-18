import time
import pandas as pd
import requests
from lxml import etree
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
ws.append([
    "评论内容"
])


def get_comment(w_url):
    # lst = ['陶瓷', '国风', '颜值', '小米MIX4', '审美', '入手 ', '购买', '中国']
    try:
        resp = requests.get(w_url, headers=headers)
        print(w_url)
        html = etree.HTML(resp.text.encode("utf-8"))
        comments = html.xpath("//span[@class='ctt']")
        for comment in comments:
            content = comment.xpath("./text()")
            content = "".join(str(j) for j in content)
            # for j in lst:
            #     if j in content:
            if content.startswith(':'):
                continue
            else:
                print(content)
                ws.append([content])
                wb.save(r'D:\weibo\weibo_11月\weibo_11_18\双11惊喜宝箱_评论_1.xlsx')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    df = pd.read_excel(r'D:\weibo\weibo_11月\weibo_11_18\#双11惊喜宝箱#.xlsx')
    urls = df['发布链接']
    for url in urls:
        w_id = url.split("/")[-1]
        for i in range(20):
            url = f"https://weibo.cn/comment/{w_id}?&rl=0&page={i + 1}"
            get_comment(url)
            time.sleep(2)


