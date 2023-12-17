from datetime import datetime

import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt  # 由于 Backtrader 的问题，此处要求 pip install matplotlib==3.2.2
import pandas as pd
import talib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import time

import akshare as ak

plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False


class MyStrategy(bt.Strategy):
    """
    主策略程序
    """
    params = (("maperiod", 20),
              ('printlog', False),)  # 全局设定交易策略的参数, maperiod是 MA 均值的长度

    def log(self, txt, dt=None, do_print=False):
        """
        Logging function fot this strategy
        """
        if self.params.printlog or do_print:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))


    def __init__(self):
        self.data_close = self.datas[0].close  # 指定价格序列
        # 初始化交易指令、买卖价格和手续费
        self.order = None
        self.buy_price = None
        self.buy_comm = None

        # 添加移动均线指标
        self.sma = bt.indicators.SMA(self.datas[0], period=self.params.maperiod)


    def notify_order(self, order):
        '''
        记录交易执行情况
        :param order:
        :return:
        '''
        # 如果 order 为 submitted/accepted,返回空
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        # 如果order为buy/sell executed,报告价格结果
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    f"买入:\n价格:{order.executed.price},\
                                成本:{order.executed.value},\
                                手续费:{order.executed.comm}"
                )
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            elif order.issell():
                self.log(
                    f"卖出:\n价格：{order.executed.price},\
                               成本: {order.executed.value},\
                               手续费{order.executed.comm}"
                )
            # self.bar_executed = len(self)
            # print('=======order',self.bar_executed)
        # 如果指令取消/交易失败, 报告结果
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None


    def next(self):
        '''
        主逻辑
        :return:
        '''
        # 检查是否有指令等待执行,
        if self.order:
            self.log("==is order: %s" % self.order)
            return

        # 检查是否持仓
        if not self.position:
            # 执行买入条件判断：上涨突破20日均线执行买入
            if self.data_close[0] > self.sma[0]:
                self.log('BUY CREATE, %.2f' % self.data_close[0])
                self.order = self.buy()
        else:
            # 执行卖出条件判断：下跌突破20日均线执行卖出
            if self.data_close[0] < self.sma[0]:
                self.log('SELL CREATE, %.2f' % self.data_close[0])
                self.order = self.sell()

    def notify_trade(self, trade):
        """
        记录交易收益情况
        """
        if not trade.isclosed:
            return
        self.log(f"策略收益：\n毛收益 {trade.pnl:.2f}, 净收益 {trade.pnlcomm:.2f}")

    def stop(self):
        """
        回测结束后输出结果
        """
        self.log("(MA均线： %2d日) 期末总资金 %.2f" % (self.params.maperiod, self.broker.getvalue()), do_print=True)

# 修改字段名与backtrader一致
def change_column_name(data):

    name_clomuns = data.columns.tolist()
    new_name_dict = {}
#日期,开盘,收盘,最高,最低,成交量,成交额,振幅,涨跌幅,涨跌额,换手率
    for name in name_clomuns:

        # if name == '日期':
        #     new_name_dict[name] = 'datetime'
        if name == '开盘':
            new_name_dict[name] = 'open'
        if name == '收盘':
            new_name_dict[name] = 'close'
        if name == '最高':
            new_name_dict[name] = 'high'
        if name == '最低':
            new_name_dict[name] = 'low'
        if name == '成交量':
            new_name_dict[name] = 'volume'
        if name == 'HTSCSecurityID':
            new_name_dict[name] = 'sec_code'

    data.rename(columns=new_name_dict, inplace=True)
    return data
def download_stock_day(code):
    # 准备数据
    print("正在下载" + str(code) + "日线数据")
    try:
        stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, period="daily",start_date="20100101",end_date="20500101", adjust="")
        stock_zh_a_hist_df.to_csv("./stock/day/" + str(code) + ".csv")
    except:
        print("下载异常" + str(code) + "....")
        time.sleep(1)
    else:
        print("下载stock" + str(code) + "日线数据完成")
        time.sleep(0.5)

def download_etf_day(code):

    # 准备数据
    print("正在下载" + str(code) + "日线数据")
    try:
        #不复权  前复权qfq 后复权 hfq
        fund_etf_hist_em_df = ak.fund_etf_hist_em(symbol=code, period="daily", start_date="20100101", end_date="20501201", adjust="")
        fund_etf_hist_em_df.to_csv("./etf/day/" + str(code) + ".csv")
    except:
        print("下载异常" + str(code) + "....")
        time.sleep(1)
    else:
        print("下载etf " + str(code) + "日线数据完成")
        time.sleep(0.5)


def main(code="512170",type='etf', start_cash=1000000, stake=100, commission_fee=0.001):
    cerebro = bt.Cerebro()
    # cerebro.optstrategy(MyStrategy, maperiod=range(3, 31))  # 导入策略参数寻优
    cerebro.addstrategy(MyStrategy,maperiod=55,printlog=True)
    # 读取数据
    if type =='etf':
        download_etf_day(code)
        df = pd.read_csv(f'./etf/day/{code}.csv', index_col=0, parse_dates=True, encoding='utf-8')
    else:
        download_stock_day(code)
        df = pd.read_csv(f'./stock/day/{code}.csv', index_col=0, parse_dates=True, encoding='utf-8')

    new_df = change_column_name(df)
    # new_df['datetime'] = pd.to_datetime(df['日期'])
    # 把 date 作为日期索引，以符合 Backtrader 的要求
    new_df.index = pd.to_datetime(df['日期'])
    # new_df.set_index('datetime', inplace=True)
    start_date = datetime(2021, 4, 3)  # 回测开始时间
    end_date = datetime(2023, 12, 15)  # 回测结束时间
    # 给cerebro添加数据
    data = bt.feeds.PandasData(dataname=new_df, fromdate=start_date, todate=end_date)

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



if __name__ == '__main__':
    main()
