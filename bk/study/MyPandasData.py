import backtrader as bt


class MyPandasData(bt.feeds.PandasData):
    # lines = (
    #     "datetime",
    #     "open",
    #     "close",
    #     "high",
    #     "low",
    #     "volume",
    #     "amount",
    #     "amplitude",
    #     "change_pct",
    #     "change_amt",
    #     "turnover",
    # )
    # 添加自定义参数
    # params = (
    #     ('my_custom_param', None),  # 新的自定义参数
    #     ('datetime', None),
    #
    #     # Possible values below:
    #     #  None : column not present
    #     #  -1 : autodetect position or case-wise equal name
    #     #  >= 0 : numeric index to the colum in the pandas dataframe
    #     #  string : column name (as index) in the pandas dataframe
    #     ('open', None),
    #     ('close', None),
    #     ('high', None),
    #     ('low', None),
    #     ('volume', None),
    #     ('amount', None),
    #     ('amplitude', None),
    #     ('change_pct', None),
    #     ('change_amt', None),
    #     ('turnover', None),
    # )
    params = (

        # Possible values for datetime (must always be present)
        #  None : datetime is the "index" in the Pandas Dataframe
        #  -1 : autodetect position or case-wise equal name
        #  >= 0 : numeric index to the colum in the pandas dataframe
        #  string : column name (as index) in the pandas dataframe
        ('datetime', None),

        # Possible values below:
        #  None : column not present
        #  -1 : autodetect position or case-wise equal name
        #  >= 0 : numeric index to the colum in the pandas dataframe
        #  string : column name (as index) in the pandas dataframe
        ('open', -1),
        ('high', -1),
        ('low', -1),
        ('close', -1),
        ('volume', -1),
        ('openinterest', -1),
    )

    def __init__(self, **kwargs):
        # 调用父类的 __init__ 方法
        super().__init__(**kwargs)

    def start(self):
        # 在数据加载开始前的初始化操作
        pass

    def prenext(self):
        # 在下一个时间步之前的数据预处理操作
        pass

    def next(self):
        # 在每个时间步的策略逻辑实现
        pass

    def stop(self):
        pass


# 在数据加载结束后的清理操作



