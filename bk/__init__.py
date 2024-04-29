# from datetime import datetime
# import backtrader as bt
#
# class SmaCross(bt.SignalStrategy):
#     def __init__(self):
#         sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
#         crossover = bt.ind.CrossOver(sma1, sma2)
#         self.signal_add(bt.SIGNAL_LONG, crossover)
#
# cerebro = bt.Cerebro()
# cerebro.addstrategy(SmaCross)
#
# data0 = bt.feeds.BacktraderCSV(dataname='../yc/day/600036.csv', fromdate=datetime(2023, 1, 3),
#                                   todate=datetime(2023, 12, 12))
# cerebro.adddata(data0)
#
# cerebro.run()
# cerebro.plot()
#
#
#
# import backtrader as bt
#
#
# if __name__ == '__main__':
#     cerebro = bt.Cerebro()
#
#     print("starting portfolio value: %.2f" % cerebro.broker.getvalue())
#
#     cerebro.run()
#
#     print("final portfolio value: %.2f" % cerebro.broker.getvalue())