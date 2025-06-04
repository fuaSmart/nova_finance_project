import pandas as pd
import yfinance as yf
import os

def calculate_indicators(ticker):
    # Load historical data
    df = pd.read_csv(f'../data/{ticker}_historical_data.csv')
    
    # Calculate indicators
    # df['SMA_20'] = talib.SMA(df['Close'], timeperiod=20)
    # df['RSI_14'] = talib.RSI(df['Close'], timeperiod=14)
    # df['MACD'], df['MACD_signal'], _ = talib.MACD(df['Close'])
    
    # Save results
    df.to_csv(f'../results/{ticker}_with_indicators.csv', index=False)
    return df

def plot_indicators(ticker, df):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(14,10))
    
    # Price and SMA
    plt.subplot(3,1,1)
    plt.plot(df['Date'], df['Close'], label='Close')
    plt.plot(df['Date'], df['SMA_20'], label='20-day SMA')
    plt.title(f'{ticker} Price and Moving Average')
    plt.legend()
    
    # RSI

    plt.subplot(3,1,2)
    plt.plot(df['Date'], df['RSI_14'], label='RSI', color='orange')
    plt.axhline(70, linestyle='--', color='red')
    plt.axhline(30, linestyle='--', color='green')
    plt.title('Relative Strength Index (RSI)')
    
    # MACD
    plt.subplot(3,1,3)
    plt.plot(df['Date'], df['MACD'], label='MACD', color='blue')
    plt.plot(df['Date'], df['MACD_signal'], label='Signal', color='red')
    plt.title('MACD Indicator')
    
    plt.tight_layout()
    plt.savefig(f'../plots/{ticker}_technical_indicators.png')
    plt.close()

if __name__ == "__main__":
    os.makedirs('../results', exist_ok=True)
    os.makedirs('../plots', exist_ok=True)
    
    stocks = ['AMZN', 'GOOG', 'META', 'MSFT', 'NVDA', 'TSLA']
    for ticker in stocks:
        print(f"Processing {ticker}")
        df = calculate_indicators(ticker)
        plot_indicators(ticker, df)