from datetime import datetime

import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt  # 由于 Backtrader 的问题，此处要求 pip install matplotlib==3.2.2
import pandas as pd


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
