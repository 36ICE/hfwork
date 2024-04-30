import pandas as pd

from bk.data.mysql.mysql_utils import MySQLToolbox


def calculate_sar(high, low, acceleration=0.02, maximum=0.2):
    af = acceleration  # 加速因子
    max_af = maximum  # 最大加速因子

    sar = [0] * len(high)  # 初始化 SAR 列表
    trend = [0] * len(high)  # 初始化趋势列表
    ep = high[0]  # 极点初始值

    for i in range(2, len(high)):
        if trend[i - 1] == 1:
            if low[i] < ep:
                ep = low[i]
                af = min(af + acceleration, max_af)
            sar[i] = sar[i - 1] + af * (ep - sar[i - 1])
            if high[i] > high[i - 1]:
                trend[i] = 1
            else:
                trend[i] = -1
        else:
            if high[i] > ep:
                ep = high[i]
                af = min(af + acceleration, max_af)
            sar[i] = sar[i - 1] + af * (ep - sar[i - 1])
            if low[i] < low[i - 1]:
                trend[i] = -1
            else:
                trend[i] = 1

    return pd.Series(sar, index=high.index)


'''
SAR指标
'''
toolbox = MySQLToolbox(host='localhost', username='root', password='123456', port=33060, database='hf')
toolbox.connect()
data = toolbox.query_builder("raw_a_day_hist") \
    .select("*") \
    .where("code = '000001'") \
    .order_by("ri_qi", ascending=True) \
    .execute()
sar = calculate_sar(data['zui_gao'], data['zui_di'])

print(sar)
toolbox.disconnect()
