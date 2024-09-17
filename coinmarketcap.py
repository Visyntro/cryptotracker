from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from dotenv import load_dotenv
load_dotenv()
#import streamlit as st
import os
CMC_KEY=os.getenv("COINMARKETCAP_API_KEY")

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'20',
  'sort':'market_cap',
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': CMC_KEY,
}

session = Session()
session.headers.update(headers)

try:
  response = session.get(url, params=parameters)
  data = json.loads(response.text)
  #save this json for me
  #print(data)
  with open('coinmarketcap.json', 'w') as f:
    json.dump(data, f)

except (ConnectionError, Timeout, TooManyRedirects) as e:
  print(e)


import json
import csv

# Load the JSON data from the file
with open('coinmarketcap.json', 'r') as json_file:
    data = json.load(json_file)

# Extract relevant fields from the JSON structure
formatted_data = []
for entry in data['data']:
    # Extract the fields you need
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

# Define the CSV file headers
headers = [
    "id", "name", "symbol", "num_market_pairs", "infinite_supply", "cmc_rank",
    "last_updated", "price", "volume_24h", "volume_change_24h", "percent_change_1h",
    "percent_change_24h", "percent_change_7d", "percent_change_30d", 
    "percent_change_60d", "percent_change_90d", "market_cap", 
    "market_cap_dominance", "fully_diluted_market_cap", "quote_last_updated"
]

# Write the data to a CSV file
with open('coinmarketcap.csv', 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(formatted_data)

print("CSV file created successfully!")