import streamlit as st
from newspaper import Article
import requests
from requests.exceptions import RequestException

def main():
    st.title("Web Scraping with newspaper3k")
    
    # User input for URL
    url = st.text_input("Enter the URL of the article you'd like to scrape:")
    
    # Placeholder for scraped data
    if st.button("Scrape"):
        if url:
            try:
                # Mimic a browser request with additional headers
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Referer': 'https://www.google.com/'
                }
                
                # Use a session to handle cookies and headers
                session = requests.Session()
                response = session.get(url, headers=headers)
                response.raise_for_status()  # Raise an error for bad status codes
                
                # Scraping the article
                article = Article(url)
                article.set_html(response.text)
                article.parse()
                
                # Display the title, authors, publication date, and text
                st.header("Title")
                st.write(article.title)
                
                st.header("Authors")
                st.write(article.authors)
                
                st.header("Publication Date")
                st.write(article.publish_date)
                
                st.header("Text")
                st.write(article.text)
                
            except RequestException as e:
                st.error(f"An HTTP error occurred: {e}")
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a valid URL.")
    
if __name__ == "__main__":
    main()