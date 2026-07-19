#!/usr/bin/env python3
import os
import sys
import yfinance as yf
import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")

# Default watchlist fallback if Supabase is offline/not configured
DEFAULT_WATCHLIST = ["RKLB", "VRT", "JCI", "OKLO", "IREN", "EOSE", "KEEL", "NVDA", "AVGO", "ASTS", "PLTR"]

def get_watchlist():
    """Fetch tickers from Supabase or fallback to DEFAULT_WATCHLIST."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("⚠️ Supabase credentials not found in .env. Using default local watchlist.")
        return DEFAULT_WATCHLIST
    
    url = f"{SUPABASE_URL}/rest/v1/stocks?select=ticker"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return [item['ticker'] for item in response.json()]
        else:
            print(f"⚠️ Failed to load watchlist from Supabase: {response.text}. Using defaults.")
            return DEFAULT_WATCHLIST
    except Exception as e:
        print(f"⚠️ Error connecting to Supabase: {str(e)}. Using defaults.")
        return DEFAULT_WATCHLIST

def check_ticker_signals(ticker):
    """Fetch data and evaluate EMA 10M crossings/approach signals."""
    try:
        df = yf.download(ticker, period="2y", interval="1mo", progress=False)
        if len(df) < 11:
            return None
        
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df['EMA_10M'] = df['Close'].ewm(span=10, adjust=False).mean()

        close = float(df['Close'].iloc[-1])
        ema_10m = float(df['EMA_10M'].iloc[-1])
        prev_close = float(df['Close'].iloc[-2])
        prev_ema_10m = float(df['EMA_10M'].iloc[-2])

        # Signal Calculations
        # 1. Crossed Above EMA 10M
        crossed_above = (prev_close <= prev_ema_10m) and (close > ema_10m)
        # 2. Crossed Below EMA 10M
        crossed_below = (prev_close >= prev_ema_10m) and (close < ema_10m)
        # 3. Near Support (within 3% above EMA 10M)
        diff_pct = ((close - ema_10m) / ema_10m) * 100
        near_support = 0.0 < diff_pct <= 3.0

        if crossed_above:
            return "🟩 BUY SIGNAL (ราคาตัดขึ้นยืนเหนือ EMA 10M)", diff_pct, close, ema_10m
        elif crossed_below:
            return "🟥 SELL SIGNAL (ราคาหลุดเส้น EMA 10M - STOP LOSS)", diff_pct, close, ema_10m
        elif near_support:
            return "🟨 WATCH ZONE (ราคาลงมาใกล้แนวรับเส้น EMA 10M)", diff_pct, close, ema_10m
        
        return None
    except Exception as e:
        print(f"❌ Error checking {ticker}: {str(e)}")
        return None

def write_alerts_markdown(alerts):
    """Write the detected alerts to docs/knowledge/05_watchlists/alerts.md."""
    output_path = "docs/knowledge/05_watchlists/alerts.md"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 🚨 รายงานแจ้งเตือนสัญญาณเทรดรายเดือน (Kan's Stock Monitor Alerts)\n")
        f.write(f"*อัปเดตล่าสุด ณ วันที่: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        f.write("ระบบทำการตรวจสอบราคาหุ้นรายเดือนเมื่อเทียบกับเส้น EMA 10M เพื่อหาจุดซื้อ/ขาย/เฝ้าระวังอัตโนมัติ:\n\n")
        
        if not alerts:
            f.write("> [!NOTE]\n")
            f.write("> **ยอดเยี่ยม!** ขณะนี้ไม่มีหุ้นใน Watchlist ตัวใดมีสัญญาณเปลี่ยนแปลง หรือส่งสัญญาณอันตราย (หลุดแนวรับ)\n")
        else:
            f.write("| Ticker | สัญญาณเตือน (Signal Alert) | ราคาปัจจุบัน | เส้น EMA 10M | ส่วนต่าง % |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- |\n")
            for a in alerts:
                f.write(f"| **{a['Ticker']}** | {a['Signal']} | ${a['Price']:.2f} | ${a['EMA']:.2f} | {a['Diff']:.1f}% |\n")
                
            f.write("\n\n")
            f.write("> [!IMPORTANT] **คำอธิบายการตัดสินใจ:**\n")
            f.write("> *   **BUY SIGNAL:** ราคาปิดสิ้นเดือนผ่านเหนือ EMA 10M คอนเฟิร์มจังหวะตั้งต้นขาขึ้นรอบใหญ่\n")
            f.write("> *   **SELL SIGNAL:** ราคาหลุดต่ำกว่า EMA 10M เป็นจุดที่ต้องพิจารณาตัดขาดทุนหรือลดขนาดพอร์ตทันที\n")
            f.write("> *   **WATCH ZONE:** ราคาถอยลงมาใกล้เส้น EMA 10M ในระยะ 0-3% ซึ่งเป็นจุดพิจารณาสะสมของถูกกรณีแนวโน้มยังดีอยู่\n")

    print(f"💾 Alerts successfully written to: {output_path}")

def main():
    watchlist = get_watchlist()
    print(f"🔍 Monitoring {len(watchlist)} stocks for active monthly signals...")
    
    alerts = []
    for ticker in watchlist:
        res = check_ticker_signals(ticker)
        if res:
            signal, diff_pct, close, ema_10m = res
            alerts.append({
                "Ticker": ticker,
                "Signal": signal,
                "Price": close,
                "EMA": ema_10m,
                "Diff": diff_pct
            })
            print(f"🚨 ALERT for {ticker}: {signal} (Diff: {diff_pct:.1f}%)")

    # Write report
    write_alerts_markdown(alerts)
    
    if not alerts:
        print("✅ No active signals detected for any watchlisted stocks.")
    else:
        print(f"🎉 Detected {len(alerts)} active signals. Report generated.")

if __name__ == "__main__":
    main()
