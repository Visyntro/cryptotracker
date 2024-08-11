import requests
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



"""## Key Points to notice

- We cant sort by top posts cuz most of these are giveaway/promotional posts that provide us no information about the news and updates (This will be figured by putting better queries)
- We can only search 20 posts at a time. I tried using more using this endpoint [POST https://api.socialdata.tools/twitter/search/asyncJob](https://api.socialdata.tools/twitter/search/asyncJob) but it immediately drained my account balance.
- Most of the output is in Other languages too. We must filter out languages other than english.

Running Cryptobert on these datasets
"""


for text in df['text']:
  result = classifier(text)
  print(result)

"""Now Getting News using News API"""



from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key='4670c278aa53490b99c29e290984acd4')
# /v2/everything
all_articles = newsapi.get_everything(q='bitcoin OR ethereum',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param= datetime.now()-timedelta(days=10),
                                      to=datetime.now(),
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)


all_articles

bruh= requests.get(f"https://newsapi.org/v2/everything?q=cryptocurrency OR bitcoin OR ethereum OR blockchain&from={datetime.now()-timedelta(days=10)}&to={datetime.now}&sortBy=popularity&language=en&apiKey=4670c278aa53490b99c29e290984acd4")

bruh.json()

df_news = pd.json_normalize(bruh.json()['articles'])
df_news.to_csv('cryptocurrency_news.csv', index=False)