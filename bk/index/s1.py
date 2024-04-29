import backtrader as bt


# 自定义趋势判断指标
class TrendIdentifier(bt.Indicator):
    lines = ('trend',)
    params = (('period', 14),)

    def __init__(self):
        self.addminperiod(self.params.period)

    def next(self):
        high = self.data.high
        low = self.data.low
        close = self.data.close

        highest_high = bt.indicators.Highest(high, period=self.params.period)
        lowest_low = bt.indicators.Lowest(low, period=self.params.period)
        atr = bt.indicators.ATR(high, low, close, period=self.params.period)

        if close > highest_high[-1] - atr[-1]:
            self.lines.trend[0] = '上涨'
        elif close < lowest_low[-1] + atr[-1]:
            self.lines.trend[0] = '下跌'
        elif close > highest_high[-1] - 2 * atr[-1]:
            self.lines.trend[0] = '上涨中继'
        elif close < lowest_low[-1] + 2 * atr[-1]:
            self.lines.trend[0] = '下跌中继'
        else:
            self.lines.trend[0] = '震荡'

class MyStrategy(bt.Strategy):
    def __init__(self):
        # self.trend_indicator = TrendIdentifier()

        self.rsi = bt.indicators.RSI(self.data.close, period=14)
        o_macd=bt.indicators.MACD()
        self.macd, self.macd_signal= o_macd.macd,o_macd.signal
        self.sma_short = bt.indicators.SimpleMovingAverage(self.data.close, period=10)
        self.sma_long = bt.indicators.SimpleMovingAverage(self.data.close, period=30)
        self.position_size = 0.5  # 初始仓位大小

    def next(self):
        # market_phase = self.trend_indicator.trend[0]
        # 获取当前的市场行情阶段
        if self.data.close > self.sma_long:
            market_phase = '上涨'
        elif self.data.close < self.sma_long:
            market_phase = '下跌'
        else:
            #下跌中继
            market_phase = '震荡'

        # 根据市场行情阶段选择不同的策略和买卖点指标
        if market_phase == '上涨':
            print("上涨")
            if not self.position:
                if self.rsi < 30:
                    # 根据买点指标生成买入信号
                    self.buy(size=self.position_size * self.broker.get_cash())
            else:
                if self.rsi > 70:
                    # 根据卖点指标生成卖出信号
                    self.sell()

        elif market_phase  == '下跌':
            # if not self.position:
            #     # 根据买点指标生成买入信号
            #     if self.macd > self.macd_signal:
            #         self.buy(size=self.position_size * self.broker.get_cash())
            # else:
            #     if self.rsi > 70:
            #         # 根据卖点指标生成卖出信号
            #         self.sell()
            pass

        elif market_phase == '上涨中继':
            print("上涨中继")
            pass
        elif market_phase == '下跌中继':
            print("下跌中继")
            pass
        else:
            print("震荡")

        # 根据加减仓位管理规则进行调整
        if self.rsi > 70:
            self.position_size *= 0.9
        elif self.rsi < 30:
            self.position_size *= 1.1
