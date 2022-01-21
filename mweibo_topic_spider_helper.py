#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@version: 1.0
@author: anne
@contact: thy.self@foxmail.com
@time: 2020/3/11 15:47
"""
# UA 需要更改时可以提取dts_prod.uas 随机ua
import random
import re
import time
from urllib.parse import quote

import requests
from openpyxl import Workbook

# from src.commons.weibo_cookies_helper import WeiboCookiesHelper
# from src.models.mysql.dts_prod_models import BoostUserAgent

API_URL = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D{type}%26q%3D{topic}%26t%3D0&page_type=searchall&page={page}'

USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
    "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
    "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
    "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
    "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
    "UCWEB7.0.2.37/28/999",
    "NOKIA5700/ UCWEB7.0.2.37/28/999",
    "Openwave/ UCWEB7.0.2.37/28/999",
    "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
    # iPhone 6：
    # "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
]
headers = {
    'User-Agent': random.choice(USER_AGENTS),
    'cookie': 'SINAGLOBAL=8200568277792.315.1616569676918; _ga=GA1.2.61589090.1616644667; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWkQeOeXIa3Un.6dwp7CaYw5JpX5KMhUgL.Fo-feh-ReoB0S0M2dJLoIpnLxKnL1KBL12BLxK.LBonLBKSKqg_fMJ2t; ALF=1655430343; SSOLoginState=1623894343; SCF=ArJTlx5JAmfMMKsVG7OAs2l4yApmQVJhD9qWf4GqsANvJ-VkjYkICkxHviQgKrfTDEByU-vFCBAdFh1HrVp1imA.; SUB=_2A25NztkYDeRhGeNL61cZ8irPzDuIHXVuuk3QrDV8PUNbmtAKLUzjkW9NSOu9u4zkVFUZ6x-2B5cTuCKzlqClZPvF; _s_tentry=login.sina.com.cn; Apache=6112936826984.548.1623894350767; ULV=1623894350783:23:7:3:6112936826984.548.1623894350767:1623823732287; wb_view_log_5505824377=1920*10801; wvr=6; UOR=,,www.baidu.com; webim_unReadCount=%7B%22time%22%3A1623908063571%2C%22dm_pub_total%22%3A1%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A40%2C%22msgbox%22%3A0%7D'
}

import datetime
import time

from pytz import timezone

zone = 'Asia/Shanghai'


class DateTimeHelper(object):
    """ Datetime helper

    """

    @classmethod
    def is_timestamp(cls, val):
        """ 判断是否是时间戳

        :param val:
        :return:
        """
        try:
            int(val)
            return True
        except ValueError:
            return False

    @classmethod
    def parse_formatted_datetime(cls, formatted_time: str, fmt: str):
        """ 解析已格式化的时间字符串，获得对应的时间戳

        :param formatted_time:
        :param fmt:
        :return:
        """
        return int(time.mktime(time.strptime(formatted_time, fmt)))

    @classmethod
    def format_datetime(cls, timestamp, fmt='%Y-%m-%d %H:%M:%S'):
        """ 获得给定时间戳对应的时间字符串

        :param timestamp: 时间戳
        :param fmt:
        :return:
        """
        if cls.is_timestamp(timestamp):
            return time.strftime(fmt, time.localtime(int(timestamp)))
        else:
            raise ValueError('%s is not timestamp.' % timestamp)

    @classmethod
    def get_china_timezone(cls):
        return timezone(zone)

    @classmethod
    def get_china_timezone_name(cls):
        return zone

    @classmethod
    def get_datetime_info(cls, timestamp):
        """ 获得时间的详细信息

        :param timestamp:
        :return:
        """
        datetime_obj = time.localtime(timestamp)
        return {
            'year': datetime_obj.tm_year,
            'month': datetime_obj.tm_mon,
            'day': datetime_obj.tm_mday,
            'hour': datetime_obj.tm_hour,
            'minute': datetime_obj.tm_min,
            'second': datetime_obj.tm_sec,
            'week_day': datetime_obj.tm_wday,  # 一周的第n天，0表示星期一，6表示星期日
            'year_day': datetime_obj.tm_yday  # 一年的第n天
        }

    @classmethod
    def get_differ_of_two_times(cls, start_timestamp, end_timestamp):
        """ 获得两个时间戳相差（天，小时，分钟，秒）
        :param start_timestamp:
        :param end_timestamp:
        :return:
        """
        if start_timestamp > end_timestamp:
            raise Exception('end_timestamp should greater than start_timestamp')

        start_time = cls.format_datetime(start_timestamp, '%Y-%m-%d-%H-%M-%S')
        end_time = cls.format_datetime(end_timestamp, '%Y-%m-%d-%H-%M-%S')

        diff_year = int(end_time.split('-')[0]) - int(start_time.split('-')[0])
        diff_month = diff_year * 12 + (int(end_time.split('-')[0]) - int(start_time.split('-')[0]))

        diff_minute = int((end_timestamp - start_timestamp) / 60)
        diff_hour = int((end_timestamp - start_timestamp) / 3600)
        diff_day = int((end_timestamp - start_timestamp) / (3600 * 24))

        return {
            'year': diff_year,
            'month': diff_month,
            'day': diff_day,
            'hour': diff_hour,
            'minute': diff_minute,
            'second': int(end_timestamp - start_timestamp)
        }

    @classmethod
    def get_previous_timestamp(cls, timestamp: int, day=None, hour=None):
        """ 获得timestamp的day/hour之前的时间戳

        :param timestamp:
        :param day:
        :param hour:
        :return:
        """
        if not cls.is_timestamp(timestamp):
            raise Exception('timestamp should be int type')

        if day is not None and hour is not None:
            return timestamp - day * 24 * 3600 - hour * 3600
        elif day is not None:
            return timestamp - day * 24 * 3600
        elif hour is not None:
            return timestamp - hour * 3600
        else:
            return timestamp

    @classmethod
    def get_previous_datestamp(cls, timestamp: int, day=None):
        """
        当day为正数时，获得n天前的日期戳；
        当day为空或0时，获得当天的日期戳；
        当day为负数时，获取n天之后的日期戳；

        :param timestamp:
        :param day:
        :return:
        """
        day = day or 0
        if cls.is_timestamp(timestamp):
            t = cls.format_datetime((timestamp - day * 24 * 3600), '%Y-%m-%d %H:%M:%S')[0:10]
            return cls.parse_formatted_datetime(t, '%Y-%m-%d')
        else:
            raise Exception('timestamp should be int type')


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


class MweiboTopicSpiderHelper(object):

    @classmethod
    def spider_topic(cls, spider_type, topic_keyword):
        """

        :param spider_type:
        :param topic_keyword:
        :return:
        """
        type_dict = {
            1: '1',  # 综合
            2: '60',  # 热门
            3: '61',  # 实时
        }
        to_urlcode = lambda x: quote(x)
        # requests忽略warning
        requests.packages.urllib3.disable_warnings()
        ws = Workbook()
        wb = ws.active
        wb.append(['微博内容', '微博链接', '发布时间', '转', '评', '赞', 'V', '用户名', '微博主页', '粉丝数', '性别'])
        for page in range(1, 50):
            url = API_URL.format(type=type_dict[spider_type], topic=to_urlcode(topic_keyword), page=str(page))
            print(url)
            api_resp = requests.get(url, headers=headers, verify=False)
            print(api_resp)
            if api_resp.text[0] == '<':
                continue
            api_json = api_resp.json()
            # pprint(api_json['data']['cards'][0]['mblog'])
            if api_json.get('data') and api_json['data'].get('cards'):
                article_list = api_json['data']['cards']
                if article_list:
                    for i in article_list:
                        if i.get('mblog'):
                            mblog = i['mblog']
                            text = mblog['text']
                            text = re.sub('<.*?>', '', text)
                            article_url = 'http://m.weibo.cn/detail/' + mblog['id']
                            # create_at = mblog['created_at']
                            create_time = format_weibo_posttime(mblog["created_at"]).replace("+0800", "")
                            # print(create_time)
                            article_time = datetime.datetime.strptime(create_time, "%a %b %d %H:%M:%S %Y")
                            reposts_count = mblog['reposts_count']
                            comments_count = mblog['comments_count']
                            attitudes_count = mblog['attitudes_count']
                            user = mblog['user']
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
                            user_name = user['screen_name']
                            user_url = 'http://weibo.com/u/' + str(user['id'])
                            gender = user['gender']
                            if gender == 'f':
                                gender = "女"
                            else:
                                gender = "男"
                            fans_num = user['followers_count']
                            m_list = [text, article_url, article_time, reposts_count, comments_count, attitudes_count,
                                      level,
                                      user_name,
                                      user_url, fans_num, gender]
                            print(m_list)
                            if fans_num.endswith("万"):
                                wb.append(m_list)
                        elif i.get('card_group'):
                            try:
                                mblog = i['card_group'][0]['mblog']
                                text = mblog['text']
                                text = re.sub('<.*?>', '', text)
                                article_url = 'http://m.weibo.cn/detail/' + mblog['id']
                                # create_at = mblog['created_at']
                                create_time = format_weibo_posttime(mblog["created_at"]).replace("+0800", "")
                                # print(create_time)
                                article_time = datetime.datetime.strptime(create_time, "%a %b %d %H:%M:%S %Y")
                                reposts_count = mblog['reposts_count']
                                comments_count = mblog['comments_count']
                                attitudes_count = mblog['attitudes_count']
                                user = mblog['user']
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
                                user_name = user['screen_name']
                                user_url = 'http://weibo.com/u/' + str(user['id'])
                                gender = user['gender']
                                if gender == 'f':
                                    gender = "女"
                                else:
                                    gender = "男"
                                fans_num = user['followers_count']
                                m_list = [text, article_url, article_time, reposts_count, comments_count, attitudes_count,
                                          level,
                                          user_name,

                                          user_url, fans_num, gender]
                                print(m_list)
                                if fans_num.endswith("万"):
                                    wb.append(m_list)
                            except Exception as e:
                                print(e)
            if api_json['ok'] == 0 and api_json["msg"] == "这里还没有内容":
                break
            time.sleep(5)
        ws.save(f'{topic_keyword}.xlsx')

    @classmethod
    def spider_comments(cls, mid):
        """

        :param mid:
        :return:
        """
        ws = Workbook()
        wb = ws.active
        wb.append(['评论内容', '用户名', 'V', '用户主页', '粉丝数'])
        try:
            url = 'https://m.weibo.cn/comments/hotflow?id={id}&mid={id}&max_id_type=0'.format(id=str(mid))
            api_json = requests.get(url, headers=headers, verify=False).json()

            # print(json.dumps(api_json, ensure_ascii=False))
            comment_list = api_json['data']['data']
            next_max_id = api_json['data']['max_id']
            if comment_list:
                for comment in comment_list:
                    text = comment['text']
                    text = re.sub('<.*?>', '', text)
                    user = comment['user']
                    verified_type = user['verified_type']
                    V = '蓝V' if verified_type == 2 else '黄V' if verified_type == 1 or verified_type == 0 else '无'
                    user_name = user['screen_name']
                    user_url = 'http://weibo.com/u/' + str(user['id'])
                    fans_num = user['followers_count']
                    print([text, user_name, V, user_url, fans_num])
                    wb.append([text, user_name, V, user_url, fans_num])
                time.sleep(3)
            num = 0
            while True:
                url = 'https://m.weibo.cn/comments/hotflow?id={id}&mid={id}&max_id={max_id}&max_id_type=0'.format(
                    id=str(mid),
                    max_id=next_max_id)
                print(url)
                api_json = requests.get(url, headers=cls.init_header(), verify=False).json()
                # print(json.dumps(api_json, ensure_ascii=False))
                if not api_json.get('data') or not api_json['data'].get('data'):
                    break
                comment_list = api_json['data']['data']
                next_max_id = api_json['data']['max_id']
                if comment_list:
                    for comment in comment_list:
                        text = comment['text']
                        text = re.sub('<.*?>', '', text)
                        user = comment['user']
                        verified_type = user['verified_type']
                        V = '蓝V' if verified_type == 2 else '黄V' if verified_type == 1 or verified_type == 0 else '无'
                        user_name = user['screen_name']
                        user_url = 'http://weibo.com/u/' + str(user['id'])
                        fans_num = user['followers_count']
                        print([text, user_name, V, user_url, fans_num])
                        wb.append([text, user_name, V, user_url, fans_num])
                    time.sleep(3)
                num += 1
                if num == 49:
                    break
            ws.save(mid + '.xlsx')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    MweiboTopicSpiderHelper.spider_topic(1, '#双11成就#')
    MweiboTopicSpiderHelper.spider_topic(1, '#我的双11回忆#')
    MweiboTopicSpiderHelper.spider_topic(1, '#最破防的表白情歌# ')
    # MweiboTopicSpiderHelper.spider_topic(1, '#手机里走完春节流程#')
    # MweiboTopicSpiderHelper.spider_topic(1, '#爸妈P的团圆照#')
    # MweiboTopicSpiderHelper.spider_topic(1, '#李佳琪#')
    # MweiboTopicSpiderHelper.spider_topic(1, '#投影仪拍新年大片#')
    # 超级买家秀#
