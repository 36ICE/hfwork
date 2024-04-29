import pandas as pd
import pymysql
import logging

from sqlalchemy import create_engine


class MySQLToolbox:
    def __init__(self, host, username, password, port, database):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.database = database
        self.connection = None

    def connect(self):
        # self.connection = pymysql.connect(
        #     host=self.host,
        #     user=self.username,
        #     password=self.password,
        #     port=self.port,
        #     database=self.database
        # )
        #使用sqlalchemy
        engine = create_engine(f'mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}?charset=utf8')
        self.connection = engine.connect()
        logging.info("Connected to MySQL database")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            logging.info("Disconnected from MySQL database")

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        return result

    def query_builder(self, table):
        return QueryBuilder(self.connection, table)

    def execute_insert(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        last_insert_id = cursor.lastrowid
        cursor.close()
        return last_insert_id

    def execute_update(self, query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        return affected_rows

    def execute_delete(self, query, params=None):
        return self.execute_update(query, params)


class QueryBuilder:
    def __init__(self, connection, table):
        self.connection = connection
        self.table = table
        self.query = ""

    def select(self, columns="*"):
        self.query = f"SELECT {columns} FROM {self.table}"
        return self

    def where(self, condition):
        self.query += f" WHERE {condition}"
        return self

    def limit(self, limit):
        self.query += f" LIMIT {limit}"
        return self

    def join(self, table, condition, join_type="INNER"):
        self.query += f" {join_type} JOIN {table} ON {condition}"
        return self

    def group_by(self, columns):
        self.query += f" GROUP BY {columns}"
        return self

    def having(self, condition):
        self.query += f" HAVING {condition}"
        return self

    def order_by(self, columns, ascending=True):
        order = "ASC" if ascending else "DESC"
        self.query += f" ORDER BY {columns} {order}"
        return self

    def execute(self):
        # cursor = self.connection.cursor()
        # cursor.execute(self.query)
        # result = cursor.fetchall()
        # cursor.close()
        # return result
        return pd.read_sql(self.query, self.connection)


if __name__ == '__main__':
    # 示例用法
    toolbox = MySQLToolbox(host='localhost', username='root', password='123456', port=33060, database='hf')
    toolbox.connect()
    # 执行查询
    # query = "SELECT * FROM raw_a_day_hist"
    # result = toolbox.execute_query(query)
    # print(result)

    # 执行插入
    # insert_query = "INSERT INTO your_table (column1, column2) VALUES (%s, %s)"
    # insert_params = ('value1', 'value2')
    # last_insert_id = toolbox.execute_insert(insert_query, insert_params)
    # print("Last insert ID:", last_insert_id)

    # 执行更新
    # update_query = "UPDATE your_table SET column1 = %s WHERE id = %s"
    # update_params = ('new_value', 1)
    # affected_rows = toolbox.execute_update(update_query, update_params)
    # print("Affected rows:", affected_rows)

    # 执行删除
    # delete_query = "DELETE FROM your_table WHERE id = %s"
    # delete_params = (1,)
    # affected_rows = toolbox.execute_delete(delete_query, delete_params)
    # print("Affected rows:", affected_rows)

    query_builder = toolbox.query_builder("raw_a_day_hist")
    # result = query_builder.select("*") \
    #     .join("other_table", "your_table.id = other_table.id") \
    #     .where("column1 = 'value1'") \
    #     .group_by("column1") \
    #     .having("COUNT(column2) > 5") \
    #     .order_by("column1", ascending=False) \
    #     .limit(10) \
    #     .execute()

    df = query_builder.select("*") \
        .where("code = '000001'") \
        .order_by("ri_qi", ascending=True) \
        .limit(10) \
        .execute()
    print(df)
    toolbox.disconnect()
