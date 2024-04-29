# class NDHIGH(bt.Indicator):
#     # lines特点逗号不能省略
#     lines = ('high',)
#     params = (('short_period', 8),
#               ('long_period', 21),
#               ('signal_period', 5),
#               )
#     plotlines = dict(
#         dif=dict(_name='DIF', ls='', color='blue'),
#         dea=dict(_name='DEA', ls='', color='red'),
#         macd=dict(_name='MACD', _method='bar', alpha=1, _fill_gt=(0, 'red'), _fill_lt=(0, 'green')),
#         high=dict(_name='high', ls='-', color='red'),
#
#     )
#     plotinfo = dict(
#         plot=True,  # 是否绘制
#         subplot=False,  # 是否绘制成子图
#         plotabove=True,
#     )
#
#     def __init__(self):
#         ema_short = bt.indicators.ExponentialMovingAverage(self.download, period=self.params.short_period)
#         ema_long = bt.indicators.ExponentialMovingAverage(self.download, period=self.params.long_period)
#         self.l.dif = ema_short - ema_long
#         self.l.dea = bt.indicators.ExponentialMovingAverage(self.l.dif, period=self.params.signal_period)
#         self.l.macd = (self.l.dif - self.l.dea) * 8
#
#         # macd周期计数
#         self.macd_up = 0
#         self.macd_down = 0
#         self.macd_add = 1
#
#     def next(self):
#         if self.l.macd[0] > 0 and self.l.macd[-1] < 0:
#             # self.macd_down=0
#             self.macd_add = self.macd_up
#             self.macd_up = 0
#
#         if self.l.macd[0] < 0 and self.l.macd[-1] > 0:
#             self.macd_down = 0
#         self.macd_up += 1
#         self.macd_down += 1
#         data_high = self.download.high.get(ago=0 - self.macd_up, size=self.macd_add)
#         self.l.high[0] = max(data_high)