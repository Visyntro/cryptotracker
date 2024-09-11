
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

"""This one is using the groq libary directly"""
from dotenv import load_dotenv

load_dotenv()
import json

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
from langchain_core.pydantic_v1 import BaseModel, Field
from typing_extensions import Annotated, TypedDict
from langchain.prompts import PromptTemplate
#from langchain.chains import LLMChain

from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()


import pandas as pd

cmcdf= pd.read_csv('coinmarketcappruned.csv')



top_cryptos = cmcdf['name'].tolist()





from langchain_groq import ChatGroq

from typing import List, Tuple
def crypto_categorizer(text: str) -> List[dict]:
    seen=set()
    words=text.split()
    cryptos=[]
    for word in words:
        if word in top_cryptos and word not in seen:
            cryptos.append(word)
            seen.add(word)
    if(not cryptos):
        cryptos.append("GeneralNews")
    print(cryptos)
    return cryptos
    '''llm = ChatGroq(groq_api_key = GROQ_API_KEY,model="llama3-8b-8192")
    #chain = LLMChain(prompt=prompt, llm=llm)
    chain = prompt | llm | parser
    result = chain.invoke({"text":text,"top_cryptos":top_cryptos})
    return eval(result)'''

"""### Using langchain to make our thing

Prompt Template
"""

def get_sentiment(news_articles,sentiment):

  with open('coinmarketpruned.json') as f:
    data = json.load(f)
  

  cryptos=crypto_categorizer(news_articles)
  cryptos=", ".join(cryptos)
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
    input_variables=["news_articles","sentiment","bruh","cryptos","cryptolist"],
    template="""
    
    You are Crypto Statistician and Market Analysis with extensive experience in providing real statistics on the crypto market. Given the following news article:

  

```plaintext

{news_articles}

```

  

**Market Sentiment:**

  

```plaintext

Sentiment: {bruh}

Confidence: {sentiment}%

```

  

**Live Cryptocurrency Tracker:**
Refer to the Live Cryotocurrency Tracker for the list of cryptocurrencies: 
{cryptolist}
  
  
  

**Task:**

  

Write the following strictly in **Markdown** format:

  
Write the biggest Gainers and Losers from this news article with their projected percent change and their projected market cap.

**Output:**

  

Please format the output in **Markdown** as follows:

  

```markdown

### Impact Analysis

  
  

#### Short Term

- Predictions: *The biggest Gainers and Losers related to this news with their Price, Percent Change and Projected Market Cap.*

  

#### Mid Term

- Predictions: *Details on how the news will affect specific cryptocurrencies and their trajectory or the general market in the mid term.*

  

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

  

**Only provide the Markdown output. Do not include any additional information or text.**"""
)
  
 
  
  llm = ChatGroq(groq_api_key = GROQ_API_KEY , model="llama3-8b-8192")
  chain = prompt | llm | parser 
  result = chain.invoke({"news_articles":news_articles,"sentiment":sentiment,"bruh":bruh,"cryptos":cryptos,"cryptolist":data})

  return sentiment+ " " +bruh+ "\n"+ result






  

