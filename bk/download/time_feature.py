import pandas as pd
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

from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
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
# 假设您已经加载了包含日期和股价的DataFrame：stock_df
# 假设股价列的名称为 'close'
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

# 特征工程和数据准备
# TODO: 根据需要进行特征提取、数据清洗和预处理等操作
stock_df,mean,std  = get_feature()
# 提取最近20天的行情数据
recent_data = stock_df[-N:]

# 特征选择，这里假设使用 'close' 列作为特征
features = recent_data['close'].values.reshape(-1, 1)

# 标签选择，假设使用下一天的股价作为标签
labels = stock_df['close'].shift(-1)[-N:].values.reshape(-1, 1)

# 数据标准化
scaler = MinMaxScaler()
scaled_features = scaler.fit_transform(features)
scaled_labels = scaler.transform(labels)

# 拆分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(scaled_features, scaled_labels, test_size=0.2, shuffle=False)

# 模型训练
model = LinearRegression()
model.fit(X_train, y_train)

# 进行预测
y_pred = model.predict(X_test)

# 反向标准化预测结果
predicted_prices = scaler.inverse_transform(y_pred)

# 创建包含日期和预测结果的DataFrame
predicted_df = pd.DataFrame({'Date': recent_data.index[-len(predicted_prices):], 'Predicted Price': predicted_prices})

# 将日期列设置为索引列
predicted_df.set_index('Date', inplace=True)

# 打印预测结果
print("预测结果:")
print(predicted_df)