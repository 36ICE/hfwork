import time

import akshare as ak

# stock_sse_summary_df = ak.stock_sse_summary()
# print(stock_sse_summary_df)
# import akshare as ak
#
# stock_individual_info_em_df = ak.stock_individual_info_em(symbol="000001")
# print(stock_individual_info_em_df)
# import akshare as ak
#
# stock_bid_ask_em_df = ak.stock_bid_ask_em(symbol="000001")
# print(stock_bid_ask_em_df)
#
import pandas

stock_zh_a_spot_em_df = ak.stock_zh_a_spot_em().sort_values(by='代码',ascending=True)
print(stock_zh_a_spot_em_df['代码'])
err_list =[]
# stock_zh_a_spot_em_df.to_csv("./stock_zh_a_spot_em.csv")
for code in stock_zh_a_spot_em_df['代码'][34:]:
    print("正在下载"+str(code)+"日线数据")
    try:
        stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, period="daily", adjust="")
        stock_zh_a_hist_df.to_csv("./history/day/" + str(code) + ".csv")
    except:
        print("下载异常"+str(code)+"....")
        err_list.append(str(code))
        time.sleep(1)
    else:
        print("下载"+str(code)+"日线数据完成")
        time.sleep(0.5)
result=pandas.DataFrame(err_list)
result.to_csv("err_code.csv")
for code in err_list:
    print("正在下载缺失的" + str(code) + "日线数据")
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=code, period="daily", adjust="")
    stock_zh_a_hist_df.to_csv("./history/day/" + str(code) + ".csv")
    print("下载" + str(code) + "日线数据完成")




















# stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily",  adjust="")
# print(stock_zh_a_hist_df)
# stock_zh_a_hist_df.to_csv("./history/day/000001.csv")
# stock_comment_detail_scrd_focus_em_df = ak.stock_comment_detail_scrd_focus_em(symbol="600000")
# print(stock_comment_detail_scrd_focus_em_df)
# fund_etf_spot_em_df = ak.fund_etf_spot_em()
# print(fund_etf_spot_em_df)
