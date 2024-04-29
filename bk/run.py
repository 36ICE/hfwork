from bk.config import CURRENT_WORKSPACE_DIRECTORY
from download.ak_downloader import AKDownloader
import backtrader as bt
import pandas as pd
from bk.strategy.MyStrategy_v1 import MyStrategy
from datetime import datetime
import matplotlib.pyplot as plt  # 由于 Backtrader 的问题，此处要求 pip install matplotlib==3.2.

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False


def createCerebro(df, start_cash=1000000, stake=100, commission_fee=0.001):
    start_date = datetime(2021, 4, 3)  # 回测开始时间
    end_date = datetime(2024, 4, 26)  # 回测结束时间
    cerebro = bt.Cerebro()
    # cerebro.optstrategy(MyStrategy, maperiod=range(3, 31))  # 导入策略参数寻优
    cerebro.addstrategy(MyStrategy, maperiod=55, printlog=True)

    data = bt.feeds.PandasData(dataname=df, fromdate=start_date, todate=end_date)
    cerebro.adddata(data)
    # 设置初始化资金
    cerebro.broker.setcash(start_cash)
    cerebro.broker.setcommission(commission=commission_fee)  # 手续费
    # cerebro.addsizer(bt.sizers.FixedSize, stake=stake)  # 设置买入数量
    cerebro.run(maxcpus=1)  # 用单核 CPU 做优化
    port_value = cerebro.broker.getvalue()  # 获取回测结束后的总资金
    pnl = port_value - start_cash  # 盈亏统计

    print(f"初始资金: {start_cash}\n回测期间：{start_date.strftime('%Y%m%d')}:{end_date.strftime('%Y%m%d')}")
    print(f"总资金: {round(port_value, 2)}")
    print(f"净收益: {round(pnl, 2)}")
    cerebro.plot()


def download_data(code="002821", codetype="stock"):
    # 读取数据
    if codetype == 'etf':
        df = AKDownloader.download_etf_day(code)
    else:
        df = AKDownloader.download_stock_day(code)


    return df


def main():
    df = download_data()
    createCerebro(df)


if __name__ == '__main__':
    main()
