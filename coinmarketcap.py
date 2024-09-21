from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import csv
import os
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

CMC_KEY = st.secrets["COINMARKETCAP_API_KEY"]

def fetch_and_save_cryptocurrency_data():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '20',
        'sort': 'market_cap',
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': CMC_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = response.json()  # Directly parsing the API response

        # Extract and format the data
        formatted_data = []
        for entry in data['data']:
            formatted_entry = {
                "id": entry['id'],
                "name": entry['name'],
                "symbol": entry['symbol'],
                "num_market_pairs": entry['num_market_pairs'],
                "infinite_supply": str(entry['infinite_supply']),
                "cmc_rank": entry['cmc_rank'],
                "last_updated": entry['last_updated'],
                "price": entry['quote']['USD']['price'],
                "volume_24h": entry['quote']['USD']['volume_24h'],
                "volume_change_24h": entry['quote']['USD']['volume_change_24h'],
                "percent_change_1h": entry['quote']['USD']['percent_change_1h'],
                "percent_change_24h": entry['quote']['USD']['percent_change_24h'],
                "percent_change_7d": entry['quote']['USD']['percent_change_7d'],
                "percent_change_30d": entry['quote']['USD']['percent_change_30d'],
                "percent_change_60d": entry['quote']['USD']['percent_change_60d'],
                "percent_change_90d": entry['quote']['USD']['percent_change_90d'],
                "market_cap": entry['quote']['USD']['market_cap'],
                "market_cap_dominance": entry['quote']['USD']['market_cap_dominance'],
                "fully_diluted_market_cap": entry['quote']['USD']['fully_diluted_market_cap'],
                "quote_last_updated": entry['quote']['USD']['last_updated']
            }
            formatted_data.append(formatted_entry)

        # CSV headers
        headers = [
            "id", "name", "symbol", "num_market_pairs", "infinite_supply", "cmc_rank",
            "last_updated", "price", "volume_24h", "volume_change_24h", "percent_change_1h",
            "percent_change_24h", "percent_change_7d", "percent_change_30d", 
            "percent_change_60d", "percent_change_90d", "market_cap", 
            "market_cap_dominance", "fully_diluted_market_cap", "quote_last_updated"
        ]

        # Write data to CSV directly
        with open('coinmarketcap.csv', 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(formatted_data)

        return formatted_data

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        return f"Error fetching data: {e}"

# Call the function
result = fetch_and_save_cryptocurrency_data()
print(result)
