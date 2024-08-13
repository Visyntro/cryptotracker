import ccxt
import pandas as pd
from datetime import datetime, timedelta
import time

def fetch_historical_data(exchange, symbol, timeframe='1d', limit=7):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except Exception as e:
        print(f"Error fetching data for {symbol}: {str(e)}")
        return None

# Initialize exchange
exchange = ccxt.binance()

# List of cryptocurrencies
cryptocurrencies = [
    "Bitcoin", "Ethereum", "Tether USD", "BNB", "Solana", "USDC", "XRP", "Lido Staked Ether",
    "Toncoin", "Dogecoin", "Cardano", "TRON", "Wrapped liquid staked Ether 2.0", "Wrapped BTC",
    "Avalanche", "Shiba Inu", "Wrapped Ether", "Polkadot", "Bitcoin Cash", "Chainlink", "Dai",
    "Uniswap", "Litecoin", "Polygon", "Binance-Peg BSC-USD", "Kaspa", "Wrapped eETH",
    "Internet Computer (DFINITY)", "PEPE", "USDe", "Ethereum Classic", "Monero", "PancakeSwap",
    "Aptos", "NEAR Protocol", "Immutable X", "Fetch.AI", "OKB", "Stacks", "Filecoin", "Bittensor",
    "Stellar", "First Digital USD", "Mantle", "Hedera", "VeChain", "WhiteBIT Coin", "Render Token",
    "EnergySwap", "Maker"
]

# Dictionary to store results
results = {}

# Fetch data for each cryptocurrency
for crypto in cryptocurrencies:
    print(f"Fetching data for {crypto}...")
    
    # Convert crypto name to symbol (this might need adjustment for some cryptocurrencies)
    symbol = f"{crypto}/USDT"
    
    # Fetch historical data
    df = fetch_historical_data(exchange, symbol)
    
    if df is not None:
        results[crypto] = df
    
    # Add a delay to avoid hitting rate limits
    time.sleep(1)

# Print results
for crypto, df in results.items():
    print(f"\nHistorical data for {crypto}:")
    print(df)

# You can also save the results to CSV files if needed
# for crypto, df in results.items():
#     df.to_csv(f"{crypto}_historical_data.csv", index=False)