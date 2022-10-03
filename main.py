# This is a sample Python script.
import pandas as pd
import pandas.io.sql
import sqlalchemy
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# 导入tushare
import tushare as ts
import baostock as bs
import pandas as pd

# 初始化pro接口
pro = ts.pro_api('f93d5d66fea3fafa40128e10ea0335ae4f9c70c54abdaffd4dd9939e')
# from jqdata import finance

engine = sqlalchemy.create_engine('mysql+pymysql://root:111111@127.0.0.1:3306/stock?charset=utf8')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 拉取数据
    # df = pro.query('stock_basic',
    #                'ts_code,symbol,name,area,industry,market,list_date,fullname,enname,cnspell,exchange,curr_type,list_status,delist_date,is_hs',
    #                **{
    #                    "limit":5000,
    #                    "offset":0
    #                })
    # sql = """
    # CREATE TABLE `shares11` (
    #   `ts_code` varchar(50) DEFAULT NULL,
    #   `symbol` varchar(50) DEFAULT NULL,
    #   `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
    #   `area` varchar(50) DEFAULT NULL,
    #   `industry` varchar(50) DEFAULT NULL,
    #   `market` varchar(50) DEFAULT NULL,
    #   `list_date` varchar(50) DEFAULT NULL,
    #   `fullname` varchar(50) DEFAULT NULL,
    #   `enname` varchar(50) DEFAULT NULL,
    #   `cnspell` varchar(50) DEFAULT NULL,
    #   `exchange` varchar(50) DEFAULT NULL,
    #   `curr_type` varchar(50) DEFAULT NULL,
    #   `list_status` varchar(50) DEFAULT NULL,
    #   `delist_date` varchar(50) DEFAULT NULL,
    #   `is_hs` varchar(50) DEFAULT NULL
    # )"""
    # pandas.io.sql.to_sql(df,'shares',engine,'stock',index=False,if_exists=if_exists)
    # df = pro.query('daily',
    #            'ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount',
    #            **{
    #                "limit":10000,
    #                "offset":0,
    #                "trade_date":"20210105"
    #            })
    # df = pro.query('get_tick_data',
    #            'ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount',
    #            **{
    #                "ts_code":"000011.SZ",
    #                "freq":1,
    #                "asset":"E"
    #            })
    # print(df)
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)
    #### 获取沪深A股历史K线数据 ####
    # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
    # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    rs = bs.query_history_k_data_plus("sh.600000",
    "date,time,code,open,high,low,close,volume,amount,adjustflag",
    start_date='2015-01-01', end_date='2022-09-30',
    frequency="5", adjustflag="3")
    print('query_history_k_data_plus respond error_code:' + rs.error_code)
    print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)
    #### 打印结果集 ####
    data_list = []
    while (rs.error_code == '0') & rs.next():
        # 获取一条记录，将记录合并在一起
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)

    #### 结果集输出到csv文件 ####
    result.to_csv("D:\\history_A_stock_k_data.csv", index=False)
    print(result)

    #### 登出系统 ####
    bs.logout()