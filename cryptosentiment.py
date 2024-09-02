
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

"""This one is using the groq libary directly"""

from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Optional
from typing_extensions import Annotated, TypedDict
from langchain.prompts import PromptTemplate
#from langchain.chains import LLMChain

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

def get_sentiment(news_articles,sentiment):
  
  cryptos=crypto_categorizer(news_articles)
  for crypto in cryptos:
    if crypto['category']=="crypto":
      cryptos=",".join(crypto['name'])
      break
  """
  Given the news article, returns the Sentiment Analysis Score on the Text """
# Load model directly
  '''from transformers import AutoTokenizer, AutoModelForSequenceClassification
  from transformers import pipeline
  tokenizer = AutoTokenizer.from_pretrained("kk08/CryptoBERT")
  model = AutoModelForSequenceClassification.from_pretrained("kk08/CryptoBERT")

  classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
  classy=classifier(news_articles)'''
  bruh=""
  if float(sentiment)>0:
    bruh="Positive"
  else:
    bruh="Negative"
  prompt = PromptTemplate(
    input_variables=["news_articles","sentiment","bruh","cryptos"],
    template="""

You are an expert in Cryptocurrency and Market Analysis with extensive experience in analyzing and speculating on the crypto market. Given the following news article:

```plaintext
{news_articles}
```

**Market Sentiment:**

```plaintext
Sentiment: {bruh}
Confidence: {sentiment}%
```

**Task:**

Write the following strictly in **Markdown** format:

1. Provide a detailed analysis of how this news and its sentiment will impact the performance of the associated cryptocurrencies \n {cryptos} \n Include specific predictions for the short-term (next few days), mid-term (next few weeks), and long-term (next few months) market movements.

2. If the news is about the general cryptocurrency market, analyze how it might change public and market opinion, affecting overall market trends and specific sectors within the market, also considering its sentiment.

3. Take into account, if applicable, the political, economic, and social factors that could influence the market based on this news article and its associated sentiment.

**Output:**

Please format the output in **Markdown** as follows:

```markdown
### Impact Analysis

#### Short Term
- Predictions: *Details on how the news will affect specific cryptocurrencies or the general market in the short term.*

#### Mid Term
- Predictions: *Details on how the news will affect specific cryptocurrencies or the general market in the mid term.*

#### Long Term
- Predictions: *Details on how the news will affect specific cryptocurrencies or the general market in the long term.*

### Market Opinion Change

#### Public Opinion
- *Explanation of how public opinion might shift based on the news.*

#### Market Trends
- *Analysis of how market trends might change as a result of the news.*

### Additional Factors

- **Political Factors:** *Consideration of political elements that could impact the market.*
- **Economic Factors:** *Analysis of economic conditions influenced by the news.*
- **Social Factors:** *Social dynamics that might affect the cryptocurrency market based on the news.*
```

**Only provide the Markdown output. Do not include any additional information or text.**


    """
)
  
 
  
  llm = ChatGroq(groq_api_key = "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", model="llama3-8b-8192")
  chain = prompt | llm | parser 
  result = chain.invoke({"news_articles":news_articles,"sentiment":sentiment,"bruh":bruh,"cryptos":cryptos})

  return result
  

