import re
from openpyxl import Workbook
import requests
import datetime
import time
from pytz import timezone

zone = 'Asia/Shanghai'

cookie = "SINAGLOBAL=6527234529095.878.1632706024442; UOR=,,www.google.com.hk; SUB=_2A25Mc9rbDeRhGeNL61cZ8irPzDuIHXVvn-aTrDV8PUJbkNAKLWbNkW1NSOu9u3awWlaWQNVq8z7GNkaGzOBJb8V-; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWkQeOeXIa3Un.6dwp7CaYw5NHD95QfSK5f1hzXe0MNWs4Dqcjqi--RiK.XiKy2i--4i-zRi-20-c8uUPiy; ULV=1636956919329:5:1:1:7408887662759.944.1636956919236:1635232371340; XSRF-TOKEN=9SKanKqiPEUE9ufGN56KEwZy; WBPSESS=784AcvWHjyhSLTMYqaBB2R0muMjGEdz8u8017ujja8B-rRUzTBnm7gsagnfGgQRZqAAPc9f3-TXGkFGbfKm47wukfx1PdJiN5ePLNz1Gj_On1RSgHVwWOyxU1Og3dA7jwH0fT0Mwxj7SK3wSMvQIJA=="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'cookie': cookie,
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
}
wb = Workbook()
ws = wb.active
ws.append([
    '用户名',
    '粉丝数',
    '转',
    '赞',
    '评',
    '文章内容',
    '文章链接',
    '文章创建时间',
])


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


def get_weibo_keyword(w_url):
    resp = requests.get(w_url, headers=headers).json()
    cards = resp['data']['cards']
    for card in cards:
        # print(card)
        if "mblog" in card.keys():
            # 转
            reposts_count = card["mblog"]["reposts_count"]
            # 赞
            attitudes_count = card["mblog"]["attitudes_count"]
            # 评论
            comments_count = card["mblog"]["comments_count"]
            # 文章内容
            content = re.sub(r'<.*?>', '', card["mblog"]["text"])
            # 用户名
            user_name = card["mblog"]["user"]["screen_name"]
            # 粉丝数
            fans = card["mblog"]["user"]["followers_count"]
            # 文章链接
            article_url = card["scheme"]
            # 文章创建时间
            create_time = format_weibo_posttime(card['mblog']["created_at"]).replace("+0800", "")
            # print(create_time)
            article_time = datetime.datetime.strptime(create_time, "%a %b %d %H:%M:%S %Y")
            timeArray = time.strptime(str(article_time), "%Y-%m-%d %H:%M:%S")
            timestamp = time.mktime(timeArray)
            # if 1606752000 <= int(timestamp) <= 1617120000:
            if 1609430400 <= int(timestamp):
                print([
                    user_name, fans, reposts_count, attitudes_count, comments_count, content, article_url, article_time
                ])
                ws.append([
                    user_name, fans, reposts_count, attitudes_count, comments_count, content, article_url, article_time
                ])
        wb.save(path)


if __name__ == '__main__':

    # keyword_list = ["逐本精华油", "兰精华油", "林清轩山茶花精华油", "PMPM玫瑰红茶精华油", "雏菊的天空翡冷翠精华油"]
    keyword = "逐本精华油"
    # for keyword in keyword_list:
    path = r"D:\weibo\weibo_11月\weibo_11_29\{}.xlsx".format(keyword)
    for i in range(50):
        url = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{keyword}&page_type=searchall&page={i + 1}"
        get_weibo_keyword(url)
        time.sleep(5)