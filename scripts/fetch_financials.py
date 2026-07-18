#!/usr/bin/env python3
import os
import sys
import json
import yfinance as yf
import pandas as pd
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: Please configure SUPABASE_URL and SUPABASE_KEY/SUPABASE_SERVICE_ROLE_KEY in your .env file.")
    sys.exit(1)

# Supabase PostgREST API headers
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates"
}

def get_supabase_tickers():
    """Fetch all active tickers from Supabase database."""
    url = f"{SUPABASE_URL}/rest/v1/stocks?select=ticker"
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return [item['ticker'] for item in response.json()]
        else:
            print(f"⚠️ Failed to fetch tickers from Supabase: {response.text}")
            return []
    except Exception as e:
        print(f"⚠️ Error connecting to Supabase: {str(e)}")
        return []

def fetch_stock_financials(ticker):
    """Download past 4-5 years of annual financials from Yahoo Finance."""
    print(f"📥 Fetching financials for {ticker}...")
    try:
        stock = yf.Ticker(ticker)
        
        # Fetch annual financials statements
        income_stmt = stock.income_stmt
        cash_flow = stock.cashflow
        
        if income_stmt.empty:
            print(f"⚠️ No financial data found for {ticker}")
            return None

        # Clean column names (dates)
        years = []
        for col in income_stmt.columns:
            if isinstance(col, pd.Timestamp):
                years.append(col.year)
            else:
                try:
                    years.append(pd.to_datetime(col).year)
                except:
                    years.append(str(col))

        # Map metrics
        # Index names in yfinance can vary: "Total Revenue" vs "Revenue"
        revenue_row = None
        for idx in ['Total Revenue', 'Revenue', 'TotalRevenue']:
            if idx in income_stmt.index:
                revenue_row = income_stmt.loc[idx]
                break
        
        net_income_row = None
        for idx in ['Net Income', 'NetIncome', 'Net Income Common Stockholders']:
            if idx in income_stmt.index:
                net_income_row = income_stmt.loc[idx]
                break

        ocf_row = None
        if not cash_flow.empty:
            for idx in ['Operating Cash Flow', 'Cash Flow From Operating Activities', 'OperatingCashFlow']:
                if idx in cash_flow.index:
                    ocf_row = cash_flow.loc[idx]
                    break

        financials_list = []
        
        # Construct the records
        for i, year in enumerate(years):
            rev = float(revenue_row.iloc[i]) if revenue_row is not None and not pd.isna(revenue_row.iloc[i]) else 0.0
            profit = float(net_income_row.iloc[i]) if net_income_row is not None and not pd.isna(net_income_row.iloc[i]) else 0.0
            ocf = float(ocf_row.iloc[i]) if ocf_row is not None and not pd.isna(ocf_row.iloc[i]) else 0.0

            financials_list.append({
                "year": int(year),
                "revenue": rev,
                "profit": profit,
                "operating_cash_flow": ocf,
                "growth": "0.0%" # placeholder, calculated next
            })

        # Sort years in ascending order to compute growth correctly
        financials_list = sorted(financials_list, key=lambda x: x['year'])

        # Calculate Revenue Growth YoY
        for idx in range(len(financials_list)):
            if idx == 0:
                financials_list[idx]['growth'] = "N/A"
            else:
                prev_rev = financials_list[idx-1]['revenue']
                curr_rev = financials_list[idx]['revenue']
                if prev_rev > 0:
                    growth_pct = ((curr_rev - prev_rev) / prev_rev) * 100
                    financials_list[idx]['growth'] = f"{growth_pct:.1f}%"
                else:
                    financials_list[idx]['growth'] = "0.0%"

        return financials_list
    except Exception as e:
        print(f"❌ Error fetching {ticker}: {str(e)}")
        return None

def update_supabase_financials(ticker, financials):
    """Update the financials field in Supabase for the given ticker."""
    url = f"{SUPABASE_URL}/rest/v1/stocks?ticker=eq.{ticker}"
    
    # Supabase JSONB column format
    payload = {
        "financials": financials
    }
    
    try:
        response = requests.patch(url, headers=HEADERS, data=json.dumps(payload))
        if response.status_code in [200, 204]:
            print(f"✅ Supabase updated successfully for {ticker}.")
            return True
        else:
            print(f"❌ Failed to update Supabase for {ticker}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error patching to Supabase: {str(e)}")
        return False

def main():
    # 1. Fetch active tickers from Supabase
    tickers = get_supabase_tickers()
    if not tickers:
        print("⚠️ No tickers found in Supabase. Seeding might be needed first.")
        # Fallback to defaults if empty
        tickers = ["VRT", "JCI", "OKLO", "IREN", "EOSE", "KEEL", "NVDA", "AVGO", "MRVL", "CDNS", "AMAT"]
    
    print(f"📋 Found {len(tickers)} tickers to update.")
    
    # 2. Loop and update
    success_count = 0
    for ticker in tickers:
        financials = fetch_stock_financials(ticker)
        if financials:
            success = update_supabase_financials(ticker, financials)
            if success:
                success_count += 1
                
    print(f"\n🎉 Done! Successfully updated financials for {success_count}/{len(tickers)} stocks in Supabase.")

if __name__ == "__main__":
    main()
