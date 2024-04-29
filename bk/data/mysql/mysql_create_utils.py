# 连接MySQL数据库
import pandas as pd
import pymysql
import akshare as ak
from sqlalchemy import create_engine

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    port=33060,
    db='hf'
)

engine = create_engine('mysql+pymysql://root:123456@localhost:33060/hf?charset=utf8')


# 创建股票基本信息表
def create_stock_info_table():
    sql = """CREATE TABLE IF NOT EXISTS stock_info (
                stock_code VARCHAR(10) PRIMARY KEY,
                stock_name VARCHAR(100),
                listing_date DATE,
                industry VARCHAR(100)
            )"""
    cursor = conn.cursor()
    cursor.execute(sql)

# 创建股票价格数据表
def create_stock_price_table():
    sql = """CREATE TABLE IF NOT EXISTS stock_price (
                stock_code VARCHAR(10),
                date DATE,
                open_price FLOAT,
                high_price FLOAT,
                low_price FLOAT,
                close_price FLOAT,
                volume INT,
                PRIMARY KEY (stock_code, date),
                FOREIGN KEY (stock_code) REFERENCES stock_info(stock_code)
            )"""
    cursor = conn.cursor()
    cursor.execute(sql)

# 创建股票基本面数据表
def create_fundamental_data_table():
    sql = """CREATE TABLE IF NOT EXISTS fundamental_data (
                stock_code VARCHAR(10),
                date DATE,
                pe_ratio FLOAT,
                pb_ratio FLOAT,
                eps FLOAT,
                net_assets_per_share FLOAT,
                PRIMARY KEY (stock_code, date),
                FOREIGN KEY (stock_code) REFERENCES stock_info(stock_code)
            )"""
    cursor = conn.cursor()
    cursor.execute(sql)

# 创建行业数据表
def create_industry_data_table():
    sql = """CREATE TABLE IF NOT EXISTS industry_data (
                industry_code VARCHAR(10) PRIMARY KEY,
                industry_name VARCHAR(100),
                stock_code VARCHAR(10),
                FOREIGN KEY (stock_code) REFERENCES stock_info(stock_code)
            )"""
    cursor = conn.cursor()
    cursor.execute(sql)

# 创建宏观经济数据表
def create_macro_data_table():
    sql = """CREATE TABLE IF NOT EXISTS macro_data (
                date DATE,
                indicator_name VARCHAR(100),
                indicator_value FLOAT,
                PRIMARY KEY (date, indicator_name)
            )"""
    cursor = conn.cursor()
    cursor.execute(sql)
# 创建股票数据表
def create_stock_data_table():
    sql = """CREATE TABLE IF NOT EXISTS stock_data (
                stock_code VARCHAR(10) PRIMARY KEY,
                stock_name VARCHAR(100),
                pe_ratio FLOAT,
                pb_ratio FLOAT,
                eps FLOAT,
                industry VARCHAR(100)
            )"""
    cursor = conn.cursor()
    cursor.execute(sql)

def init_mysql():
    # 调用创建表函数
    create_stock_info_table()
    create_stock_price_table()
    create_fundamental_data_table()
    create_industry_data_table()
    create_macro_data_table()
    create_stock_data_table
    # 关闭数据库连接
    conn.close()

# init_mysql()

