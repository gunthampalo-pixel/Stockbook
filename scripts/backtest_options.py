#!/usr/bin/env python3
import sys
import argparse
import yfinance as yf
import pandas as pd
from tabulate import tabulate

def parse_args():
    parser = argparse.ArgumentParser(description="Backtest Kan's EMA 10M Strategy for Options LEAPs")
    parser.add_argument("ticker", type=str, nargs="?", default="VRT", help="Stock ticker (e.g. VRT, NVDA, AAPL)")
    parser.add_argument("--capital", type=float, default=10000.0, help="Initial capital (default: 10000)")
    parser.add_argument("--period", type=str, default="15y", help="Historical period: 5y, 10y, 15y, 20y, max (default: 15y)")
    parser.add_argument("--premium-pct", type=float, default=20.0, help="Option premium cost as % of stock price (default: 20%)")
    parser.add_argument("--expiry-months", type=int, default=12, help="Options contract expiry in months (default: 12)")
    return parser.parse_args()

def calculate_indicators(df):
    # Monthly EMA 10
    df['EMA_10M'] = df['Close'].ewm(span=10, adjust=False).mean()
    return df

def run_options_backtest(df, initial_capital, premium_pct, expiry_months):
    cash = initial_capital
    active_option = None # Stores details of current open option contract
    trades = []
    
    premium_multiplier = premium_pct / 100.0
    start_idx = 14
    if len(df) <= start_idx:
        return None

    for i in range(start_idx, len(df)):
        date = df.index[i]
        close = df['Close'].iloc[i]
        ema_10m = df['EMA_10M'].iloc[i]
        prev_close = df['Close'].iloc[i-1]
        prev_ema_10m = df['EMA_10M'].iloc[i-1]

        # Check for Expiry of active option
        if active_option is not None:
            months_passed = (date.year - active_option['entry_date'].year) * 12 + (date.month - active_option['entry_date'].month)
            # Sell condition: price crosses below EMA 10M OR contract reaches expiry
            crossed_below = (prev_close >= prev_ema_10m) and (close < ema_10m)
            expired = months_passed >= expiry_months

            if crossed_below or expired:
                # Calculate Option Payoff
                # Payoff = max(0, Close_At_Exit - Strike_Price) * Contracts
                # We assume 1 contract represents 100 shares, but we scale by capital:
                # Option Value = Contracts * Payoff
                strike = active_option['strike']
                premium_paid = active_option['premium_paid']
                contracts_scaled = active_option['contracts']
                
                payoff_per_share = max(0.0, close - strike)
                final_option_value = contracts_scaled * payoff_per_share
                
                cash = final_option_value
                trade_return = ((cash - premium_paid) / premium_paid) * 100
                
                trades.append({
                    'EntryDate': active_option['entry_date'].strftime('%Y-%m-%d'),
                    'ExitDate': date.strftime('%Y-%m-%d'),
                    'Type': 'LEAP CALL',
                    'Strike': round(strike, 2),
                    'EntryPrice': round(active_option['entry_stock_price'], 2),
                    'ExitPrice': round(close, 2),
                    'PremiumPaid': round(premium_paid, 2),
                    'FinalValue': round(cash, 2),
                    'Return%': round(trade_return, 1),
                    'Reason': 'EXPIRED' if expired else 'CROSS_BELOW'
                })
                active_option = None

        # Check for Buy Signal (Crosses above EMA 10M)
        crossed_above = (prev_close <= prev_ema_10m) and (close > ema_10m)
        if crossed_above and active_option is None and cash > 0:
            # Buy At-The-Money (ATM) Call Option
            strike = close
            # Estimated premium cost per share
            option_premium = close * premium_multiplier
            # Number of shares we control (Option leverage)
            contracts = cash / option_premium
            
            active_option = {
                'entry_date': date,
                'entry_stock_price': close,
                'strike': strike,
                'premium_paid': cash,
                'contracts': contracts
            }
            # All cash is deployed into option premium
            cash = 0.0

    # Wrap up final value if there's an active option at the end of the data
    if active_option is not None:
        final_close = df['Close'].iloc[-1]
        strike = active_option['strike']
        contracts_scaled = active_option['contracts']
        payoff_per_share = max(0.0, final_close - strike)
        final_option_value = contracts_scaled * payoff_per_share
        
        trades.append({
            'EntryDate': active_option['entry_date'].strftime('%Y-%m-%d'),
            'ExitDate': df.index[-1].strftime('%Y-%m-%d'),
            'Type': 'LEAP CALL (OPEN)',
            'Strike': round(strike, 2),
            'EntryPrice': round(active_option['entry_stock_price'], 2),
            'ExitPrice': round(final_close, 2),
            'PremiumPaid': round(active_option['premium_paid'], 2),
            'FinalValue': round(final_option_value, 2),
            'Return%': round(((final_option_value - active_option['premium_paid']) / active_option['premium_paid']) * 100, 1),
            'Reason': 'HELD_TO_PRESENT'
        })
        cash = final_option_value

    return trades, cash

def main():
    args = parse_args()
    ticker = args.ticker.upper()

    print(f"📥 Downloading monthly price data for {ticker} (Period: {args.period})...")
    data = yf.download(ticker, period=args.period, interval="1mo", progress=False)

    if data.empty:
        print(f"❌ Error: No data found for ticker '{ticker}'")
        sys.exit(1)

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = calculate_indicators(data)
    trades, final_val = run_options_backtest(data, args.capital, args.premium_pct, args.expiry_months)

    if trades is None:
        print("❌ Error: Insufficient historical data to run Options backtest.")
        sys.exit(1)

    # Buy & Hold Stock comparison
    first_stock_close = data['Close'].iloc[14]
    last_stock_close = data['Close'].iloc[-1]
    buy_and_hold_return = ((last_stock_close - first_stock_close) / first_stock_close) * 100

    print("\n" + "="*95)
    print(f"🚀 KAN'S OPTIONS LEAPs BACKTEST REPORT: {ticker} (5x Leverage Call Option)")
    print("="*95)
    print(f"Strategy: Buy 12-Month ATM Call Option (Premium Cost: {args.premium_pct}% of Stock Price)")
    print(f"Exit Rule: Price Closes below Monthly EMA 10M OR Contract Reaches 12-Month Expiry")
    print("-"*95)
    print(f"Initial Capital   : ${args.capital:,.2f}")
    print(f"Final Options Value: ${final_val:,.2f}")
    
    options_return = ((final_val - args.capital) / args.capital) * 100
    print(f"Options Return    : {options_return:.2f}%")
    print(f"Stock Buy & Hold  : {buy_and_hold_return:.2f}%")
    print(f"Outperformance    : {options_return - buy_and_hold_return:.2f}%")
    
    print("-"*95)
    print("📋 OPTIONS TRANSACTION LOG:")
    print("-"*95)
    
    if not trades:
        print("No option contracts executed during this period.")
    else:
        headers = ["Entry Date", "Exit Date", "Strike", "Stock Entry", "Stock Exit", "Premium Paid", "Final Value", "Return %", "Exit Reason"]
        data_rows = [
            [
                t['EntryDate'],
                t['ExitDate'],
                f"${t['Strike']:.2f}",
                f"${t['EntryPrice']:.2f}",
                f"${t['ExitPrice']:.2f}",
                f"${t['PremiumPaid']:,.2f}",
                f"${t['FinalValue']:,.2f}",
                f"{t['Return%']}%",
                t['Reason']
            ]
            for t in trades
        ]
        print(tabulate(data_rows, headers=headers, tablefmt="grid"))
    print("="*95)

if __name__ == "__main__":
    main()
