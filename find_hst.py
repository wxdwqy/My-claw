import akshare as ak
import warnings
warnings.filterwarnings('ignore')

# 恒生科技 - 从东财港股实时
df = ak.stock_hk_spot_em()
print('=== Columns:', list(df.columns))
# 搜索恒生科技
hst = df[df['名称'].str.contains('科技', na=False)]
print('=== 科技相关:')
print(hst[['名称','最新价','涨跌幅','昨收']].to_string())
# 也搜索恒生
hs = df[df['名称'].str.contains('恒生', na=False)]
print('=== 恒生相关:')
print(hs[['名称','最新价','涨跌幅','昨收']].to_string())
