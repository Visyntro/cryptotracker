from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'50',
  'sort':'market_cap',
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '22145243-9872-45c3-8c9c-aef3bcbc79de',
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

# Define the CSV file headers
headers = [
    "id", "name", "symbol", "slug", "num_market_pairs", "date_added", "tags",
    "max_supply", "circulating_supply", "total_supply", "platform_id", "platform_name",
    "platform_symbol", "platform_slug", "platform_token_address", "infinite_supply",
    "cmc_rank", "self_reported_circulating_supply", "self_reported_market_cap",
    "tvl_ratio", "last_updated", "price", "volume_24h", "volume_change_24h",
    "percent_change_1h", "percent_change_24h", "percent_change_7d", "percent_change_30d",
    "percent_change_60d", "percent_change_90d", "market_cap", "market_cap_dominance",
    "fully_diluted_market_cap", "tvl", "quote_last_updated"
]

# Open the CSV file for writing
