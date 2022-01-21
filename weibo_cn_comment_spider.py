import time
import pandas as pd
import requests
from lxml import etree
from openpyxl import Workbook

cookie = "SINAGLOBAL=6527234529095.878.1632706024442; UOR=,,www.google.com.hk; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWkQeOeXIa3Un.6dwp7CaYw5JpX5KMhUgL.Fo-feh-ReoB0S0M2dJLoIpnLxKnL1KBL12BLxK.LBonLBKSKqg_fMJ2t; ULV=1641960628527:8:2:1:3925243501454.585.1641960628407:1641542345529; ALF=1674013221; SSOLoginState=1642477221; SCF=Ak_bWPSqvc6NA3_kw05YbeE72JbVSXImnZcdfWZTqbwgfzY7BZ6w2qHEhym9GwNRsaKy-aitY9ed_SYAVBKSQgA.; SUB=_2A25M4kb2DeRhGeNL61cZ8irPzDuIHXVvlj8-rDV8PUNbmtAKLVjAkW9NSOu9u5cpB4fWxoPjNAtf4_uJbiJrLtja; XSRF-TOKEN=6pR02dY6_45ADAmjB1n-fKOn; WBPSESS=784AcvWHjyhSLTMYqaBB2R0muMjGEdz8u8017ujja8B-rRUzTBnm7gsagnfGgQRZqAAPc9f3-TXGkFGbfKm47_fMHxq13g1-hcppz8wf4tD1LORCk3gH_gpkgEV5hvZPNNjIZUQ_I2GlhCJO0Ie3EA=="
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
                wb.save(r'D:\weibo\weibo22_1月\weibo_01_18\微博评论.xlsx')
    except Exception as e:
        print(e)


if __name__ == '__main__':
    df = pd.read_excel(r'D:\weibo\weibo22_1月\weibo_01_18\#新年带点新年味回家#.xlsx')
    urls = df['发布链接']
    for url in urls:
        w_id = url.split("/")[-1]
        for i in range(20):
            url = f"https://weibo.cn/comment/{w_id}?&rl=0&page={i + 1}"
            get_comment(url)
            time.sleep(2)


