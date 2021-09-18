import time

import requests
import pandas as pd
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.append([
    '用户名',
    '粉丝数',
    '用户认证信息'
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


def get_weibo_user(w_url):
    try:
        resp = requests.get(url=w_url, headers=headers).json()
        user_info = resp['data']['user']
        print(user_info)
        user_name = user_info['screen_name']
        user_desc = user_info['description']
        user_fans = user_info['followers_count']
        if 'verified_reason' in user_info.keys():
            user_verified = user_info['verified_reason']
        else:
            user_verified = ""
        user_desc_verified = str(user_desc) + str(user_verified)
        ws.append([user_name, user_fans, user_desc_verified])
    except Exception as e:
        print(e)
    wb.save(r"D:\weibo\weibo_7月\weibo_07_01\补缺result.xlsx")


if __name__ == '__main__':
    df = pd.read_excel(r"D:\weibo\weibo_7月\weibo_07_01\补缺.xlsx")
    urls = df['主页链接']
    for url in urls:
        u_id = url.split("/")[-1]
        u_url = f"https://weibo.com/ajax/profile/info?custom={u_id}"
        get_weibo_user(u_url)
        time.sleep(3)
