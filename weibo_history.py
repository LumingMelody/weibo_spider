import datetime
import time
from concurrent.futures import ThreadPoolExecutor

import pytz
import requests
import pandas as pd
from boost_py.helpers.core.datetime_helper import DateTimeHelper
from openpyxl import Workbook
import re

from pytz import utc

from wb_spider import format_weibo_posttime

wb = Workbook()
ws = wb.active
# ws.append([
#     "用户名",
#     "文章链接",
#     "文章ID",
#     "转发",
#     "赞",
#     "评论",
#     "文章内容",
#     "发布时间",
#     "互动量",
# ])
ws.append(['用户名', '文章链接', '转', '赞', '评', '文章创建时间', '是否为置顶'])

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

cookie = "SINAGLOBAL=6527234529095.878.1632706024442; UOR=,,www.google.com.hk; SUB=_2A25Mc9rbDeRhGeNL61cZ8irPzDuIHXVvn-aTrDV8PUJbkNAKLWbNkW1NSOu9u3awWlaWQNVq8z7GNkaGzOBJb8V-; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWkQeOeXIa3Un.6dwp7CaYw5NHD95QfSK5f1hzXe0MNWs4Dqcjqi--RiK.XiKy2i--4i-zRi-20-c8uUPiy; _s_tentry=-; Apache=2013801656523.3574.1641542345405; ULV=1641542345529:7:1:1:2013801656523.3574.1641542345405:1640054077977; XSRF-TOKEN=ItGQFexDDaald-SS1u3L3gZp; WBPSESS=784AcvWHjyhSLTMYqaBB2R0muMjGEdz8u8017ujja8B-rRUzTBnm7gsagnfGgQRZqAAPc9f3-TXGkFGbfKm478XEosJzwDoBV5GBAZuku_k1OwQMzavkowPBrCMDxpCv0MIo14MuCScxYmOEOKZ21w=="
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


def weibo_his(uid, article_start_time ,article_stop_time, page):
    # all_interact_count = 0
    article_time = ""
    num = 0
    note_url = ""
    # try:
    history_url = f'https://m.weibo.cn/api/container/getIndex?containerid=230413{uid}_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page={page}'
    print(history_url)
    # reposts_count = 0
    # user_name = ""
    # attitudes_count = 0
    # comments_count = 0
    rsp = requests.get(headers=headers, url=history_url).json()
    print(rsp)
    # if rsp['data']['cardlistInfo']['page'] is not None:
    # print(rsp)
    cards_info = rsp["data"]["cards"]
    # print(cards_info)
    for cards in cards_info:
        # print(cards)
        if "mblog" in cards.keys():
            print(cards)
            num += 1
            if "isTop" in cards['mblog'].keys():
                is_Top = 1
                print("此条为置顶")
            else:
                is_Top = 0
            # print(num)
            # if num > 15:
            #     break
            # 转发
            reposts_count = cards["mblog"]["reposts_count"]
            # 赞
            attitudes_count = cards["mblog"]["attitudes_count"]
            # 评论
            comments_count = cards["mblog"]["comments_count"]
            # 文章内容
            content = re.sub(r'<.*?>', '', cards["mblog"]["text"])
            # 用户名
            user_name = cards["mblog"]["user"]["screen_name"]
            # 互动量
            # all_interact_count = int(reposts_count) + int(attitudes_count) + int(comments_count)
            # reposts_count += reposts_count
            # attitudes_count += attitudes_count
            # comments_count += comments_count
            # all_interact_count += all_interact_count
            # content = re.sub(r'<.*?>', '', content)
            # 文章标识ID
            n_id = cards["mblog"]["id"]
            note_url = cards["scheme"]
            # 文章创建时间
            create_time = format_weibo_posttime(cards['mblog']["created_at"]).replace("+0800", "")
            # print(create_time)
            article_time = datetime.datetime.strptime(create_time, "%a %b %d %H:%M:%S %Y")
            # print(article_time)
            # print(type(article_start_time))
            n_article_start_time = datetime.datetime.strptime(str(article_start_time), '%Y-%m-%d %H:%M:%S')
            n_article_stop_time = datetime.datetime.strptime(str(article_stop_time), '%Y-%m-%d %H:%M:%S')
            if n_article_start_time <= article_time <= n_article_stop_time:

            # ws.append(
            #     [user_name, note_url, n_id, reposts_count, attitudes_count, comments_count, content, article_time])
            # while cards['mblog']['page_info'] is not None:
            #     num += 1
            #     print(num, "*" * 20)
            # if num >= 15:
            #     print("退出循环")
            #     break
                ws.append([user_name, note_url, reposts_count, attitudes_count, comments_count, article_time, is_Top])
        time.sleep(2)
    # except Exception as e:
    #     print(e)
    wb.save(r"D:\weibo\weibo22__1月\weibo_01_07\weibo_UNI星球_his.xlsx")


if __name__ == '__main__':
    # url = "https://m.weibo.cn/api/container/getIndex?uid=5675449379&containerid=1076035675449379"
    # wei_bo_content(url)
    # df = pd.read_excel(r"D:\weibo\weibo_7月\weibo_07_20\长安汽车.xlsx")
    article_start_time = '2021-01-01 00:00:00'
    article_stop_time = '2021-12-30 11:59:59'
    # urls = df["主页链接"]
    with ThreadPoolExecutor(40) as t:
        page = 0
        for i in range(0, 150):
            # print(page)
            # history_url = ""
            # for url in urls:
            # if "https://weibo.com/u/" in url:
            # containerid = '107603' + uid
            # uid = url.split("/")[-1]
            uid = "7396009734"
            # # api_url = "https://m.weibo.cn/api/container/getIndex?uid={}&containerid={}".format(uid, containerid)
            # weibo_his(uid=uid, article_start_time=article_start_time, article_stop_time=article_stop_time, page=page)
            t.submit(weibo_his, uid=uid, article_start_time=article_start_time, article_stop_time=article_stop_time,
                     page=page)
            page += 1
