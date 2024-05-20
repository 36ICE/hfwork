
import logging

import time
from datetime import datetime

import requests
import pandas as pd
import glob


from bk.config import CURRENT_WORKSPACE_DIRECTORY
# 获取当前文件所在的文件夹路径
# CURRENT_WORKSPACE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

header_mapping = {
    '标题': 'title',
    '日期': 'datetime',
    '时间': 'datetime',
    '发布时间': 'datetime',
    '内容': 'context',
    '链接': 'url',
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
# 检查文件是否存在
data_path = f"{CURRENT_WORKSPACE_DIRECTORY}/data/news/"

def stock_info_global_sina(page=1, page_size=40) -> pd.DataFrame:
    """
    新浪财经-全球财经快讯
    https://finance.sina.com.cn/7x24
    :return: 全球财经快讯
    :rtype: pandas.DataFrame
    """
    url = "https://zhibo.sina.com.cn/api/zhibo/feed"
    params = {
        "page": page,
        "page_size": page_size,
        "zhibo_id": "152",
        "tag_id": "0",
        "dire": "f",
        "dpc": "1",
        "pagesize": page_size,
        "type": "1",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    time_list = [
        item["create_time"] for item in data_json["result"]["data"]["feed"]["list"]
    ]
    text_list = [
        item["rich_text"] for item in data_json["result"]["data"]["feed"]["list"]
    ]
    temp_df = pd.DataFrame([time_list, text_list]).T
    temp_df.columns = ["时间", "内容"]
    return temp_df


def stock_info_global_ths(page=1, page_size=40) -> pd.DataFrame:
    """
    同花顺财经-全球财经直播
    https://news.10jqka.com.cn/realtimenews.html
    https://news.10jqka.com.cn/tapp/news/push/stock/?page=1&tag=&track=website&ctime=1716209675
    :return: 全球财经直播
    :rtype: pandas.DataFrame
    """
    url = "https://news.10jqka.com.cn/tapp/news/push/stock"
    params = {
        "page": page,
        "tag": "",
        "track": "website",
        "pagesize": page_size,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/111.0.0.0 Safari/537.36"
    }
    r = requests.get(url, params=params, headers=headers)
    data_json = r.json()
    temp_df = pd.DataFrame(data_json["data"]["list"])
    temp_df = temp_df[["title", "digest", "rtime", "url"]]
    temp_df["rtime"] = [
        datetime.fromtimestamp(int(item)).strftime("%Y-%m-%d %H:%M:%S")
        for item in temp_df["rtime"]
    ]
    temp_df.rename(
        columns={
            "title": "标题",
            "digest": "内容",
            "rtime": "发布时间",
            "url": "链接",
        },
        inplace=True,
    )
    return temp_df
error_page=[]

def merge():

    # 获取所有的CSV文件路径
    file_paths = glob.glob(data_path + '*.csv')

    # 创建一个空的DataFrame用于存储合并后的数据
    merged_data = pd.DataFrame()

    # 逐个读取并合并CSV文件
    for file_path in file_paths:
        df = pd.read_csv(file_path)
        merged_data = pd.concat([merged_data, df], ignore_index=True)

    # 保存合并后的数据为CSV文件
    merged_data.to_csv(data_path + 'merged_data.csv', index=False)

    # 打印保存成功的提示信息
    print("CSV文件合并完成并保存为 merged_data.csv")

def download_etf_day(page, page_size=200):
    # 准备数据
    print("正在下载第" + str(page) + "页数据")
    try:

        # import akshare as ak
        news_df = stock_info_global_sina(page, page_size)
        # news_df = stock_info_global_ths(page,page_size)
        news_df = news_df.rename(columns=header_mapping)
        print(news_df)
        # 设置index
        news_df.set_index('datetime', inplace=True, drop=False)

        # 检查文件是否存在
        filename = f"{data_path}{page}.csv"
        news_df.to_csv(filename, header=True, index=False)
    except Exception as e:
        logging.error("下载新闻数据第 %s page数据完成", str(page), e)
        error_page.append(page)
        time.sleep(1)
    else:
        logging.error("下载新闻数据第 %s page数据完成", str(page))
        # time.sleep(0.1)


for i in range(1,10000):
    download_etf_day(i,80)

print(error_page)

#补数
for i in error_page:
    download_etf_day(i,80)
#合并文件
# merge()