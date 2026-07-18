#!/usr/bin/env python3
import sys
import argparse
import yfinance as yf
import pandas as pd
import numpy as np
from tabulate import tabulate

def parse_args():
    parser = argparse.ArgumentParser(description="Backtest Kan's EMA 10M Strategy")
    parser.add_argument("ticker", type=str, nargs="?", default="VRT", help="Stock ticker (e.g. VRT, NVDA, AAPL)")
    parser.add_argument("--capital", type=float, default=10000.0, help="Initial capital (default: 10000)")
    parser.add_argument("--period", type=str, default="15y", help="Historical period: 5y, 10y, 15y, 20y, max (default: 15y)")
    parser.add_argument("--confirm-macd", action="store_true", help="Require MACD to be bullish (MACD > Signal) to buy")
    return parser.parse_args()

def calculate_indicators(df):
    # Close price EMA 10 Month
    df['EMA_10M'] = df['Close'].ewm(span=10, adjust=False).mean()

    # MACD (12, 26, 9)
    df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['EMA_12'] - df['EMA_26']
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['MACD_Bullish'] = df['MACD'] > df['Signal']

    # RSI (14)
    delta = df['Close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=14, min_periods=1).mean()
    avg_loss = loss.rolling(window=14, min_periods=1).mean()
    rs = avg_gain / (avg_loss + 1e-10)
    df['RSI'] = 100 - (100 / (1 + rs))

    return df

def run_backtest(df, initial_capital, confirm_macd=False):
    cash = initial_capital
    position = 0.0
    trades = []
    equity_curve = []

    # Start loop from index where EMA 10M and other indicators are computed (at least 14 months data)
    start_idx = 14
    if len(df) <= start_idx:
        return None, None

    for i in range(start_idx, len(df)):
        date = df.index[i]
        close = df['Close'].iloc[i]
        ema_10m = df['EMA_10M'].iloc[i]
        prev_close = df['Close'].iloc[i-1]
        prev_ema_10m = df['EMA_10M'].iloc[i-1]
        
        macd_bullish = df['MACD_Bullish'].iloc[i]
        rsi = df['RSI'].iloc[i]

        # Current portfolio value
        portfolio_value = cash + (position * close)
        equity_curve.append({'Date': date, 'PortfolioValue': portfolio_value, 'Close': close})

        # Trading signals
        # Buy condition: Close crosses above EMA 10M
        crossed_above_ema = (prev_close <= prev_ema_10m) and (close > ema_10m)
        buy_signal = crossed_above_ema
        
        if confirm_macd:
            buy_signal = buy_signal and macd_bullish

        # Sell condition: Close crosses below EMA 10M
        sell_signal = (prev_close >= prev_ema_10m) and (close < ema_10m)

        # Execute Buy
        if buy_signal and position == 0.0:
            position = cash / close
            cash = 0.0
            trades.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Type': 'BUY',
                'Price': round(close, 2),
                'Shares': round(position, 4),
                'Cash': round(cash, 2),
                'Value': round(portfolio_value, 2),
                'RSI': round(rsi, 1)
            })

        # Execute Sell / Stop Loss
        elif sell_signal and position > 0.0:
            cash = position * close
            position = 0.0
            trades.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Type': 'SELL',
                'Price': round(close, 2),
                'Shares': 0.0,
                'Cash': round(cash, 2),
                'Value': round(cash, 2),
                'RSI': round(rsi, 1)
            })

    # Wrap up final value
    final_close = df['Close'].iloc[-1]
    final_val = cash + (position * final_close)
    
    return trades, final_val, equity_curve

def print_results(ticker, trades, initial_capital, final_val, buy_and_hold_return, total_periods_months):
    print("\n" + "="*70)
    print(f"📊 KAN'S MONTHLY STRATEGY BACKTEST RESULTS: {ticker.upper()}")
    print("="*70)
    print(f"Initial Capital   : ${initial_capital:,.2f}")
    print(f"Final Value       : ${final_val:,.2f}")
    
    strategy_return = ((final_val - initial_capital) / initial_capital) * 100
    print(f"Strategy Return   : {strategy_return:.2f}%")
    print(f"Buy & Hold Return : {buy_and_hold_return:.2f}%")
    
    # Calculate CAGR
    years = total_periods_months / 12.0
    strategy_cagr = (((final_val / initial_capital) ** (1 / years)) - 1) * 100 if final_val > 0 else -100
    print(f"Strategy CAGR     : {strategy_cagr:.2f}% per year (Period: {years:.1f} years)")

    print(f"Total Trades      : {len(trades)}")
    
    if len(trades) > 0:
        # Calculate Win Rate
        wins = 0
        total_closed = 0
        for i in range(len(trades)):
            if trades[i]['Type'] == 'SELL':
                total_closed += 1
                # Find matching buy
                buy_trade = trades[i-1]
                if trades[i]['Value'] > buy_trade['Value']:
                    wins += 1
        
        win_rate = (wins / total_closed * 100) if total_closed > 0 else 0
        print(f"Win Rate          : {win_rate:.2f}% ({wins}/{total_closed} profitable trades)")
    
    print("-"*70)
    print("📋 TRANSACTION LOG:")
    print("-"*70)
    if len(trades) == 0:
        print("No trades executed (Price stayed in one direction relative to EMA 10M).")
    else:
        headers = ['Date', 'Action', 'Price', 'Shares', 'Cash Balance', 'Portfolio Value', 'RSI']
        data = [[t['Date'], t['Type'], t['Price'], t['Shares'], t['Cash'], t['Value'], t['RSI']] for t in trades]
        print(tabulate(data, headers=headers, tablefmt='grid'))

def main():
    args = parse_args()
    ticker = args.ticker.upper()

    print(f"📥 Downloading monthly data for {ticker} (Period: {args.period})...")
    
    # Download monthly bars
    data = yf.download(ticker, period=args.period, interval="1mo", progress=False)
    
    if data.empty:
        print(f"❌ Error: No data found for ticker '{ticker}'")
        sys.exit(1)

    # Convert MultiIndex columns if present (yfinance v0.2.40+ sometimes creates multiindex)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = calculate_indicators(data)
    trades, final_val, equity_curve = run_backtest(data, args.capital, args.confirm_macd)

    if not trades and not final_val:
        print("❌ Error: Insufficient historical data to compute indicators and run backtest.")
        sys.exit(1)

    # Buy & Hold Return calculation
    first_close = data['Close'].iloc[14] # Matching start point
    last_close = data['Close'].iloc[-1]
    buy_and_hold_return = ((last_close - first_close) / first_close) * 100

    total_months = len(data) - 14

    print_results(ticker, trades, args.capital, final_val, buy_and_hold_return, total_months)

if __name__ == "__main__":
    main()
