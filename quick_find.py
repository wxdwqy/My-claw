import akshare as ak, warnings, sys
warnings.filterwarnings('ignore')

print('=== 1. 纳斯达克综合 ===', flush=True)
try:
    df = ak.index_investing_global_index_hist(symbol='美国纳斯达克综合指数', period='daily', start_date='20260331', end_date='20260402')
    print(df.tail(2).to_string(), flush=True)
except Exception as e:
    print('Error:', str(e)[:80], flush=True)

print('=== 2. TecDAX ===', flush=True)
try:
    df = ak.index_investing_global_index_hist(symbol='TecDAX', period='daily', start_date='20260331', end_date='20260402')
    print(df.tail(2).to_string(), flush=True)
except Exception as e:
    print('Error:', str(e)[:80], flush=True)

print('=== 3. KOSDAQ ===', flush=True)
try:
    df = ak.index_investing_global_index_hist(symbol='KOSDAQ', period='daily', start_date='20260331', end_date='20260402')
    print(df.tail(2).to_string(), flush=True)
except Exception as e:
    print('Error:', str(e)[:80], flush=True)

print('=== 4. 恒生科技 ===', flush=True)
try:
    df = ak.stock_hk_spot_em()
    hst = df[df['名称'].str.contains('科技', na=False)]
    print(hst[['名称','最新价','涨跌幅','昨收']].to_string(), flush=True)
except Exception as e:
    print('Error:', str(e)[:80], flush=True)

print('=== DONE ===', flush=True)
