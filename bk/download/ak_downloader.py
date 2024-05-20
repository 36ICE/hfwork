import logging
import akshare as ak
import time
import pandas as pd

# 配置日志输出
from pypinyin import pinyin, Style

from bk.config import *
from bk.data.mysql.mysql_create_utils import conn, engine

logging.basicConfig(level=logging.ERROR, format='[%(levelname)s] %(asctime)s - %(message)s')

'''
原始数据前缀：

你可以使用前缀 'raw_' 或 'source_' 来表示原始数据。例如，如果你的数据集名为 data.csv，
你可以将原始数据表命名为 'raw_data' 或 'source_data'。
特征数据前缀：

对于特征数据，你可以使用前缀 'feat_' 或 'feature_' 来表示。例如，如果你的特征数据表包含特征列如 'age'、'gender' 等，
你可以将特征数据表命名为 'feat_age_gender' 或 'feature_age_gender'。
结果数据前缀：

对于结果数据，你可以使用前缀 'result_' 或 'output_' 来表示。例如，如果你的结果数据表包含结果列如 'prediction'、'score' 等，
你可以将结果数据表命名为 'result_prediction_score' 或 'output_prediction_score'。

'''

# 设置列头映射
header_mapping = {
    '日期': 'datetime',
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


class AKDownloader:

    def download_stock_day(code):
        '''
        下载股票日线数据
        :param code:
        :return:
        '''
        # 准备数据
        print("正在下载" + str(code) + "日线数据")
        try:
            stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date="20100101",
                                                    end_date="20500101",
                                                    adjust="")
            stock_zh_a_hist_df = stock_zh_a_hist_df.rename(columns=header_mapping)
            stock_zh_a_hist_df['datetime'] = pd.to_datetime(stock_zh_a_hist_df['datetime'])
            # 将日期时间格式化为特定格式
            stock_zh_a_hist_df['datetime'] = stock_zh_a_hist_df['datetime'].dt.strftime('%Y%m%d')
            stock_zh_a_hist_df['datetime'] = pd.to_datetime(stock_zh_a_hist_df['datetime'])
            stock_zh_a_hist_df.set_index('datetime', inplace=True, drop=False)
            # 检查文件是否存在
            filename = f"{CURRENT_WORKSPACE_DIRECTORY}/data/stock/day/{code}.csv"

            stock_zh_a_hist_df.to_csv(filename, header=True, index=False)
        except Exception as e:
            # 记录错误日志
            logging.error("下载stock %s 异常:%s", str(code), str(e), e)
            time.sleep(1)
        else:
            logging.error("下载stock %s 日线数据完成", str(code))
            time.sleep(0.5)
        return stock_zh_a_hist_df

    def download_etf_day(code):
        '''
        下载etf日线数据
        '''
        # 准备数据
        print("正在下载" + str(code) + "日线数据")
        try:
            # 不复权  前复权qfq 后复权 hfq
            fund_etf_hist_em_df = ak.fund_etf_hist_em(symbol=code, period="daily", start_date="20100101",
                                                      end_date="20501201", adjust="")
            fund_etf_hist_em_df = fund_etf_hist_em_df.rename(columns=header_mapping)
            fund_etf_hist_em_df['datetime'] = pd.to_datetime(fund_etf_hist_em_df['datetime'])
            # 将日期时间格式化为特定格式
            fund_etf_hist_em_df['datetime'] = fund_etf_hist_em_df['datetime'].dt.strftime('%Y%m%d')
            fund_etf_hist_em_df['datetime'] = pd.to_datetime(fund_etf_hist_em_df['datetime'])
            # 设置index
            fund_etf_hist_em_df.set_index('datetime', inplace=True, drop=False)

            # 检查文件是否存在
            filename = f"{CURRENT_WORKSPACE_DIRECTORY}/data/etf/day/{code}.csv"
            fund_etf_hist_em_df.to_csv(filename, header=True, index=False)
        except Exception as e:
            logging.error("下载etf %s 异常:%s", str(code), str(e), e)
            time.sleep(1)
        else:
            logging.error("下载etf %s 日线数据完成", str(code))
            time.sleep(0.5)
        return fund_etf_hist_em_df


def generate_mysql_schema(df, table_name):
    # 获取DataFrame的列名和列数据类型
    column_names = df.columns.tolist()
    column_types = df.dtypes.tolist()

    # 存储MySQL字段类型映射关系
    type_mapping = {
        'int64': 'INT',
        'float64': 'FLOAT',
        'object': 'VARCHAR(255)',
        'datetime64[ns]': 'DATETIME',
        'bool': 'BOOLEAN'
    }
    # 生成建表语句
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    for column_name, column_type in zip(column_names, column_types):
        # 将列名从中文转换为英文
        english_column_name = convert_to_english(column_name)
        mysql_type = type_mapping.get(str(column_type), ' VARCHAR(1000)')
        create_table_sql += f"\n{english_column_name} {mysql_type}"
        # 将中文写入表结构的备注中
        create_table_sql += f" COMMENT '{column_name}',"
    create_table_sql = create_table_sql.rstrip(',') + "\n);"
    print(create_table_sql)
    df = convert_dataframe_columns(df)
    return df


def convert_to_english(column_name):
    # 使用pypinyin将中文转换为拼音，默认样式为首字母大写
    pinyin_list = pinyin(column_name, style=Style.NORMAL)
    return '_'.join([item[0] for item in pinyin_list]).lower()


def convert_dataframe_columns(df):
    # 将列名从中文转换为英文
    english_columns = [convert_to_english(column) for column in df.columns]
    df.columns = english_columns
    return df


def company_info(code):
    '''
    公司概况-巨潮资讯
    :param code:
    :return:
    '''
    stock_profile_cninfo_df = ak.stock_profile_cninfo(symbol=code)

    return stock_profile_cninfo_df


def save_tosql(df, table_name):
    df = generate_mysql_schema(df, table_name)
    try:
        df.to_sql(table_name, engine, if_exists='append', index=False)
    except Exception as e:
        logging.error("save_tosql table_name:[%s] 异常:", str(table_name), e)


def stock_info_day():
    '''
    日周期数据

    :return:
    '''

    # 获取全市场个股的基本信息
    stock_list = ak.stock_info_a_code_name()
    stock_list.columns = ['code', 'name']
    df = pd.DataFrame()
    # stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em()
    for index, row in stock_list.head(8).iterrows():
        df = pd.concat([df, company_info(row['code'])], axis=0)
        time.sleep(1)

    save_tosql(df, 'raw_company_info')


def stock_zh_a_day_hist():
    # 获取全市场个股的基本信息
    stock_list = ak.stock_info_a_code_name()
    stock_list.columns = ['code', 'name']
    df = pd.DataFrame()
    for index, row in stock_list.head(8).iterrows():
        stock_df = ak.stock_zh_a_hist(row['code'], start_date="20100101", period='daily', adjust="hfq")
        stock_df.insert(0, 'code', row['code'])
        df = pd.concat([df, stock_df], axis=0)
        # time.sleep(1)
    save_tosql(df, 'raw_a_day_hist')



if __name__ == '__main__':
    stock_info_day()
    # stock_zh_a_day_hist()
    # stream_news_data()