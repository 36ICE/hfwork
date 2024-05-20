
'''
特征数据

预测未来三天股票的高低点、止盈止损点，得到一个分数。
遍历热门股，得到分数最大的TopN 买入，买入点在哪???

'''

# 导入所需的库
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # 使用TkAgg后端

import matplotlib.pyplot as plt

header_mapping = {
    '日期': 'datetime',
    '开盘': 'open',
    '收盘': 'close',
    '最高': 'high',
    '最低': 'low',
    '成交量': 'volume',
    "成交额": "amount",
    "振幅": "amplitude",
    "涨跌幅": "change_pct",
    "涨跌额": "change_amt",
    "换手率": "turnover",
}
N=1

def get_feature():
    # 使用akshare获取A股历史行情数据
    stock_df = ak.stock_zh_a_hist(symbol="600000", period="daily", start_date="20200101", end_date="20240518")
    stock_df = stock_df.rename(columns=header_mapping)
    stock_df.set_index("datetime", inplace=True)
    # 构造目标特征
    stock_df["target"] = stock_df["close"].shift(-N)  # 将未来三天的收盘价作为目标特征，使用shift函数向上平移三行

    # 去除包含缺失值的行
    stock_df = stock_df.dropna()

    # 选择特定的列作为特征
    selected_features = stock_df[["open", "close", "high", "low", "volume","target"]]

    # 处理缺失值
    selected_features = selected_features.dropna()


    # 特征标准化
    mean =selected_features.mean()
    std = selected_features.std()
    selected_features = (selected_features - mean) / std

      # 创建一个新的 DataFrame，将特征和目标列进行合并
    # merged_data = pd.concat([selected_features, stock_df], axis=1)
    return selected_features,mean ,std
    pass
# 定义逆标准化函数
def inverse_normalize(data, mean, std):
    return (data * std) + mean
# 加载数据集
# data = pd.read_csv("your_dataset.csv")

# 特征工程和数据准备
# TODO: 根据需要进行特征提取、数据清洗和预处理等操作
data,mean,std  = get_feature()

# 划分训练集和测试集
X = data[["open", "close", "high", "low", "volume"]]  # 选择特征列
Y = data["target"]  # 目标列
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# 训练模型
model = LinearRegression()
model.fit(X_train, y_train)

# 在测试集上进行预测
y_pred = model.predict(X_test)

# 评估模型性能
mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)

# 使用训练好的模型预测未来三天的高低点
# TODO: 根据具体情况获取未来三天的特征数据，并进行预测
# 根据具体情况获取未来三天的特征数据（示例中使用最后三行数据）
future_features = X.tail(3)

# 使用训练好的模型预测未来三天的目标特征
future_pred = model.predict(future_features)
# 使用逆标准化函数恢复到原始股价范围
future_pred = [inverse_normalize(normalized_pred, mean['close'], std['close']) for normalized_pred in future_pred]
# 创建包含日期和预测结果的DataFrame
predicted_df = pd.DataFrame({'datetime': X_test.index[-len(future_pred):], 'close': future_pred})

# 将日期列设置为索引列
predicted_df.set_index('datetime', inplace=True)

# 打印未来三天的预测结果
print("未来三天的预测结果:", predicted_df)

# 将日期作为索引列
# X.set_index('datetime', inplace=True)

# 绘制实际收盘价和预测收盘价曲线
plt.figure(figsize=(12, 6))
plt.plot(X_test.index, X_test['close'], label='Actual Close Price')
# plt.plot(X.index[-len(y_pred):], y_pred, label='Predicted Close Price')
plt.plot(X_test.index, y_pred, label='Predicted Close Price')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.title('Actual vs Predicted Close Price')
plt.legend()
plt.xticks(rotation=45)
plt.show()


# 制定止盈止损策略
# TODO: 根据预测结果和其他条件，制定止盈和止损策略

# 编写代码实现止盈止损模型
# TODO: 根据具体策略和规则编写代码实现止盈止损模型