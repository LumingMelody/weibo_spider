import datetime
import time

import pytz
import requests
import pandas as pd
from boost_py.helpers.core.datetime_helper import DateTimeHelper
from openpyxl import Workbook
import re

from pytz import utc

wb = Workbook()
ws = wb.active
ws.append([
    "用户名",
    "文章链接",
    "文章ID",
    "转发",
    "赞",
    "评论",
    "文章内容",
    "发布时间"
])

cookie = "SINAGLOBAL=8200568277792.315.1616569676918; _ga=GA1.2.61589090.1616644667; SUB=_2A25NYpTNDeRhGeNL61cZ8irPzDuIHXVurDyFrDV8PUJbkNAKLVLgkW1NSOu9u1cnRflVimoNEv_cURkWH9ob_aXT; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWkQeOeXIa3Un.6dwp7CaYw5NHD95QfSK5f1hzXe0MNWs4Dqcjqi--RiK.XiKy2i--4i-zRi-20-c8uUPiy; wvr=6; wb_view_log_5505824377=1920*10801; _s_tentry=www.baidu.com; UOR=,,www.baidu.com; Apache=3326332886095.5845.1620796823826; ULV=1620796823837:13:3:3:3326332886095.5845.1620796823826:1620696227066; webim_unReadCount=%7B%22time%22%3A1620796826356%2C%22dm_pub_total%22%3A1%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A40%2C%22msgbox%22%3A0%7D"
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


def format_weibo_posttime(date):
    """
    :param date:
    :return:
    """
    if re.match('刚刚', date):
        date = DateTimeHelper.format_datetime(int(time.time()))
    elif re.match('\d+秒', date):
        second = re.match('(\d+)', date).group(1)
        second = datetime.timedelta(seconds=int(second))
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


def wei_bo_content(url):
    # 获取微博评论和回复
    rsp = requests.get(headers=headers, url=url).json()
    cards_info = rsp["data"]["cards"]
    print(cards_info)
    user_name = ""
    n_create_time = ""
    user_url = ""
    # for cards in cards_info:
    cards = cards_info[1]
    if "mblog" in cards.keys():
        # 转发
        # reposts_count = cards["mblog"]["reposts_count"]
        # # 赞
        # attitudes_count = cards["mblog"]["attitudes_count"]
        # # 评论
        # comments_count = cards["mblog"]["comments_count"]
        # # 文章内容
        # content = re.sub(r'<.*?>', '', cards["mblog"]["text"])
        #
        # # content = re.sub(r'<.*?>', '', content)
        # # 文章标识ID
        # n_id = cards["mblog"]["id"]
        # note_url = cards["scheme"]
        # 文章创建时间
        create_time = cards["mblog"]["created_at"]
        # 格林威治时间转换为标准时间格式
        std_transfer = '%a %b %d %H:%M:%S %z %Y'
        n_create_time = datetime.datetime.strptime(create_time, std_transfer)
        # start_time = n_create_time.replace(tzinfo=pytz.timezone("Asia/Shanghai"))
        # print(start_time)
        # create_time = format_weibo_posttime(cards['mblog']["created_at"])
        # article_time = DateTimeHelper.parse_formatted_datetime(create_time, '%Y-%m-%d %H:%M:%S')
        # last_time = datetime.datetime(2021, 3, 28, tzinfo=pytz.timezone("Asia/Shanghai"))
        # print(last_time)
        # if last_time.__ge__(start_time):
        #     return

        # # print(content, create_time)
        # # 用户名
        user_name = cards["mblog"]["user"]["screen_name"]
        # # 用户ID
        user_id = cards["mblog"]["user"]["id"]
        user_url = f"https://m.weibo.cn/profile/{user_id}"
        # # if cards["mblog"]["user"]["verified_reason"] is not None:
        # #     verified_reason = cards["mblog"]["user"]["verified_reason"]
        # 粉丝数
        # fans = cards["mblog"]["user"]["followers_count"]
        # # 关注数
        # follow = cards["mblog"]["user"]["follow_count"]
        # # 签名
        # desc = cards["mblog"]["user"]["description"]
        # ws.append([
        #     user_id, user_name, fans, follow, desc, content, create_time,
        # ])
    ws.append(
        [user_name, user_url])
    wb.save("D:/weibo/weibo_06_25/weibo_0625.xlsx")


if __name__ == '__main__':
    # url = "https://m.weibo.cn/api/container/getIndex?uid=5675449379&containerid=1076035675449379"
    # wei_bo_content(url)
    df = pd.read_excel(r"D:\weibo\weibo_8月\weibo_08_03\weibo_08_03.xlsx")
    urls = df["链接"]
    for url in urls:
        user_id = url.split("/")[-2]
        user_url = f"https://m.weibo.cn/profile/{user_id}"
        ws.append([user_id, user_url])
    wb.save('D:/weibo/weibo_06_25/weibo_0625.xlsx')
    # for url in urls:
    #     # if "https://weibo.com/u/" in url:
    #     uid = url.split("/")[-2]
    #     print(uid)
    #     containerid = '107603' + uid
    #     api_url = f"https://m.weibo.cn/api/container/getIndex?uid={uid}&containerid={containerid}"
    #     print(api_url)
    #     wei_bo_content(url=api_url)
    #     time.sleep(2)
