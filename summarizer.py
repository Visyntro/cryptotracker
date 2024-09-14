from groq import Groq
import streamlit as st
def summarize_news_article(news_article:str)->str:
    client = Groq(groq_api_key=st.secrets["groq_api_key"])
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Summarize the following news article in 100 words, highlighting key points and cryptocurrencies mentioned. The summary should strictly contain only the core content and details without any introductory or concluding phrases."
            },
            {
                "role": "user",
                "content": news_article
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    return completion.choices[0].message.content

