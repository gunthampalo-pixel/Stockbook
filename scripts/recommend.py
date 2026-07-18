#!/usr/bin/env python3
import sys
import argparse
import yfinance as yf
import pandas as pd
from tabulate import tabulate

# A curated universe of high-growth tech, infrastructure, and defensive compounders to scan
DEFAULT_UNIVERSE = [
    # AI Infra (Power, Cooling, Data Center)
    "VRT", "JCI", "OKLO", "IREN", "EOSE", "GE", "CEG", "VST",
    # Chips, Hardware, Equipment & EDA
    "NVDA", "AVGO", "MRVL", "CDNS", "SNPS", "AMAT", "LRCX", "KLAC", "TSMC", "ASML", "ARM", "ALAB",
    # Connectivity, Space Tech & Defense
    "ASTS", "RKLB", "PLTR", "AVAV", "KTOS", "LMT", "NOC",
    # Software & Cloud
    "MSFT", "AMZN", "GOOGL", "META", "NFLX", "CRWD", "NET", "DDOG", "NOW"
]

def parse_args():
    parser = argparse.ArgumentParser(description="Scan and recommend stocks based on Kan's Playbook")
    parser.add_argument("--tickers", type=str, help="Comma-separated list of custom tickers to scan")
    parser.add_argument("--min-growth", type=float, default=15.0, help="Minimum annual revenue growth % (default: 15.0)")
    return parser.parse_args()

def analyze_stock(ticker, min_growth):
    try:
        # 1. Fetch financials
        stock = yf.Ticker(ticker)
        income_stmt = stock.income_stmt
        if income_stmt.empty:
            return None

        # Calculate Revenue Growth YoY (last 3-4 years)
        revenue_row = None
        for idx in ['Total Revenue', 'Revenue', 'TotalRevenue']:
            if idx in income_stmt.index:
                revenue_row = income_stmt.loc[idx]
                break
        
        if revenue_row is None:
            return None

        revenues = [float(val) for val in revenue_row.values if not pd.isna(val)]
        # Sort in chronological order (oldest first)
        revenues = list(reversed(revenues))
        
        growths = []
        for i in range(1, len(revenues)):
            prev = revenues[i-1]
            curr = revenues[i]
            if prev > 0:
                growths.append(((curr - prev) / prev) * 100)
        
        avg_growth = sum(growths) / len(growths) if growths else 0.0

        # 2. Fetch monthly technical data
        df = yf.download(ticker, period="10y", interval="1mo", progress=False)
        if len(df) < 15:
            return None

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        # Calculate Indicators
        df['EMA_10M'] = df['Close'].ewm(span=10, adjust=False).mean()
        
        # MACD
        df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

        # RSI
        delta = df['Close'].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(window=14, min_periods=1).mean()
        avg_loss = loss.rolling(window=14, min_periods=1).mean()
        rs = avg_gain / (avg_loss + 1e-10)
        df['RSI'] = 100 - (100 / (1 + rs))

        # Latest values
        close = float(df['Close'].iloc[-1])
        ema_10m = float(df['EMA_10M'].iloc[-1])
        prev_close = float(df['Close'].iloc[-2])
        prev_ema_10m = float(df['EMA_10M'].iloc[-2])
        macd = float(df['MACD'].iloc[-1])
        signal = float(df['Signal'].iloc[-1])
        rsi = float(df['RSI'].iloc[-1])

        # Determine Technical Status
        above_ema = close > ema_10m
        just_crossed_above = (prev_close <= prev_ema_10m) and (close > ema_10m)
        macd_bullish = macd > signal

        # Categorize
        fundamental_pass = avg_growth >= min_growth
        
        if not fundamental_pass:
            status = "❌ Fail (Low Growth)"
        elif rsi > 75:
            status = "🔥 Too Hot (RSI Overheated)"
        elif just_crossed_above and macd_bullish:
            status = "🌟 Buy Candidate (Just Crossed above EMA 10M)"
        elif above_ema and macd_bullish:
            status = "📈 Hold (Raining Trend)"
        elif above_ema and not macd_bullish:
            status = "⚠️ Hold (MACD Bearish)"
        else:
            status = "⏳ Wait (Below EMA 10M)"

        return {
            "Ticker": ticker,
            "Price": round(close, 2),
            "EMA 10M": round(ema_10m, 2),
            "Diff %": round(((close - ema_10m) / ema_10m) * 100, 1),
            "Avg Growth %": f"{avg_growth:.1f}%",
            "RSI 14M": round(rsi, 1),
            "MACD Status": "Bullish" if macd_bullish else "Bearish",
            "Recommendation": status
        }
    except Exception as e:
        return None

def main():
    args = parse_args()
    
    if args.tickers:
        universe = [t.strip().upper() for t in args.tickers.split(",")]
    else:
        universe = DEFAULT_UNIVERSE

    print(f"🔎 Scanning {len(universe)} stocks using Kan's Core Playbook...")
    print(f"Criteria: Min Avg Growth: {args.min_growth}%, Technicals: Monthly close above/crossing EMA 10M")
    print("-" * 80)

    results = []
    for ticker in universe:
        res = analyze_stock(ticker, args.min_growth)
        if res:
            results.append(res)
            print(f"✅ Scanned {ticker:6} -> {res['Recommendation']}")

    # Sort results by recommendation priority
    # 1. Buy Candidate, 2. Hold, 3. Wait, 4. Too Hot, 5. Fail
    def sort_key(x):
        rec = x['Recommendation']
        if "Buy Candidate" in rec: return 0
        if "Hold (Raining" in rec: return 1
        if "Hold" in rec: return 2
        if "Wait" in rec: return 3
        if "Too Hot" in rec: return 4
        return 5

    results = sorted(results, key=sort_key)

    print("\n" + "="*90)
    print("📈 KAN'S STOCK RECOMMENDATION SCANNER REPORT")
    print("="*90)
    
    headers = ["Ticker", "Price", "EMA 10M", "Diff %", "Avg Growth", "RSI 14M", "MACD", "Status"]
    data_rows = [
        [
            r["Ticker"],
            f"${r['Price']:,.2f}",
            f"${r['EMA 10M']:,.2f}",
            f"{r['Diff %']}%",
            r["Avg Growth %"],
            r["RSI 14M"],
            r["MACD Status"],
            r["Recommendation"]
        ]
        for r in results
    ]
    
    print(tabulate(data_rows, headers=headers, tablefmt="grid"))
    print("="*90)
    print("🌟 Buy Candidate = เพิ่งตัดขึ้นเหนือเส้น EMA 10M ในระดับเดือน + MACD ขาขึ้น + งบเติบโตเฉลี่ย 15%+")
    print("⏳ Wait          = หุ้นเติบโตดีแต่ราคาปรับฐานอยู่ต่ำกว่าเส้น EMA 10M ควรรอให้กราฟยืนยันก่อนซื้อ")
    print("🔥 Too Hot       = หุ้นดีแต่ราคาขึ้นร้อนแรงเกินไป (RSI > 75) ควรหลีกเลี่ยงหรือรอให้ราคาย่อลงมาก่อน")

if __name__ == "__main__":
    main()
