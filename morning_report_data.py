import akshare as ak, warnings, sys
warnings.filterwarnings('ignore')

print('=== 全球指数实时 ===', flush=True)
df = ak.index_global_spot_em()
indices = {
    'NDX': '纳斯达克100',
    'SPX': '标普500',
    'GDAXI': 'DAX 40',
    'N225': '日经225',
    'KS11': 'KOSPI',
    'HSI': '恒生指数'
}
for code, name in indices.items():
    row = df[df['代码'] == code]
    if len(row) > 0:
        r = row.iloc[0]
        print(f'{name}|{r["最新价"]}|{r["涨跌幅"]}|{r["最新行情时间"]}', flush=True)

print('=== SOX ===', flush=True)
df2 = ak.macro_global_sox_index()
row2 = df2.iloc[-1]
print(f'费城半导体(SOX)|{row2["最新值"]}|{row2["涨跌幅"]}', flush=True)
print('=== DONE ===', flush=True)
