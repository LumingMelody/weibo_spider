#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@version: 1.0
@author: adair
@contact: adair.ma@amdigital.cn
@time: 2020/11/19 11:26
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from datetime import timedelta
import datetime
import requests
import pandas as pd
import time
import json
import re
import traceback
from openpyxl import Workbook

from boost_py.helpers.core.datetime_helper import DateTimeHelper


def format_weibo_posttime(date):
    """

    :param date:
    :return:
    """
    if re.match('刚刚', date):
        date = DateTimeHelper.format_datetime(int(time.time()))
    elif re.match('\d+秒', date):
        second = re.match('(\d+)', date).group(1)
        second = timedelta(seconds=int(second))
        date = (datetime.now() - second).strftime('%Y-%m-%d %H:%M:%S')
    elif re.match('\d+分钟前', date):
        minute = re.match('(\d+)', date).group(1)
        date = DateTimeHelper.format_datetime(int(time.time()) - 60 * int(minute))
    elif re.match('\d+小时前', date):
        hour = re.match('(\d+)', date).group(1)
        date = DateTimeHelper.format_datetime(int(time.time()) - 60 * 60 * int(hour))
    elif re.match('昨天.*', date):
        date = re.match('昨天(.*)', date).group(1).strip()
        date = DateTimeHelper.format_datetime(int(time.time()) - 24 * 60 * 60, '%Y-%m-%d') + ' ' + date + ":00"
    elif re.match('今天.*', date):
        date = re.match('今天(.*)', date).group(1).strip()
        date = DateTimeHelper.format_datetime(int(time.time()), '%Y-%m-%d') + ' ' + date + ":00"
    elif re.match('\d{1,2}-\d{1,2}', date):
        date = time.strftime('%Y-', time.localtime()) + date + ' 00:00:00'
        date = DateTimeHelper.format_datetime(DateTimeHelper.parse_formatted_datetime(date, '%Y-%m-%d %H:%M:%S'))
    elif re.match('\d{4}-\d{1,2}-\d{1,2}', date):
        date = date.split(' ')[0] + ' 00:00:00'
        date = DateTimeHelper.format_datetime(DateTimeHelper.parse_formatted_datetime(date, '%Y-%m-%d %H:%M:%S'))
    elif re.match('\d{1,2}月\d{1,2}日', date):
        date = time.strftime('%Y-', time.localtime()) + date.replace('月', '-').replace('日', '') + ' 00:00:00'
        date = DateTimeHelper.format_datetime(DateTimeHelper.parse_formatted_datetime(date, '%Y-%m-%d %H:%M:%S'))
    elif re.match('\d{4}年\d{1,2}月\d{1,2}日', date):
        date = date.split(' ')[0].replace('年', '-').replace('月', '-').replace('日', '') + ' 00:00:00'
        date = DateTimeHelper.format_datetime(DateTimeHelper.parse_formatted_datetime(date, '%Y-%m-%d %H:%M:%S'))
    return date


# def get_zhi_liu_ip():
#     # 代理隧道验证信息
#     url = "http://api.zhuzhaiip.com:498/GetIpPort?passageId=1340905649676349441&num=1&protocol=2&province=&city" \
#           "=&minute=1&format=2&split=&splitChar=&reset=true&secret=8PQhgV"
#     resp = requests.get(url)
#     print(f"获取到代理：{resp.text}")
#     resp = resp.json()
#     ip = resp["data"][0]["ip"]
#     port = resp["data"][0]["port"]
#     meta = "http://%(host)s:%(port)s" % {
#         "host": ip,
#         "port": port,
#     }
#     proxies = {
#         "http": meta,
#         "https": meta
#     }
#     return proxies

def get_yuanrenyun_ip():
    # 代理隧道验证信息
    # url = "http://http.tiqu.letecs.com/getip3?num=1&type=2&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=2&regions=&gm=4"
    url = "http://tunnel-api.apeyun.com/h?id=2021040800226731834&secret=pA7prxttyuCTFjwM&limit=1&format=json&auth_mode=hand"
    resp = requests.get(url).json()
    print(resp)
    ip = resp["data"][0]["ip"]
    port = resp["data"][0]["port"]
    meta = "https://%(host)s:%(port)s" % {
        "host": ip,
        "port": port,
    }
    proxies = {
        "http": meta,
        "https": meta
    }
    # proxies = meta
    # print(proxies)
    return proxies


df = pd.read_excel(r"D:\weibo\weibo_7月\weibo_07_20\长安汽车.xlsx")
urls = df["主页链接"]
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
}
header_com = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
    'Cookie': "SINAGLOBAL=8200568277792.315.1616569676918; _ga=GA1.2.61589090.1616644667; UOR=,,www.baidu.com; SCF=ArJTlx5JAmfMMKsVG7OAs2l4yApmQVJhD9qWf4GqsANvVCKhHes_KjKPtdCz107K0H680Lz53yxK7QO7GERc0r8.; SUB=_2A25NuorLDeRhGeNL61cZ8irPzDuIHXVusfsDrDV8PUNbmtB-LVf_kW9NSOu9uzQPkbBOQAYbBctA2ww9La3uln7R; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWkQeOeXIa3Un.6dwp7CaYw5JpX5KMhUgL.Fo-feh-ReoB0S0M2dJLoIpnLxKnL1KBL12BLxK.LBonLBKSKqg_fMJ2t; ALF=1654664730; SSOLoginState=1623128731; wvr=6; wb_view_log_5505824377=1920*10801; _s_tentry=www.baidu.com; Apache=4530702248365.112.1623140310442; ULV=1623140310497:17:1:1:4530702248365.112.1623140310442:1621319928619; webim_unReadCount=%7B%22time%22%3A1623140312569%2C%22dm_pub_total%22%3A1%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A41%2C%22msgbox%22%3A0%7D"
}
PROXY = {}
wb = Workbook()
ws = wb.active
# ws.append(["用户名", "粉丝", "文章链接", "发布时间", "认证", "15条点赞量", "15条转发量", "15条评论量", "15条平均互动量", "统计文章数", "标签"])
ws.append(["用户名", "粉丝", "文章链接", "发布时间", "认证", "点赞量", "转发量", "评论量"])


def get_weibo_his(urls):
    for url in urls:
        page_size = 0
        print(url)
        uid = str(url).split('?')[0].split('/')[-1]
        datatop = {}
        topic = ''
        page = 78
        num = 0
        all_interact_count = 0
        all_like_count = 0
        all_repost_count = 0
        all_comment_count = 0
        repost_count = 0
        like_count = 0
        comment_count = 0

        data = {}
        post_time = ''
        username = ""
        note_url = ""
        verified_reason = "无"
        fans = ""
        try:
            history_url = 'https://m.weibo.cn/api/container/getIndex?containerid=230413{uid}_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page={page}'
            data = requests.get(history_url.format(uid=uid, page=page), headers=HEADERS, timeout=2).json()
            print(data)
            for p in range(1, 80):
                page_num = p
                for i in data['data']['cards']:
                    if 'mblog' not in i.keys():
                        continue
                    if "isTop" in i['mblog'].keys() and i["mblog"]["isTop"] == 1:
                        continue
                    post_time = format_weibo_posttime(i['mblog']["created_at"])
                    # 文章创建时间
                    create_time = format_weibo_posttime(post_time).replace("+0800", "")
                    # print(create_time)
                    article_time = datetime.datetime.strptime(create_time, "%a %b %d %H:%M:%S %Y")
                    n_article_start_time = datetime.datetime.strptime(str('2021-01-01 00:00:00'), '%Y-%m-%d %H:%M:%S')
                    n_article_stop_time = datetime.datetime.strptime(str('2021-07-20 16:22:00'), '%Y-%m-%d %H:%M:%S')
                    if article_time < n_article_start_time or article_time > n_article_stop_time:
                        break
                    # print(type(post_time))
                    if '万' in str(i['mblog']['reposts_count']):  # 百万转发
                        repost_count = int(re.findall(r'(\d+)', i['mblog']['reposts_count'])[0]) * 10000
                    else:
                        repost_count = i['mblog']['reposts_count']  # 转发
                    if '万' in str(i['mblog']['comments_count']):  # 百万评论
                        comment_count = int(re.findall(r'(\d+)', i['mblog']['comments_count'])[0]) * 10000
                    else:
                        comment_count = i['mblog']['comments_count']  # 评论
                    if '万' in str(i['mblog']['attitudes_count']):  # 百万点赞
                        like_count = int(re.findall(r'(\d+)', i['mblog']['attitudes_count'])[0]) * 10000
                    else:
                        like_count = i['mblog']['attitudes_count']  # 点赞
                    if 'obj_ext' in i['mblog'].keys():  # 2：视频，1：转发，0：直发
                        article_type = '视频'
                    else:
                        article_type = '转发' if 'repost_type' in i['mblog'].keys() else '直发'  # 1：转发，0：直发
                    # if article_type != "直发":
                    #     print(article_type)
                    #     continue
                    print(article_type, post_time)
                    username = i["mblog"]["user"]["screen_name"]
                    fans = i["mblog"]["user"]["followers_count"]
                    mid = i["mblog"]['mid']
                    note_url = f"https://m.weibo.cn/detail/{mid}"
                    print([username, fans, verified_reason, like_count, repost_count, comment_count])
                    ws.append([username, fans, note_url, article_time, verified_reason, like_count, repost_count,
                               comment_count])
                data = requests.get(history_url.format(uid=uid, page=page_num), headers=HEADERS, timeout=2).json()
                print(page_num)
                time.sleep(2.5)
                wb.save(r"D:\weibo\weibo_7月\weibo_07_20\weibo_长安汽车_his_1.xlsx")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    pool = ThreadPoolExecutor(max_workers=10)
    pool.submit(get_weibo_his, urls)
    pool.shutdown(wait=True)
