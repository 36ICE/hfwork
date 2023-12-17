import pandas as pd

# 创建 DataFrame
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# 创建要添加的行数据
new_row = pd.DataFrame({'A': [7], 'B': [8]})

# 使用 append() 方法添加行数据
df.loc[len(df.index)]=[1,3]

print(df)