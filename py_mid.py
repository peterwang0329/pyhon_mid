import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, DayLocator

url = 'https://rate.bot.com.tw/xrt/quote/ltm/USD'
#payload = {'key1':'value1','key2':'value2'}
#r = requests.get("網址",params=payload)
html = requests.get(url)
html.encoding = 'UTF-8'
sp = BeautifulSoup(html.text,'lxml')
print(sp.title.text)
datas = sp.find_all('td',class_ = "rate-content-cash text-right print_table-cell")
dates = sp.find_all('td',class_ = "text-center")

# 创建字典，存储日期和卖出价格
exchange_rates = {"日期":[],"買入":[],"賣出":[]}

# 将日期和卖出价格存入字典
for i in range(1, len(datas), 2):
    date = dates[i - 1].text
    sell_rate_buy = datas[i - 1].text
    sell_rate_sell = datas[i].text
    exchange_rates["日期"].append(date)
    exchange_rates["買入"].append(sell_rate_buy)
    exchange_rates["賣出"].append(sell_rate_sell)

# 打印字典
out = pd.DataFrame(exchange_rates)

out['日期'] = pd.to_datetime(out['日期'])
plt.rcParams["font.sans-serif"] = "Microsoft JhengHei"
plt.rcParams["axes.unicode_minus"] = False
plt.figure(figsize=(10, 5))
plt.plot(out['日期'], out['買入'], label='買入', marker='o', color='red')
plt.plot(out['日期'], out['賣出'], label='賣出', marker='o', color='blue')

# 设置横轴和纵轴的标签
plt.xlabel('日期')
plt.ylabel('價格')
plt.title('買入與賣出價格比較')

# 设置纵轴范围和间隔
plt.ylim(31, 33)
plt.yticks([0 + i * 25 for i in range(9)])  # 31 到 33 之间以 0.25 为间隔

# 设置横轴的日期格式和间隔为 5 天
plt.gca().xaxis.set_major_locator(DayLocator(interval=5))
plt.gca().xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
plt.xticks(rotation=45)

# 显示图例并调整布局
plt.legend()
plt.tight_layout()
plt.show()
#out.to_excel("./test.xlsx",index=False)

