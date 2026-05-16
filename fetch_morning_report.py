# -*- coding: utf-8 -*-
import akshare as ak
import warnings
warnings.filterwarnings('ignore')
from datetime import datetime, timedelta
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

today = datetime.now().strftime('%Y%m%d')
yesterday = (datetime.now() - timedelta(days=3)).strftime('%Y%m%d')

results = {}

index_map = [
    ('nasdaq_comp', '美国纳斯达克综合指数', '纳斯达克'),
    ('nasdaq100',   '纳斯达克100',         '纳斯达克100'),
    ('sox',         '费城半导体指数',       '费城半导体(SOX)'),
    ('dax',         '德国DAX30指数',        'DAX 40'),
    ('tecdax',      'TecDAX指数',           'TecDAX'),
    ('nikkei',      '日经225指数',          '日经225'),
    ('kospi',       '韩国综合股价指数',      'KOSPI'),
    ('kosdaq',      '韩国KOSDAQ指数',        'KOSDAQ'),
    ('hstech',      '恒生科技指数',          '恒生科技'),
]

for key, symbol, label in index_map:
    try:
        df = ak.index_investing_global_index_hist(symbol=symbol, period='daily', start_date=yesterday, end_date=today)
        if df is not None and len(df) > 0:
            row = df.iloc[-1]
            results[label] = {
                'date': str(row.get('日期', row.index[0] if hasattr(row,'index') else '')),
                'close': row['收盘'],
                'change_pct': row['涨跌幅']
            }
        else:
            results[label] = {'error': '无数据'}
    except Exception as e:
        results[label] = {'error': str(e)[:80]}

print("=== 科技指数早报 ===")
print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print()
for label, v in results.items():
    if 'error' in v:
        print(f"{label}: 获取失败 ({v['error']})")
    else:
        pct = float(str(v['change_pct']).replace('%','').replace('+',''))
        arrow = '▲' if pct >= 0 else '▼'
        sign = '+' if pct >= 0 else ''
        print(f"{label}: {v['close']}  {arrow}{sign}{pct:.2f}%")
