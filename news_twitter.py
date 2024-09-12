'''import requests
import pandas as pd
from datetime import datetime, timedelta

# Social Data API endpoint and your API key
API_ENDPOINT = "https://api.socialdata.tools/twitter/search"
API_KEY = "574|9dLEGFBiWHWnFsZj04Tx5fflaBFJEgJqLq7PTedh7a138543"

def fetch_tweets(keywords, start_date, end_date, limit=1000):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    params = {
        "query": " OR ".join(keywords)+ " AND news",
        "type": "Top",
        "limit": limit,
    }

    response = requests.get(API_ENDPOINT, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching tweets: {response.status_code} - {response.text}")

def process_tweets(tweets_data):
    processed_tweets = []
    for tweet in tweets_data['tweets']:
        processed_tweets.append({
            'created_at': tweet['tweet_created_at'],
            'text': tweet['full_text'],
            'username': tweet['user']['screen_name'],
            'retweet_count': tweet['retweet_count'],
            'favorite_count': tweet['favorite_count'],
            'media_url': tweet['entities']['media'][0]['media_url_https'] if 'media' in tweet['entities'] else None
        })
    return processed_tweets

# Main execution
if __name__ == "__main__":
    # Set up search parameters
    keywords = ["bitcoin", "ethereum", "cryptocurrency", "crypto"]
    start_date = datetime.now() - timedelta(days=10)  # Last 7 days
    end_date = datetime.now()

    # Fetch tweets
    raw_tweets = fetch_tweets(keywords, start_date, end_date)

    # Process tweets
    processed_tweets = process_tweets(raw_tweets)

    # Convert to DataFrame
    df = pd.DataFrame(processed_tweets)

    # Save to CSV
    csv_filename = 'cryptocurrency_tweets.csv'
    df.to_csv(csv_filename, index=False)

    print(f"Extracted {len(df)} tweets about cryptocurrency.")
    print(f"Data saved to '{csv_filename}'")

    # Display first few rows
    print(df.head())

'''

"""## Key Points to notice

- We cant sort by top posts cuz most of these are giveaway/promotional posts that provide us no information about the news and updates (This will be figured by putting better queries)
- We can only search 20 posts at a time. I tried using more using this endpoint [POST https://api.socialdata.tools/twitter/search/asyncJob](https://api.socialdata.tools/twitter/search/asyncJob) but it immediately drained my account balance.
- Most of the output is in Other languages too. We must filter out languages other than english.

Running Cryptobert on these datasets
"""


"""Now Getting News using News API"""


import pandas as pd
import dotenv 
import os
from dotenv import load_dotenv
load_dotenv()
eventkey = os.getenv('eventregistry')

from eventregistry import *
# since we want results from last month, just prevent use of archive - in this way we don't need to set any date constraints
er = EventRegistry(apiKey = eventkey , allowUseOfArchive = False)


query = {
    "$query": {
          "$or": [
                        {"keyword": "Memecoins", "keywordLoc": "body"},
                        {"keyword": "Cryptocurrency", "keywordLoc": "body"},
                        {"keyword": "Bitcoin", "keywordLoc": "body"},
                        {"keyword": "Ethereum", "keywordLoc": "body"},
                        {"keyword": "Cryptocurrency_wallet", "keywordLoc": "body"},
                        {"keyword": "Blockchain", "keywordLoc": "body"},
                        {"keyword": "Altcoins", "keywordLoc": "body"},
                        {"keyword": "Web3", "keywordLoc": "body"},
                        {"keyword": "Metaverse", "keywordLoc": "body"},
                        {"keyword": "DAO", "keywordLoc": "body"},
                        {"keyword": "Cryptocurrency exchange", "keywordLoc": "body"},
                    
            {
              "conceptUri": "http://en.wikipedia.org/wiki/Cryptocurrency"
            },
            {
              "conceptUri": "http://en.wikipedia.org/wiki/Bitcoin"
            },
            {
              "conceptUri": "http://en.wikipedia.org/wiki/Ethereum"
            },
            {
              "conceptUri": "http://en.wikipedia.org/wiki/Cryptocurrency_wallet"
            },
            {
              "conceptUri": "http://en.wikipedia.org/wiki/Blockchain"
            },
            {
              "conceptUri": "http://pt.wikipedia.org/wiki/Altcoins"
            },
            {
              "conceptUri": "http://en.wikipedia.org/wiki/Web3"
            },
            {
              "conceptUri": "http://en.wikipedia.org/wiki/Metaverse"
            },
            {
              "conceptUri": "http://es.wikipedia.org/wiki/DAO"
            },
            {
              "conceptUri": "http://en.wikipedia.org/wiki/Cryptocurrency_exchange"
            },
                  {
        "$or": [
          {
            "locationUri": "http://en.wikipedia.org/wiki/India"
          },
          {
            "locationUri": "http://en.wikipedia.org/wiki/United_States"
          },
          {
            "locationUri": "http://en.wikipedia.org/wiki/Europe"
          }
        ]
      },
            {
              "lang": "eng"
            }
          ]
        },
    "$filter": {
      "forceMaxDataTimeWindow": "120"
    }
    
  }
q = QueryArticlesIter.initWithComplexQuery(query)
# change maxItems to get the number of results that you want
articles = []

# change maxItems to get the number of results that you want
for article in q.execQuery(er, maxItems=150):
    articles.append({
        "title": article.get("title"),
        "url": article.get("url"),
        "date": article.get("date"),
        "source": article.get("source", {}).get("title"),
        "body": article.get("body"),
        "image": article.get("image", {}),
        "sentiment": article.get("sentiment", {})
    })

# Convert the list of dictionaries into a DataFrame
df_news = pd.DataFrame(articles)

# Display the DataFrame
print(df_news)

df_news.to_csv('C:\\Users\\utfu\\Desktop\\cryptotracker\\test\\cryptotracker\\cryptocurrency_newsapi.csv', index=False)


# alternatively, the same query using the query language could look something like this:

                

#bruh.json()

'''df_news = pd.json_normalize(bruh.json()['articles'])
df_news.to_csv('cryptocurrency_news.csv', index=False)'''