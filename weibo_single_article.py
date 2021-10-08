#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@version: 1.0
@author: adair
@contact: adair.ma@amdigital.cn
@time: 2020/11/16 16:59
"""
import time
import re
import requests
import json

from openpyxl import Workbook
import pandas as pd
from boost_py.helpers.core.datetime_helper import DateTimeHelper

wb = Workbook()
ws = wb.active
ws.append(["发布链接", "粉丝数", "转", "评", "赞", "15天互动量", "是否为视频", "播放量", "V", "发布时间"])
df = pd.read_excel(r"D:\red_book\red_book_51wom\red_book_10月\red_book_10_08\【1008】闲鱼校园圈跑数据.xlsx")
print(df.columns)
urls = df["发布链接"]

for index, url in enumerate(urls):
    url = url.replace("http://", "https://").replace(" ", "").replace(" ", "")
    if "weibo.com" in url:
        headers = {
            'authority': 'weibo.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'SINAGLOBAL=8200568277792.315.1616569676918; _ga=GA1.2.61589090.1616644667; SUB=_2A25NYpTNDeRhGeNL61cZ8irPzDuIHXVurDyFrDV8PUJbkNAKLVLgkW1NSOu9u1cnRflVimoNEv_cURkWH9ob_aXT; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWkQeOeXIa3Un.6dwp7CaYw5NHD95QfSK5f1hzXe0MNWs4Dqcjqi--RiK.XiKy2i--4i-zRi-20-c8uUPiy; UOR=,,www.baidu.com; _s_tentry=-; Apache=5521507069516.416.1618805829401; ULV=1618805829438:5:2:1:5521507069516.416.1618805829401:1617349429696; wb_view_log_5505824377=1920*10801; webim_unReadCount=%7B%22time%22%3A1618806523453%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A5%2C%22msgbox%22%3A0%7D',
        }
        try:
            response = requests.get(url, headers=headers)
            text = response.content.decode()
            # print(text)
        except:
            ws.append([url, 0, 0, 0, 0, 0, 0])
            wb.save("./data/weibo_0927单文章采集.xlsx")
            continue
        forward = re.findall(
            r'<span class=\\"pos\\"><span class=\\"line S_line1\\" node-type=\\"forward_btn_text\\"><span><em class=\\"W_ficon ficon_forward S_ficon\\">.*?<\\/em><em>(.*?)<\\/em><\\/span><\\/span><\\/span><\\/a>',
            text, re.S)
        comment = re.findall(
            r'<span class=\\"pos\\"><span class=\\"line S_line1\\" node-type=\\"comment_btn_text\\"><span><em class=\\"W_ficon ficon_repeat S_ficon\\">.*?<\\/em><em>(.*?)<\\/em><\\/span><\\/span><\\/span><\\/a>',
            text, re.S)
        like = re.findall(
            r'<span node-type=\\"like_status\\" class=\\"\\"><em class=\\"W_ficon ficon_praised S_txt2\\">.*?<\\/em><em>(.*?)<\\/em><\\/span>',
            text, re.S)
        fans = re.findall(r'<span class="W_f12">(.*?)</span>', text, re.S)
        if len(like) == 2:
            like = like[1:]
        video = "否"
        play_ = re.findall(r'&play_count=(.*?)&duration=', text, re.S)
        if play_:
            video = "是"
            play_count = play_[0]
        else:
            play_count = 0

        verify = re.findall(
            r'suda-uatrack=\\"key=noload_singlepage&value=user_name\\">.*?<\\/a> <a target=\\"_blank\\" href=\\"\\/\\/verified\.weibo\.com\\/verify\\"><i title= \\".*?\\" class=\\"(.*?)\\"><\\/i>',
            text, re.S)
        if verify:
            verify_ = verify[0]
            if verify_ == "W_icon icon_approve_gold":
                level = "红V"
            elif verify_ == "W_icon icon_approve":
                level = "黄V"
            else:
                level = "未认证"
        else:
            verify = re.findall(
                r'suda-uatrack=\\"key=noload_singlepage&value=user_name\\">.*?<\\/a> <a target=\\"_blank\\" href=\\"\\/\\/fuwu\.biz\.weibo\.com\\"><i title= \\".*?\\" class=\\"(.*?)\\"><\\/i>',
                text,
                re.S)
            if verify:
                verify_ = verify[0]
                level = "蓝V"
            else:
                verify_ = ""
                level = "未认证"
        try:
            if forward[0] == "转发":
                forward_count = 0
            else:
                forward_count = forward[0]
        except:
            ws.append([url, 0, 0, 0, 0, 0, 0])
            wb.save("./data/单文章采集.xlsx")
            continue

        if comment[0] == "评论":
            comment_count = 0
        else:
            comment_count = comment[0]

        if like[0] == "赞":
            like_count = 0
        else:
            like_count = like[0]
        all_interact_count = int(forward_count) + int(comment_count) + int(like_count)
        print(forward, comment, like, video, play_count, verify_, level)
        ws.append([url, str(fans), forward_count, comment_count, like_count, round(all_interact_count / 15, 2), video, play_count, level])
        wb.save("./data/weibo_0927单文章采集1.xlsx")
    else:
        mweibo_cn_url = url
        headers = {
            "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
        }
        resp = requests.get(mweibo_cn_url, headers=headers)
        content = resp.content.decode()
        try:
            render_data = re.findall(r'\$render_data = \[(.*?)\]\[0\]', content, re.S)[0].replace("\n", "").replace(" ",
                                                                                                                    "")
        except IndexError:
            ws.append(
                [url, 0, 0, 0,
                 0,
                 0, 0])
            continue
        json_data = json.loads(render_data)
        print(json_data)
        print(json_data["status"])
        user = json_data["status"]["user"]
        fans_count = user["followers_count"]
        attention_count = user["follow_count"]
        post_count = user["statuses_count"]

        verify = user["verified_type"]
        if verify == -1:
            level = "未认证"
        elif verify == 0:
            if user["verified_type_ext"] == 0:
                level = "黄V"
            elif user["verified_type_ext"] == 1:
                level = "红V"
            else:
                level = "未知"
        elif verify == 3:
            level = "蓝V"
        else:
            level = "未认证"
        print(json_data)
        article_reposts_count = json_data["status"]["reposts_count"]
        article_comments_count = json_data["status"]["comments_count"]
        article_attitudes_count = json_data["status"]["attitudes_count"]
        article_post_time = json_data["status"]["created_at"]
        all_interact_count = int(article_reposts_count) + int(article_comments_count) + int(article_attitudes_count)
        try:
            is_video = json_data["status"]["page_info"]["type"]
            if is_video == "video":
                video = "是"
                play_count = json_data["status"]["page_info"]["play_count"]
            else:
                video = "否"
                play_count = 0
        except:
            video = "否"
            play_count = 0
        # Wed Nov 04 10:42:22 +0800 2020

        article_post_format_time = DateTimeHelper.format_datetime(
            DateTimeHelper.parse_formatted_datetime(article_post_time, "%a%b%d%H:%M:%S+0800%Y"))
        ws.append(
            [url, fans_count, article_reposts_count, article_comments_count, article_attitudes_count,  str((all_interact_count / 15, 2)),
             video,
             play_count, level, article_post_format_time])
        wb.save("./data/weibo_0927单文章采集.xlsx")
    print("=" * 100)
