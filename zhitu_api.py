"""
智兔数据API对接脚本 v2
- Token: 4BDA45E5-F103-4FE4-8C91-530D44F68C67
- 基础URL: https://api.zhituapi.com/hs/
- 字段映射: dm=代码, mc=名称, jys=交易所
"""

import requests
import json
from datetime import datetime

TOKEN = "4BDA45E5-F103-4FE4-8C91-530D44F68C67"
BASE_URL = "https://api.zhituapi.com/hs/"


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
    print(">> 智兔数据API 全面测试")
    print(f"Token: {TOKEN[:8]}...{TOKEN[-4:]}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # -- 1. 股票列表 --
    print("[1] 股票列表")
    try:
        data = api("list/all")
        if isinstance(data, list):
            print(f"  OK - 共 {len(data)} 只股票/板块")
            print(f"  示例: {data[0].get('dm', 'N/A')} | {data[0].get('mc', 'N/A')} | {data[0].get('jys', 'N/A')}")
        else:
            print(f"  WARN - 返回非列表: {str(data)[:100]}")
    except Exception as e:
        print(f"  FAIL - {e}")

    # -- 2. 指数实时行情 --
    print("\n[2] 指数实时行情")
    indices = [
        ("000001.SS", "上证指数"),
        ("399001.SZ", "深证成指"),
        ("399006.SZ", "创业板指"),
        ("000300.SS", "沪深300"),
        ("000016.SS", "上证50"),
        ("000688.SS", "科创50"),
    ]
    for code, name in indices:
        try:
            d = api(f"real/ssjy/{code}")
            if isinstance(d, dict) and "data" in d:
                dd = d["data"]
                price = dd.get("price", "N/A")
                change = dd.get("change_ratio", "N/A")
                change_amount = dd.get("change", "N/A")
                volume = dd.get("volume", "N/A")
                if volume:
                    vol_str = f"{float(volume)/1e8:.2f}亿"
                else:
                    vol_str = "N/A"
                print(f"  {name}({code}): {price} | {change_amount} ({change}%) | 成交 {vol_str}")
            elif isinstance(d, dict):
                price = d.get("price", "N/A")
                change = d.get("change_ratio", "N/A")
                print(f"  {name}({code}): {price} | {change}%")
        except Exception as e:
            print(f"  FAIL {name}({code}): {e}")

    # -- 3. 个股实时行情 --
    print("\n[3] 个股实时行情")
    stocks = [
        ("600519.SS", "贵州茅台"),
        ("000001.SZ", "平安银行"),
        ("300750.SZ", "宁德时代"),
    ]
    for code, name in stocks:
        try:
            d = api(f"real/ssjy/{code}")
            if isinstance(d, dict) and "data" in d:
                dd = d["data"]
                price = dd.get("price", "N/A")
                change = dd.get("change_ratio", "N/A")
                pe = dd.get("pe_ratio", "N/A")
                mcap = dd.get("market_cap", "N/A")
                if mcap:
                    mcap_str = f"{float(mcap)/1e8:.2f}亿"
                else:
                    mcap_str = "N/A"
                print(f"  {name}({code}): {price} | {change}% | PE={pe} | 市值={mcap_str}")
        except Exception as e:
            print(f"  FAIL {name}({code}): {e}")

    # -- 4. 公司基本信息 --
    print("\n[4] 公司基本信息 - 贵州茅台")
    try:
        d = api("gs/gsjj/600519.SS")
        if isinstance(d, dict) and "data" in d:
            dd = d["data"]
            print(f"  代码: {dd.get('dm', dd.get('code', 'N/A'))}")
            print(f"  名称: {dd.get('mc', dd.get('name', 'N/A'))}")
            print(f"  行业: {dd.get('industry', 'N/A')}")
            print(f"  主营业务: {dd.get('main_business', 'N/A')}")
            print(f"  总股本: {dd.get('total_shares', 'N/A')}")
            print(f"  流通股本: {dd.get('float_shares', 'N/A')}")
            print(f"  可用字段: {list(dd.keys())}")
        elif isinstance(d, dict):
            print(f"  字段: {list(d.keys())}")
    except Exception as e:
        print(f"  FAIL - {e}")

    # -- 5. 财务指标 --
    print("\n[5] 财务指标 - 贵州茅台")
    try:
        d = api("gs/cwzb/600519.SS")
        if isinstance(d, dict):
            print(f"  返回字段: {list(d.keys())}")
            if "data" in d:
                for k, v in d["data"].items():
                    print(f"    {k}: {v}")
            else:
                for k, v in list(d.items())[:10]:
                    print(f"    {k}: {str(v)[:100]}")
    except Exception as e:
        print(f"  FAIL - {e}")

    # -- 6. 概念板块列表 --
    print("\n[6] 概念板块列表")
    try:
        data = api("list/sectors")
        if isinstance(data, list):
            print(f"  OK - 共 {len(data)} 个概念板块")
            for s in data[:5]:
                print(f"    {s.get('dm', 'N/A')} | {s.get('mc', 'N/A')} | {s.get('jys', 'N/A')}")
        elif isinstance(data, dict):
            print(f"  字段: {list(data.keys())}")
    except Exception as e:
        print(f"  FAIL - {e}")

    # -- 7. 涨停股池（今日）--
    print("\n[7] 涨停股池 - 今日")
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        d = api(f"pool/ztgc/{today}")
        if isinstance(d, dict) and "data" in d:
            pool = d["data"]
            if isinstance(pool, list):
                print(f"  OK - 今日涨停股共 {len(pool)} 只")
                for s in pool[:5]:
                    print(f"    {s.get('dm', 'N/A')} | {s.get('mc', 'N/A')} | {s.get('change_ratio', 'N/A')}%")
        elif isinstance(d, list):
            print(f"  OK - 涨停股 {len(d)} 只")
        else:
            print(f"  返回: {str(d)[:200]}")
    except Exception as e:
        print(f"  FAIL - {e}")

    print("\n" + "=" * 60)
    print("测试完成!")
    print("=" * 60)


if __name__ == "__main__":
    test_all()
