import time
import pandas as pd

df = pd.read_excel(r"D:\bilibili\bilibili_07_06\bilibili_PMPM精华油.xlsx")
ts = df['创建时间']
for t in ts:
    timeArray = time.localtime(t)
    otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
    print(otherStyleTime)
