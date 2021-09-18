import datetime

# 原时间是字符串
time1_s = '2020-03-28 08:10:50'
time2 = datetime.datetime.strptime(time1_s, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=8)
print(time1_s, time2.strftime("%Y-%m-%d %H:%M:%S"))

# 原时间是时间类型
time1 = datetime.datetime.now()
time2 = time1 + datetime.timedelta(hours=8)

print(time1.strftime("%Y-%m-%d %H:%M:%S"), time2.strftime("%Y-%m-%d %H:%M:%S"))