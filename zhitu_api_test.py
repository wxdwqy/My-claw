"""
智兔数据API测试脚本 v3 - 修正版
- Token: 4BDA45E5-F103-4FE4-8C91-530D44F68C67
- 基础URL: https://api.zhituapi.com/
"""

import requests
import json
from datetime import datetime

TOKEN = "4BDA45E5-F103-4FE4-8C91-530D44F68C67"
BASE_URL = "https://api.zhituapi.com/"

def api(path, params=None):
    """通用API调用"""
    url = BASE_URL + path
    if params is None:
        params = {}
    params["token"] = TOKEN
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def test_all():
    """全面测试所有接口"""
    print(">> 智兔数据API 测试 v3 (修正版)")
    print(f"Token: {TOKEN[:8]}...{TOKEN[-4:]}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # -- 1. 股票列表 --
    print("[1] 股票列表")
    try:
        data = api("hs/list/all")
        if isinstance(data, list):
            print(f"  ✅ OK - 共 {len(data)} 只股票/板块")
            print(f"  示例: {data[0].get('dm', 'N/A')} | {data[0].get('mc', 'N/A')} | {data[0].get('jys', 'N/A')}")
        else:
            print(f"  ⚠️ WARN - 返回非列表: {str(data)[:100]}")
    except Exception as e:
        print(f"  ❌ FAIL - {e}")

    # -- 2. 指数实时行情 (使用 /hz/ 接口) --
    print("\n[2] 指数实时行情")
    indices = [
        ("000001.SH", "上证指数"),
        ("399001.SZ", "深证成指"),
        ("399006.SZ", "创业板指"),
        ("000300.SH", "沪深300"),
        ("000016.SH", "上证50"),
        ("000688.SH", "科创50"),
    ]
    for code, name in indices:
        try:
            d = api(f"hz/real/ssjy/{code}")
            if isinstance(d, dict):
                p = d.get("p", "N/A")
                pc = d.get("pc", "N/A")
                cje = d.get("cje", "N/A")
                print(f"  ✅ {name}({code}): {p} | {pc}% | 成交额:{cje}")
            else:
                print(f"  ⚠️ {name}({code}): {str(d)[:100]}")
        except Exception as e:
            print(f"  ❌ FAIL {name}({code}): {e}")

    # -- 3. 个股实时行情 (代码不带后缀) --
    print("\n[3] 个股实时行情")
    stocks = [
        ("600519", "贵州茅台"),
        ("000001", "平安银行"),
        ("300750", "宁德时代"),
    ]
    for code, name in stocks:
        try:
            d = api(f"hs/real/ssjy/{code}")
            if isinstance(d, dict):
                p = d.get("p", "N/A")
                pc = d.get("pc", "N/A")
                pe = d.get("pe", "N/A")
                sz = d.get("sz", "N/A")
                print(f"  ✅ {name}({code}): {p} | {pc}% | PE={pe} | 市值={sz}")
            else:
                print(f"  ⚠️ {name}({code}): {str(d)[:100]}")
        except Exception as e:
            print(f"  ❌ FAIL {name}({code}): {e}")

    # -- 4. 概念板块列表 --
    print("\n[4] 概念板块列表")
    try:
        data = api("hs/list/sectors")
        if isinstance(data, list):
            print(f"  ✅ OK - 共 {len(data)} 个概念板块")
            for s in data[:5]:
                print(f"    {s.get('dm', 'N/A')} | {s.get('mc', 'N/A')} | {s.get('jys', 'N/A')}")
        elif isinstance(data, dict):
            print(f"  字段: {list(data.keys())}")
    except Exception as e:
        print(f"  ❌ FAIL - {e}")

    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)

if __name__ == "__main__":
    test_all()
