import streamlit as st
import pandas as pd
from cryptosentiment import crypto_categorizer, get_sentiment
from summarizer import summarize_news_article
import streamlit as st
import threading
import subprocess
import ccxt
import eventregistry
# Load the news CSV file
@st.cache_data
def load_news_data():
    return pd.read_csv("cryptocurrency_newsapi.csv")

def safe_lower(value):
    """Convert value to lowercase string if possible, otherwise return empty string."""
    try:
        return str(value).lower()
    except:
        return ""

def run_script(script_path):
    subprocess.run(['pipenv', 'run', 'python', script_path], check=True)

def run_all_scripts():
    scripts = [
        'tracker.py',
        'coinmarketcap.py',
        'news_twitter.py'
    ]
    
    for script in scripts:
        try:
            run_script(script)
        except subprocess.CalledProcessError as e:
            print(f"Error running {script}: {e}")

@st.cache_resource
def start_background_scripts():
    thread = threading.Thread(target=run_all_scripts)
    thread.daemon = True
    thread.start()
    return thread

def main():
    st.set_page_config(page_title="Crypto News Analyzer", page_icon=":newspaper:", layout="wide")

    st.title("Crypto News Analyzer")
    start_background_scripts()
    # Load news data
    news_data = load_news_data()

    # Sidebar for filters
    st.sidebar.title("Filters")
    search_term = st.sidebar.text_input("Search news")
    
    # Main content area
    for index, row in news_data.iterrows():
        title = safe_lower(row.get('title', ''))
        description = safe_lower(row.get('description', ''))
        
        if search_term.lower() in title or search_term.lower() in description:
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(f"📰 {row.get('title', 'Untitled')}", key=f"news_{index}"):
                    with st.expander("Article Details", expanded=True):
                        st.write(f"**Source:** {row.get('source', 'Unknown')}")
                        st.write(f"**Published:** {row.get('date', 'Unknown')}")
                        st.write(f"**Link:** {row.get('url', 'No description available')}")
                        
                        # Sentiment analysis
                        sentiment = str(row.get('sentiment', ''))
                        content=str(row.get('body', ''))
                        if len(content) > 20000:
                            content = content[:20000] + "..."
                        summarized_content = summarize_news_article(content)
                        categories = crypto_categorizer(content)
                        get_sentiment(summarized_content, sentiment,categories)
                        
                        # Cryptocurrency categorization
                        
                        
                        st.write("**Cryptocurrencies mentioned:**")
                        for category in categories:
                            st.write("- " + category)
            
            with col2:
                image_url = row.get('image')
                if image_url and isinstance(image_url, str):
                    st.image(image_url, use_column_width=True)
            
            st.markdown("---")

if __name__ == "__main__":
    main()