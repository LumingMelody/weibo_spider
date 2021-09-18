import time
import pandas as pd
import requests
from lxml import etree
from openpyxl import Workbook

cookie = 'SCF=ArJTlx5JAmfMMKsVG7OAs2l4yApmQVJhD9qWf4GqsANvbekL3SejvAW8yzcA-ca5fytwhAX0bdSURzuye5w2eDc.; SUB=_2A25Nz1uTDeRhGeFL61QY8SjLzzuIHXVvMGXbrDV6PUJbktB-LUj5kW1NQoYgCzzDgFyGLTd_TX2Wn694GrTYj_rQ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWndaMrC7jCK8pQ3JIVbkC45NHD95QNSK5c1K2cS0BNWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNS0-7So.pSoMXS7tt; _T_WM=43654619978; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4670189054467222%26luicode%3D20000061%26lfid%3D4670189054467222'
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
                wb.save(r"D:\weibo\weibo_8月\weibo_08_31\充个电把爸爸吓到了_result_1.xlsx")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    df = pd.read_excel(r'D:\weibo\weibo_8月\weibo_08_31\url.xlsx')
    urls = df['文章链接']
    for url in urls:
        w_id = url.split("/")[-1]
        for i in range(20):
            url = f"https://weibo.cn/comment/{w_id}?&rl=0&page={i + 1}"
            get_comment(url)
            time.sleep(2)

