import pandas as pd
import numpy as np
from textblob import TextBlob
from tqdm import tqdm

def analyze_sentiment(text):
    return TextBlob(text).sentiment.polarity

def process_news_data():
    # Process news in chunks
    chunks = pd.read_csv('../data/raw_analyst_ratings.csv', 
                         chunksize=100000,
                         parse_dates=['date'])
    
    results = []
    for chunk in tqdm(chunks, desc="Processing news data"):
        # Sentiment analysis
        chunk['sentiment'] = chunk['headline'].apply(analyze_sentiment)
        
        # Simplify date to match stock data
        chunk['date_only'] = chunk['date'].dt.date
        
        # Keep only needed columns
        results.append(chunk[['stock', 'date_only', 'sentiment']])
    
    return pd.concat(results)

def calculate_daily_correlation(stock_ticker):
    # Load stock data
    stock_df = pd.read_csv(f'../results/{stock_ticker}_with_indicators.csv')
    stock_df['Date'] = pd.to_datetime(stock_df['Date']).dt.date
    stock_df['Daily_Return'] = stock_df['Close'].pct_change()
    
    # Load sentiment data for this stock
    news_df = pd.read_csv('../results/daily_sentiment.csv')
    news_df = news_df[news_df['stock'] == stock_ticker]
    
    # Merge datasets
    merged = pd.merge(stock_df, news_df, 
                      left_on='Date', 
                      right_on='date_only',
                      how='left')
    
    # Calculate correlation
    correlation = merged[['sentiment', 'Daily_Return']].corr().iloc[0,1]
    
    # Plot results
    import matplotlib.pyplot as plt
    fig, ax1 = plt.subplots(figsize=(14,6))
    
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Sentiment Score', color='tab:blue')
    ax1.plot(merged['Date'], merged['sentiment'], color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    
    ax2 = ax1.twinx()
    ax2.set_ylabel('Daily Return', color='tab:red')
    ax2.plot(merged['Date'], merged['Daily_Return'], color='tab:red', alpha=0.6)
    ax2.tick_params(axis='y', labelcolor='tab:red')
    
    plt.title(f'{stock_ticker}: Sentiment vs. Returns (Correlation: {correlation:.2f})')
    plt.savefig(f'../plots/{stock_ticker}_sentiment_correlation.png')
    plt.close()
    
    return correlation

if __name__ == "__main__":
    # Step 1: Process news data (only run once)
    print("Processing news sentiment...")
    news_df = process_news_data()
    
    # Aggregate by stock and date
    daily_sentiment = news_df.groupby(['stock', 'date_only'])['sentiment'].mean().reset_index()
    daily_sentiment.to_csv('../results/daily_sentiment.csv', index=False)
    
    # Step 2: Calculate correlations for each stock
    stocks = ['AMZN', 'GOOG', 'META', 'MSFT', 'NVDA', 'TSLA']
    correlations = {}
    
    for ticker in stocks:
        print(f"Analyzing {ticker}")
        corr = calculate_daily_correlation(ticker)
        correlations[ticker] = corr
    
    # Save correlation results
    corr_df = pd.DataFrame(list(correlations.items()), columns=['Stock', 'Correlation'])
    corr_df.to_csv('../results/sentiment_correlations.csv', index=False)
    print(corr_df)