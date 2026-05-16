# -*- coding: utf-8 -*-
"""
科技指数每日早报 - morning_report.py
数据源:
  - 智兔API: A股主要指数（上证/深证/创业板/科创50/沪深300等，/hz/real/ssjy/接口）
  - akshare + 新浪财经: 美股(SOX/纳斯达克)、德/日/韩/港股（全球指数）
  - akshare + 东方财富: A股指数（智兔备用）
覆盖: 上证/深证/创业板/科创50/沪深300、纳斯达克综合/100、SOX、DAX40、日经225、KOSPI、恒生指数、恒生科技
"""

import sys, os, subprocess, warnings, requests
from datetime import datetime, timedelta

warnings.filterwarnings('ignore')

import akshare as ak

# ─── 邮件脚本配置 ─────────────────────────────────────────
MAIL_SCRIPT = r"C:\Users\wxd\.workbuddy\skills\qq-email\scripts\mail.py"
MAIL_TO = "63224457@qq.com"

# ─── 智兔API配置 ─────────────────────────────────────────
ZHITU_TOKEN = "4BDA45E5-F103-4FE4-8C91-530D44F68C67"
ZHITU_BASE = "https://api.zhituapi.com"


# ─── A股指数（智兔 via /hz/real/ssjy/，主数据源）─────────

def get_ashare_indices_zhitu():
    """通过智兔获取A股指数实时行情（免费版可用）"""
    # 代码->标准名称映射
    code_to_name = {
        "000001.SH": "上证指数",
        "399001.SZ": "深证成指",
        "399006.SZ": "创业板指",
        "000688.SH": "科创50",
        "000300.SH": "沪深300",
        "000016.SH": "上证50",
        "000905.SH": "中证500",
        "000852.SH": "中证1000",
    }
    result = {}
    try:
        for code, std_name in code_to_name.items():
            url = f"{ZHITU_BASE}/hz/real/ssjy/{code}"
            r = requests.get(url, params={"token": ZHITU_TOKEN}, timeout=5)
            d = r.json()
            if "error" not in d:
                p = d.get("p")
                pc = d.get("pc")
                cje = d.get("cje", 0)
                if p is not None and p != "":
                    # 用标准名称存储，忽略API返回的乱码名称
                    result[std_name] = {
                        "close": float(p),
                        "chg_pct": float(pc) if pc else 0.0,
                        "cje": float(cje) if cje else 0.0,
                    }
        return result
    except Exception as e:
        print(f"[智兔A股指数错误] {e}")
        return {}

def get_ashare_indices_em():
    """通过东方财富获取A股指数实时行情"""
    try:
        df = ak.stock_zh_index_spot_em()
        if df is None or df.empty:
            return {}
        # 列名: 代码, 名称, 最新价, 涨跌幅, 涨跌额, 成交量(手), 成交额, 振幅...
        # 代码列可能是数字或字符串
        df.iloc[:, 0] = df.iloc[:, 0].astype(str).str.zfill(6)
        result = {}
        targets = {
            "000001": "\u4e0a\u8bc1\u6307\u6570",
            "399001": "\u6df1\u8bc1\u6210\u6307",
            "399006": "\u521b\u4e1a\u677f\u6307",
            "000688": "\u79d1\u521b50",
            "000300": "沪深300",
            "000016": "上证50",
            "000905": "中证500",
            "000852": "中证1000",
        }
        for code, name in targets.items():
            row = df[df.iloc[:, 0] == code]
            if not row.empty:
                close = float(row.iloc[0, 3]) if row.iloc[0, 3] not in ["-", ""] else None
                chg_pct = float(row.iloc[0, 4]) if row.iloc[0, 4] not in ["-", ""] else 0.0
                chg_amt = float(row.iloc[0, 5]) if len(row.columns) > 5 and row.iloc[0, 5] not in ["-", ""] else 0.0
                vol = row.iloc[0, 6] if len(row.columns) > 6 else None
                update_time = str(row.iloc[0, 31]) if len(row.columns) > 31 and row.iloc[0, 31] not in ["-", ""] else ""
                if close:
                    result[name] = {
                        "close": close,
                        "chg_pct": chg_pct,
                        "chg_amt": chg_amt,
                        "volume": vol,
                        "update_time": update_time,
                    }
        return result
    except Exception as e:
        print(f"[A股\u6307\u6570\u9519\u8bef] {e}")
        return {}


# ─── A股指数（新浪 via akshare - 备用）─────────────────────

def get_ashare_index_sina(symbol_cn):
    """通过新浪获取A股指数历史数据"""
    try:
        df = ak.index_zh_a_hist(symbol=symbol_cn, period="daily",
                                start_date=(datetime.now() - timedelta(days=5)).strftime("%Y%m%d"),
                                end_date=datetime.now().strftime("%Y%m%d"))
        if df is None or df.empty:
            return None
        last = df.iloc[-1]
        prev = df.iloc[-2]
        close = float(last.iloc[4])
        prev_close = float(prev.iloc[4])
        chg_pct = (close - prev_close) / prev_close * 100
        date = str(last.iloc[0])[:10]
        return {"close": close, "chg_pct": chg_pct, "date": date}
    except Exception as e:
        print(f"[A股\u6307\u6570 {symbol_cn} \u9519\u8bef] {e}")
        return None


# ─── 美股数据（新浪+akshare） ─────────────────────────────

def get_us_index_sina(symbol):
    """新浪美股指数: .IXIC .NDX .INX .DJI"""
    try:
        df = ak.index_us_stock_sina(symbol=symbol)
        if df is None or len(df) < 2:
            return None
        last = df.iloc[-1]
        prev = df.iloc[-2]
        close = float(last.iloc[4])
        prev_close = float(prev.iloc[4])
        chg_pct = (close - prev_close) / prev_close * 100
        date = str(last.iloc[0])[:10]
        return {"close": close, "chg_pct": chg_pct, "date": date}
    except Exception as e:
        print(f"[\u7f8e\u80a1\u9519\u8bef] {symbol}: {e}")
        return None


def get_global_index_sina(symbol_cn):
    """新浪全球指数"""
    try:
        df = ak.index_global_hist_sina(symbol=symbol_cn)
        if df is None or len(df) < 2:
            return None
        last = df.iloc[-1]
        prev = df.iloc[-2]
        close = float(last.iloc[4])
        prev_close = float(prev.iloc[4])
        chg_pct = (close - prev_close) / prev_close * 100
        date = str(last.iloc[0])[:10]
        return {"close": close, "chg_pct": chg_pct, "date": date}
    except Exception as e:
        print(f"[\u5168\u7403\u6307\u6570 {symbol_cn} \u9519\u8bef]: {e}")
        return None


def get_hk_index_sina(symbol):
    """新浪港股指数"""
    try:
        df = ak.stock_hk_index_spot_sina()
        if df is None or df.empty:
            return None
        row = df[df["\u4ee3\u7801"] == symbol]
        if row.empty:
            return None
        close = float(row.iloc[0]["\u6700\u65b0\u4ef7"])
        chg_pct = float(row.iloc[0]["\u6da8\u8dcc\u5e45"])
        return {"close": close, "chg_pct": chg_pct, "date": datetime.now().strftime("%Y-%m-%d")}
    except Exception as e:
        print(f"[\u6e2f\u80a1\u9519\u8bef] {symbol}: {e}")
        return None


def get_sox():
    """费城半导体指数 SOX"""
    try:
        df = ak.macro_global_sox_index()
        if df is None or df.empty:
            return None
        last = df.iloc[-1]
        prev = df.iloc[-2]
        close = float(last.iloc[1])
        prev_close = float(prev.iloc[1])
        chg_pct = (close - prev_close) / prev_close * 100
        date = str(last.iloc[0])[:10]
        return {"close": close, "chg_pct": chg_pct, "date": date}
    except Exception as e:
        print(f"[SOX\u9519\u8bef] {e}")
        return None


# ─── 格式化 ──────────────────────────────────────────────

def fmt_index(name, data, extra=""):
    """格式化指数行"""
    if data is None:
        return f"  {name}  --  \u6682\u7f3a\u6570\u636e"
    pct = data["chg_pct"]
    sign = "+" if pct >= 0 else ""
    cls = "[+]" if pct >= 0 else "[-]"
    extra_str = f"  {extra}" if extra else ""
    return f"  {cls} {name}  {data['close']:,.2f}  {sign}{pct:.2f}%{extra_str}"


def fmt_money(n):
    """格式化金额"""
    if not n:
        return "N/A"
    if n >= 1e12:
        return f"{n/1e12:.2f}\u4e07\u4ebf"
    elif n >= 1e8:
        return f"{n/1e8:.2f}\u4ebf"
    elif n >= 1e4:
        return f"{n/1e4:.2f}\u4e07"
    return str(n)


# ─── 主程序 ────────────────────────────────────────────────

def main():
    now = datetime.now()
    today_str = f"{now.year}\u5e74{now.month}\u6708{now.day}\u65e5"
    weekday_map = ["\u5468\u4e00", "\u5468\u4e8c", "\u5468\u4e09", "\u5468\u56db",
                   "\u5468\u4e94", "\u5468\u516d", "\u5468\u65e5"]
    weekday_str = weekday_map[now.weekday()]
    gen_time = f"{now.hour:02d}:{now.minute:02d}"
    yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")

    print(">> \u83b7\u53d6\u6570\u636e\u4e2d...")

    # ── A股指数（智兔主数据源，东方财富备用）──
    print("  [智兔] \u83b7\u53d6A股\u6307\u6570...")
    ashare = get_ashare_indices_zhitu()
    if not ashare:
        print("  [东方财富] \u667a\u5154\u5931\u6548\uff0c\u5207\u6362\u5907\u7528...")
        ashare = get_ashare_indices_em()

    # ── 美股（新浪+akshare） ──
    print("  [\u65b0\u6d6a] \u83b7\u53d6\u7f8e\u80a1\u6570\u636e...")
    ixic = get_us_index_sina(".IXIC")
    ndx  = get_us_index_sina(".NDX")
    sox  = get_sox()

    # ── 德/日/韩/港（新浪+akshare） ──
    print("  [\u65b0\u6d6a] \u83b7\u53d6\u5168\u7403\u6570\u636e...")
    dax  = get_global_index_sina("\u5fb7\u56fdDAX 30\u79cd\u80a1\u4ef7\u6307\u6570")
    n225 = get_global_index_sina("\u65e5\u7ecf225\u6307\u6570")
    ks11 = get_global_index_sina("\u9996\u5c14\u7efc\u5408\u6307\u6570")
    hsi   = get_hk_index_sina("HSI")
    hstech = get_hk_index_sina("HSTECH")

    # ── 数据日期 ──
    us_date = (ixic or ndx or sox or {}).get("date", yesterday)
    de_date = (dax or {}).get("date", yesterday)
    jp_date = (n225 or {}).get("date", yesterday)
    kr_date = (ks11 or {}).get("date", yesterday)
    hk_date = now.strftime("%Y-%m-%d")
    cn_date_str = ""
    for name in ["\u4e0a\u8bc1\u6307\u6570", "\u6df1\u8bc1\u6210\u6307"]:
        d = ashare.get(name)
        if d and d.get("update_time"):
            cn_date_str = d["update_time"][:10]
            break
    if not cn_date_str:
        cn_date_str = yesterday

    # ── 组装早报 ──────────────────────────────────────────
    lines = []
    lines.append("=" * 55)
    lines.append("  \u79d1\u6280\u6307\u6570\u6bcf\u65e5\u65e9\u62a5")
    lines.append(f"  {today_str} {weekday_str}  \u751f\u6210\u65f6\u95f4 {gen_time}")
    lines.append("=" * 55)

    # ── A股 ──
    lines.append("")
    lines.append(f"[\u4e2d\u56fd A\u80a1] \u4e0a\u6d77/\u6df1\u5733\u4ea4\u6240  \u6536\u76d8\u65f6\u95f4 15:00")
    lines.append(f"  \u6570\u636e\u65e5\u671f: {cn_date_str}")
    priority_a = ["\u4e0a\u8bc1\u6307\u6570", "\u6df1\u8bc1\u6210\u6307", "\u521b\u4e1a\u677f\u6307",
                  "\u79d1\u521b50", "沪深300", "上证50", "中证500", "中证1000"]
    for name in priority_a:
        d = ashare.get(name)
        if d:
            # 成交额显示（如果有的话）
            extra = ""
            if d.get("cje"):
                extra = "  \u6210\u4ea4" + fmt_money(d["cje"])
            lines.append(fmt_index(name, d, extra))
        else:
            lines.append(f"  --- {name}  \u6682\u7f3a")

    # ── 美股 ──
    lines.append("")
    lines.append(f"[\u7f8e\u56fd US] \u6536\u76d8\u65f6\u95f4 \u5317\u4eac\u65f6\u95f4 04:00(\u6b21\u65e5)")
    lines.append(f"  \u6570\u636e\u65e5\u671f: {us_date}")
    lines.append(fmt_index("\u7eb3\u65af\u8fbe\u514b\u7efc\u5408 .IXIC", ixic))
    lines.append(fmt_index("\u7eb3\u65af\u8fbe\u514b100 .NDX", ndx))
    lines.append(fmt_index("\u8d39\u57ce\u534a\u5bfc\u4f53 SOX", sox))

    # ── 德国 ──
    lines.append("")
    lines.append(f"[\u5fb7\u56fd DE] \u6536\u76d8\u65f6\u95f4 \u5317\u4eac\u65f6\u95f4 00:30(\u6b21\u65e5)")
    lines.append(f"  \u6570\u636e\u65e5\u671f: {de_date}")
    lines.append(fmt_index("DAX40", dax))

    # ── 日本 ──
    lines.append("")
    lines.append(f"[\u65e5\u672c JP] \u6536\u76d8\u65f6\u95f4 \u5317\u4eac\u65f6\u95f4 15:00")
    lines.append(f"  \u6570\u636e\u65e5\u671f: {jp_date}")
    lines.append(fmt_index("\u65e5\u7ecf225", n225))

    # ── 韩国 ──
    lines.append("")
    lines.append(f"[\u97e9\u56fd KR] \u6536\u76d8\u65f6\u95f4 \u5317\u4eac\u65f6\u95f4 15:00")
    lines.append(f"  \u6570\u636e\u65e5\u671f: {kr_date}")
    lines.append(fmt_index("KOSPI", ks11))

    # ── 港股 ──
    lines.append("")
    lines.append(f"[\u6e2f\u80a1 HK] \u6536\u76d8\u65f6\u95f4 \u5317\u4eac\u65f6\u95f4 16:00")
    lines.append(f"  \u6570\u636e\u65e5\u671f: {hk_date}")
    lines.append(fmt_index("\u6052\u751f\u6307\u6570 HSI", hsi))
    lines.append(fmt_index("\u6052\u751f\u79d1\u6280 HSTECH", hstech))

    # ── 今日小结 ──
    lines.append("")
    lines.append("-" * 55)
    lines.append("  [\u4eca\u65e5\u5c0f\u7ed3]")
    all_data = [
        ("\u4e0a\u8bc1\u6307\u6570", ashare.get("\u4e0a\u8bc1\u6307\u6570")),
        ("\u6df1\u8bc1\u6210\u6307", ashare.get("\u6df1\u8bc1\u6210\u6307")),
        ("\u521b\u4e1a\u677f\u6307", ashare.get("\u521b\u4e1a\u677f\u6307")),
        ("\u79d1\u521b50", ashare.get("\u79d1\u521b50")),
        ("沪深300", ashare.get("沪深300")),
        ("\u7eb3\u65af\u8fbe\u514b\u7efc\u5408", ixic),
        ("\u7eb3\u65af\u8fbe\u514b100", ndx),
        ("\u8d39\u57ce\u534a\u5bfc\u4f53", sox),
        ("DAX40", dax),
        ("\u65e5\u7ecf225", n225),
        ("KOSPI", ks11),
        ("\u6052\u751f\u6307\u6570", hsi),
        ("\u6052\u751f\u79d1\u6280", hstech),
    ]
    up_list   = [(n, d) for n, d in all_data if d and d["chg_pct"] >  0.3]
    down_list = [(n, d) for n, d in all_data if d and d["chg_pct"] < -0.3]
    flat_list = [(n, d) for n, d in all_data if d and abs(d["chg_pct"]) <= 0.3]
    miss_list = [n for n, d in all_data if d is None]

    if up_list:
        up_str = "\u3001".join([f"{n}({d['chg_pct']:+.2f}%)" for n, d in up_list])
        lines.append(f"  \u4e0a\u6da8 {len(up_list)}\u4e2a: {up_str}")
    if down_list:
        dn_str = "\u3001".join([f"{n}({d['chg_pct']:+.2f}%)" for n, d in down_list])
        lines.append(f"  \u4e0b\u8dcc {len(down_list)}\u4e2a: {dn_str}")
    if flat_list:
        fl_str = "\u3001".join([f"{n}({d['chg_pct']:+.2f}%)" for n, d in flat_list])
        lines.append(f"  \u6301\u5e73 {len(flat_list)}\u4e2a: {fl_str}")
    if miss_list:
        sep = "\u3001"
        lines.append(f"  \u6682\u7f3a: {sep.join(miss_list)}")

    total = len([d for _, d in all_data if d is not None])
    if total > 0:
        up_count = len(up_list)
        dn_count = len(down_list)
        if up_count >= dn_count * 2 and up_count >= 3:
            summary = f"\u5168\u7403\u79d1\u6280\u80a1\u5e02\u6574\u4f53\u504f\u5f3a\uff0c{up_count}\u4e2a\u6307\u6570\u4e0a\u6da8\u3002"
        elif dn_count >= up_count * 2 and dn_count >= 3:
            summary = f"\u5168\u7403\u79d1\u6280\u80a1\u5e02\u6574\u4f53\u504f\u5f31\uff0c{dn_count}\u4e2a\u6307\u6570\u4e0b\u8dcc\u3002"
        else:
            summary = f"\u5168\u7403\u79d1\u6280\u5e02\u8d8a\u52d5\u5206\u5316\uff0c\u4e0a{up_count}\u3001\u4e0b{dn_count}\u3001\u5e73{len(flat_list)}\u3002"
        lines.append(f"  >> {summary}")

    lines.append("-" * 55)
    lines.append(f"  \u6570\u636e\u6765\u6e90: \u65b0\u6d6a\u8d22\u7ecf+akshare(\u5168\u7403\u6307\u6570)\u3001\u667a\u5154API(A\u80a1\u6307\u6570)\u3001\u4e1c\u65b9\u8d22\u5bcc(\u5907\u7528)\u3002")

    report = "\n".join(lines)
    print("\n" + report)

    # ── 发送邮件 ──────────────────────────────────────────
    subject = f"\u79d1\u6280\u6307\u6570\u65e5\u62a5 {today_str} {weekday_str}"
    result = subprocess.run(
        ["py", "-X", "utf8", MAIL_SCRIPT, "send",
         "--to", MAIL_TO,
         "--subject", subject,
         "--body", report],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if result.returncode == 0:
        print("\n  >> \u90ae\u4ef6\u53d1\u9001\u6210\u529f\uff01")
    else:
        print(f"\n  >> \u90ae\u4ef6\u53d1\u9001\u5931\u8d25: {result.stderr[:200]}")


if __name__ == "__main__":
    main()
