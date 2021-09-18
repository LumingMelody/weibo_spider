import time

import requests
import pandas as pd
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.append([
    "粉丝数",
    "评论数",
    "转发数"
])

cookie = "SINAGLOBAL=8200568277792.315.1616569676918; _ga=GA1.2.61589090.1616644667; SUB=_2A25NYpTNDeRhGeNL61cZ8irPzDuIHXVurDyFrDV8PUJbkNAKLVLgkW1NSOu9u1cnRflVimoNEv_cURkWH9ob_aXT; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWkQeOeXIa3Un.6dwp7CaYw5NHD95QfSK5f1hzXe0MNWs4Dqcjqi--RiK.XiKy2i--4i-zRi-20-c8uUPiy; UOR=,,www.baidu.com; _s_tentry=-; Apache=5521507069516.416.1618805829401; ULV=1618805829438:5:2:1:5521507069516.416.1618805829401:1617349429696; wb_view_log_5505824377=1920*10801; webim_unReadCount=%7B%22time%22%3A1618806523453%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A5%2C%22msgbox%22%3A0%7D"
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


def get_weibo(w_url, z_url, p_url):
    p_total_num = ""
    fans = ""
    z_total_num = ""
    rs = requests.get(headers=headers, url=w_url)
    if rs.content:
        rsp = rs.json()
        try:
            if rsp:
                fans = rsp["data"]["user"]["followers_count"]
            p_rsp = requests.get(url=p_url, headers=headers).json()
            if p_rsp:
                p_total_num = p_rsp["data"]["total_number"]
            z_rsp = requests.get(headers=headers, url=z_url).json()
            if z_rsp:
                z_total_num = z_rsp["data"]["total_number"]
        except Exception as e:
            print(e)
    ws.append([fans, p_total_num, z_total_num])
    wb.save("D:/weibo/jinzhuangjiang.xlsx")


if __name__ == '__main__':
    df = pd.read_excel("D:/weibo/weibo_url2.xlsx")
    f_urls = df["发布链接"]
    # print(urls)
    for f_url in f_urls:
        # if "https://weibo.com/u/" in url:
        uid = f_url.split("/")[3]
        nid = f_url.split("/")[-1]
        info_url = "https://m.weibo.cn/profile/info?uid={}".format(uid)
        p_url = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0".format(nid, nid)
        z_url = "https://m.weibo.cn/api/statuses/repostTimeline?id={}&page=1".format(nid)
        # print(info_url)
        get_weibo(info_url, z_url, p_url)
        time.sleep(3)

