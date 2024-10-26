import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, DayLocator

url = 'https://rate.bot.com.tw/xrt/quote/ltm/USD'
html = requests.get(url)
html.encoding = 'UTF-8'
sp = BeautifulSoup(html.text,'lxml')
print(sp.title.text)
datas = sp.find_all('td',class_ = "rate-content-cash text-right print_table-cell")
dates = sp.find_all('td',class_ = "text-center")

# 創建字典，储存日期和賣出價格
exchange_rates = {"日期":[],"買入":[],"賣出":[]}

# 將日期和賣出價格存入字典
for i in range(1, len(datas), 2):
    date = dates[i - 1].text
    sell_rate_buy = datas[i - 1].text
    sell_rate_sell = datas[i].text
    exchange_rates["日期"].append(date)
    exchange_rates["買入"].append(sell_rate_buy)
    exchange_rates["賣出"].append(sell_rate_sell)

# 放入字典
out = pd.DataFrame(exchange_rates)

out['日期'] = pd.to_datetime(out['日期'])
plt.rcParams["font.sans-serif"] = "Microsoft JhengHei"
plt.rcParams["axes.unicode_minus"] = False
plt.figure(figsize=(10, 5))
plt.plot(out['日期'], out['買入'], label='買入', color='red')
plt.plot(out['日期'], out['賣出'], label='賣出', color='blue')

# 设置橫軸&縱軸標籤
plt.xlabel('日期')
plt.ylabel('價格')
plt.title('買入與賣出價格比較')

# 設定符合匯率的合理縱軸範圍
plt.gca().yaxis.set_major_locator(plt.MultipleLocator(15))

# 设置横轴的日期格式和间隔为 10 天
plt.gca().xaxis.set_major_locator(DayLocator(interval=10))
plt.gca().xaxis.set_major_formatter(DateFormatter("%Y-%m-%d"))
plt.xticks(rotation=45)

# 顯示圖表
plt.legend()
plt.tight_layout()
plt.show()

#輸出成excel格式
#out.to_excel("./test.xlsx",index=False)

