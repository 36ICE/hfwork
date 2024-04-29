import backtrader as bt

from bk.index.index import MyIndicator

'''

使用自定义指标实现策略

'''


# 创建策略类
class MyStrategy(bt.Strategy):
    def __init__(self):
        self.my_indicator = MyIndicator(self.data.close)  # 使用自定义指标

    def next(self):
        # 访问自定义指标的值
        indicator_value = self.my_indicator[0]
        print(f"My Indicator: {indicator_value}")



if __name__ == '__main__':

    pass