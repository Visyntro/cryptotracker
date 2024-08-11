
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

"""This one is using the groq libary directly"""

from groq import Groq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()


top_cryptos = [
    "Bitcoin", "Ethereum", "Tether USD", "BNB", "Solana", "USDC", "XRP", "Lido Staked Ether",
    "Toncoin", "Dogecoin", "Cardano", "TRON", "Wrapped liquid staked Ether 2.0", "Wrapped BTC",
    "Avalanche", "Shiba Inu", "Wrapped Ether", "Polkadot", "Bitcoin Cash", "Chainlink", "Dai",
    "Uniswap", "Litecoin", "Polygon", "Binance-Peg BSC-USD", "Kaspa", "Wrapped eETH",
    "Internet Computer (DFINITY)", "PEPE", "USDe", "Ethereum Classic", "Monero", "PancakeSwap",
    "Aptos", "NEAR Protocol", "Immutable X", "Fetch.AI", "OKB", "Stacks", "Filecoin", "Bittensor",
    "Stellar", "First Digital USD", "Mantle", "Hedera", "VeChain", "WhiteBIT Coin", "Render Token",
    "EnergySwap", "Maker",'BRETT', 'The Doge NFT', 'DEGEN', 'TOSHI', 'doginme', 'Normie',
    'OmniCat', 'Marvin', 'RealGOAT', 'Mister Miggles', 'Basenji', 'Filecoin',
    'UPSIDE DOWN MEME', 'SPX6900', '$MFER', 'ChompCoin', 'SKOP Token',
    'Marso.Tech', 'Keyboard Cat', 'higher', 'donotfomoew', 'Pepe',
    'Base God', 'Crash', 'BORED', 'Roost Coin', 'BUILD', 'FomoBullClub',
    'Noggles', 'All Street Bets', 'WASSIE', 'DINO', 'Moby', 'Mamba',
    'Shoobadookie', 'Based Street Bets', 'Ski Mask Dog', 'AEROBUD',
    'Fungi', 'FOMO_BASE', 'ROCKY', 'Rug World Assets', 'BlockChainPeople',
    'Apedinbase', 'GameStop on Base', 'Based Shiba Inu', 'Misser',
    'Father Of Meme: Origin', 'Katt Daddy', 'Heroes of memes', 'DERP'
]

prompt = PromptTemplate(
    input_variables=["text","top_cryptos"],
    template="""
        Given the following text:
        {text}

        Identify any cryptocurrencies mentioned in the text and categorize them as 'crypto' and the name of The specific Cryptocurrency from this list:
        {top_cryptos}

        If no cryptocurrencies are found, categorize the text as 'general'.

        The response should be a list of dictionaries with the following format:
        [
            {{
                "name": "Bitcoin",
                "category": "crypto"
            }},
            {{
                "name": "Ethereum",
                "category": "crypto"
            }},
            {{
                "name": "This text is not about any specific cryptocurrencies",
                "category": "general"
            }}
        ]
        Only write the list. Do not include any other text.
    """
)

from langchain_groq import ChatGroq

from typing import List, Tuple
def crypto_categorizer(text: str) -> List[dict]:
    llm = ChatGroq(groq_api_key = "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",model="llama3-8b-8192")
    #chain = LLMChain(prompt=prompt, llm=llm)
    chain = prompt | llm | parser
    result = chain.invoke({"text":text,"top_cryptos":top_cryptos})
    return eval(result)

"""### Using langchain to make our thing

Prompt Template
"""

def get_sentiment(news_articles):
  """
  Given the news article, returns the Sentiment Analysis Score on the Text """
# Load model directly
  from transformers import AutoTokenizer, AutoModelForSequenceClassification
  from transformers import pipeline
  tokenizer = AutoTokenizer.from_pretrained("kk08/CryptoBERT")
  model = AutoModelForSequenceClassification.from_pretrained("kk08/CryptoBERT")

  classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
  classy=classifier(news_articles)
  if classy[0]['label']=="LABEL_1":
    sentiment="Positive"
  else:
    sentiment="Negative"
  bruh= classy[0]['score']
  prompt = PromptTemplate(
    input_variables=["news_articles","sentiment","bruh"],
    template="""

        You are an expert in Cryptocurrency and have tons of experience in the analysis and speculations in the crypto market. You are given the follwing news article:
        {news_articles}

        We are getting the following sentiment from this article:
        {sentiment} with {bruh} confidence.

        In your expert knowledge in this field, explain why there could be this given sentiment:
    """
)
  llm = ChatGroq(groq_api_key = "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", model="llama3-8b-8192")
  chain = prompt | llm | parser
  result = chain.invoke({"news_articles":news_articles,"sentiment":sentiment,"bruh":bruh})


  return f"{sentiment} {classy[0]['score']} \n Here is why: \n {result}"

text = "The cryptocurrency market is no stranger to fleeting trends, and the recent surge and subsequent crash of immutable x … Continu"
categories = crypto_categorizer(text)
for category in categories:
    print(f"{category['name']} - {category['category']}")

"""Explaining the Sentiment using Groq."""

query = """
The cryptocurrency market is no stranger to fleeting trends, and the recent surge and subsequent crash of immutable x … Continu"""

print(get_sentiment(query))