import pandas as pd
import talib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import time

import akshare as ak
def download_day(code):
    # 准备数据
    print("正在下载" + str(code) + "日线数据")
    try:
        stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, period="daily",start_date="20230101",end_date="20500101", adjust="")
        stock_zh_a_hist_df.to_csv("./day/" + str(code) + ".csv")
    except:
        print("下载异常" + str(code) + "....")
        time.sleep(1)
    else:
        print("下载" + str(code) + "日线数据完成")
        time.sleep(0.5)
code='603259'
download_day(code)
data = pd.read_csv(f"./day/{code}.csv")  # 读取历史股价数据，假设数据存储在 stock_data.csv 文件中
data['日期'] = pd.to_datetime(data['日期'])  # 将日期列转换为日期时间类型
data = data.sort_values('日期')  # 按日期升序排列
data = data.reset_index(drop=True)  # 重置索引

for row in data['收盘']:
    if row is None:
        print(row)
# 计算技术指标作为特征
data['SMA'] = talib.SMA(data['收盘'], timeperiod=10)  # 计算10日简单移动平均线
data['EMA'] = talib.EMA(data['收盘'], timeperiod=10)  # 计算10日指数移动平均线
data['RSI'] = talib.RSI(data['收盘'], timeperiod=14)  # 计算14日相对强弱指标

# 准备训练数据
features = data[['SMA', 'EMA', 'RSI']][30:]  # 选择特征列
# last_high=download['最高'][-1:]
# last_low=download['最低'][-1:]

targets = pd.concat([data[['最高', '最低']][31:],pd.DataFrame({'最高': data['最高'][-1:].values, '最低': data['最低'][-1:].values})])
# num=len(targets)-1
# targets.loc[len(targets.index)]=[targets.iloc[num][0],targets.iloc[num][1]]
# targets._append(pd.DataFrame({'最高':[0],'最低':[0]}), ignore_index=True)   # 选择预测目标列

# 划分训练集和测试集
# X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, shuffle=False)

# 创建并训练模型
model = LinearRegression()
model.fit(X_train, y_train)

# 进行预测
predictions = model.predict(X_test)


# 计算准确率 平均误差
# 打印预测结果
print("预测结果：")
low_sum = 0
high_sum = 0
for i in range(len(predictions)):
    print(f"预测最高价: {predictions[i][0]}, 预测最低价: {predictions[i][1]},实际最高价：{y_test.iloc[i][0]},实际最低价：{y_test.iloc[i][1]},")
    high_sum+=predictions[i][0]/y_test.iloc[i][0]-1
    low_sum+=predictions[i][1]/y_test.iloc[i][1]-1

print(f"最小值平均误差：{low_sum/len(predictions)*10000}")
print(f"最大值平均误差：{high_sum/len(predictions)*10000}")
