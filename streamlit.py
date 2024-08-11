import streamlit as st
import pandas as pd
from cryptosentiment import crypto_categorizer, get_sentiment

# Load the news CSV file
@st.cache_data
def load_news_data():
    return pd.read_csv("cryptocurrency_news.csv")

def safe_lower(value):
    """Convert value to lowercase string if possible, otherwise return empty string."""
    try:
        return str(value).lower()
    except:
        return ""

def main():
    st.set_page_config(page_title="Crypto News Analyzer", page_icon=":newspaper:", layout="wide")

    st.title("Crypto News Analyzer")

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
                        st.write(f"**Source:** {row.get('source.name', 'Unknown')}")
                        st.write(f"**Published:** {row.get('publishedAt', 'Unknown')}")
                        st.write(f"**Description:** {row.get('description', 'No description available')}")
                        
                        # Sentiment analysis
                        content = str(row.get('title', ''))
                        sentiment_result = get_sentiment(content)
                        st.write("**Sentiment Analysis:**")
                        st.write(sentiment_result)
                        
                        # Cryptocurrency categorization
                        categories = crypto_categorizer(content)
                        st.write("**Cryptocurrencies mentioned:**")
                        for category in categories:
                            st.write(f"- {category['name']} ({category['category']})")
            
            with col2:
                image_url = row.get('urlToImage')
                if image_url and isinstance(image_url, str):
                    st.image(image_url, use_column_width=True)
            
            st.markdown("---")

if __name__ == "__main__":
    main()