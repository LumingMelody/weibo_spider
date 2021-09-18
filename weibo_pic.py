import random
from concurrent.futures import ThreadPoolExecutor

import requests
import pandas as pd

path2 = r"E:\weibo\weibo_pic_0629"


def get_pic(p_url):
    response = requests.get(p_url, timeout=10)
    return response


if __name__ == '__main__':
    df = pd.read_excel("D:/weibo/weibo_06_24/weibo_pic_urls_06_29.xlsx")
    # pool = ThreadPoolExecutor(max_workers=80)
    urls = df['图片链接']
    # i = 0
    for url in urls:
        ty_pe = url.split("=")[-1]
        pic_name = random.randint(0, 1000)
        # resp = pool.submit(get_pic, url)
        resp = requests.get(url, timeout=10)
        with open(path2 + './' + str(pic_name) + "." + ty_pe, "wb") as fd:
            for chunk in resp.iter_content():
                fd.write(chunk)
