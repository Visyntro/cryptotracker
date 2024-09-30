import ccxt
import os
import time
from coinmarketcap import fetch_and_save_cryptocurrency_data
from news_twitter import newsscrape
from tracker import fetch_historical_data
import pandas as pd
def combinedscraperfunc():
    exchange = ccxt.kucoin()

    # List of cryptocurrencies
    cryptocurrencies = ['BTC', 'ETH', 'USDT', 'BNB', 'SOL', 'USDC', 'XRP', 'DOGE', 'TRX', 'TON', 'ADA', 'AVAX', 'SHIB', 'LINK', 'BCH', 'DOT', 'LEO', 'DAI', 'LTC', 'NEAR', 'UNI', 'KAS', 'ICP', 'XMR', 'PEPE', 'APT', 'FET', 'XLM', 'ETC', 'FDUSD', 'OKB', 'SUI', 'STX', 'CRO', 'AAVE', 'FIL', 'RENDER', 'IMX', 'MNT', 'TAO', 'MATIC', 'HBAR', 'ARB', 'VET', 'INJ', 'OP', 'ATOM', 'WIF', 'MKR', 'AR']

    # Folder to store the CSV files
    folder_name = 'crypto_data'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)  # Create the folder if it doesn't exist

    # Fetch data for each cryptocurrency
    for crypto in cryptocurrencies:
        print(f"Fetching data for {crypto}...")
        
        # Convert crypto name to symbol (this might need adjustment for some cryptocurrencies)
        symbol = f"{crypto}/USDT"
        if crypto == 'USDT':
            symbol = 'USDT/USD'
        
        # Fetch historical data
        df = fetch_historical_data(exchange, symbol)
        
        if df is not None:
            # Save the DataFrame as a CSV file in the designated folder
            csv_filename = os.path.join(folder_name, f"{crypto}_ohlcv.csv")
            df.to_csv(csv_filename, index=False)
            print(f"Saved {crypto} data to {csv_filename}")
        
        # Add a delay to avoid hitting rate limits
        time.sleep(1)

    bruh = fetch_and_save_cryptocurrency_data()

    if bruh == "Error fetching data: {e}":
        print("Error fetching data: {e}")

    bruh2= newsscrape()
    if bruh2.empty:
        print("Error fetching news:")
    else:
        print("News data fetched successfully.")
        os.remove("cryptocurrency_newsapi.csv")

        #bruhprev.drop(axis=0, inplace=True
        #add newly scraped dataframe to the previous dataframe
        bruh2.to_csv("cryptocurrency_newsapi.csv", index=False)

    print("All data saved successfully.")

