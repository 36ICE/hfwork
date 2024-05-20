import time
import akshare as ak

dce_text = ak.match_main_contract(symbol="dce")
czce_text = ak.match_main_contract(symbol="czce")
shfe_text = ak.match_main_contract(symbol="shfe")
gfex_text = ak.match_main_contract(symbol="gfex")

# while True:
#     time.sleep(3)
#     futures_zh_spot_df = ak.futures_zh_spot(
#         symbol=",".join([dce_text, czce_text, shfe_text, gfex_text]),
#         market="CF",
#         adjust='0')
#     print(futures_zh_spot_df)


import akshare as ak

get_futures_daily_df = ak.get_futures_daily(start_date="20200701", end_date="20200716", market="DCE")
print(get_futures_daily_df)