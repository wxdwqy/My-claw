import akshare as ak
import warnings
warnings.filterwarnings('ignore')

results = {}

# 1. 纳斯达克综合
try:
    df = ak.index_investing_global_index_hist(symbol='美国纳斯达克综合指数', period='daily', start_date='20260331', end_date='20260402')
    row = df.iloc[-1]
    results['纳斯达克综合'] = {'close': row['收盘'], 'change': row['涨跌幅']}
    print(f"纳斯达克综合: close={row['收盘']}, change={row['涨跌幅']}%")
except Exception as e:
    print(f'NC Error: {str(e)[:80]}')

# 2. TecDAX
try:
    df = ak.index_investing_global_index_hist(symbol='TecDAX', period='daily', start_date='20260331', end_date='20260402')
    row = df.iloc[-1]
    results['TecDAX'] = {'close': row['收盘'], 'change': row['涨跌幅']}
    print(f"TecDAX: close={row['收盘']}, change={row['涨跌幅']}%")
except Exception as e:
    print(f'TecDAX Error: {str(e)[:80]}')

# 3. KOSDAQ
try:
    df = ak.index_investing_global_index_hist(symbol='KOSDAQ', period='daily', start_date='20260331', end_date='20260402')
    row = df.iloc[-1]
    results['KOSDAQ'] = {'close': row['收盘'], 'change': row['涨跌幅']}
    print(f"KOSDAQ: close={row['收盘']}, change={row['涨跌幅']}%")
except Exception as e:
    print(f'KOSDAQ Error: {str(e)[:80]}')

# 4. 恒生科技 - 从东财港股列表
try:
    df = ak.stock_hk_spot_em()
    hst = df[df['名称'].str.contains('恒生科技', na=False)]
    if len(hst) > 0:
        row = hst.iloc[0]
        results['恒生科技'] = {'close': row['最新价'], 'change': row['涨跌幅']}
        print(f"恒生科技: close={row['最新价']}, change={row['涨跌幅']}%")
    else:
        print('恒生科技: not found in HK spot')
except Exception as e:
    print(f'恒生科技 Error: {str(e)[:80]}')

print('\n=== DONE ===')
