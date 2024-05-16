import json
import streamlit as st
import requests
from datetime import date
#from nav import switch_page
from annotated_text import annotated_text

st.set_page_config(
    page_title="News",
    page_icon="📰",
    layout="wide"
)

target_date = str("2024-03-27")

# Function to fetch JSON data from the cloud
def fetch_json_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return json.loads(response.text)
    else:
        st.error(f"Failed to fetch JSON data from {url}")
        return None

# Specify the URL of your JSON file hosted on the cloud
json_url = f"https://tuwtkihewdnqtxitktpe.supabase.co/storage/v1/object/public/tech-crunch/{target_date}_TechCrunch.json"

# Fetch JSON data from the cloud
json_data = fetch_json_data(json_url)

if json_data:
    #if st.button("⬅️ Go Back"):
        #switch_page("main")

    st.title(f"TechCrunch - {target_date}")
    st.write(f"Number of Articles: {json_data['no_of_articles']}")

    count = 454

    # Loop through articles and display information
    for article in json_data['articles']:
        with st.container(border=True):
            col1, col2 = st.columns([6, 3])
            with col1:
                st.subheader(article['revised_title'])
                st.caption(f"Original Title: {article['title']}")
                # annotated_text("Category: ", (article['category'], ""))
                
                st.markdown(f"{article['Summary']}</font>", unsafe_allow_html=True)
            with col2:
                # Display only the first image link if available
                if 'image_links' in article and len(article['image_links']) > 0:
                    st.image(article['image_links'][0], caption=None, width=None, use_column_width=True, clamp=False,
                             channels="RGB", output_format="auto")
                st.divider()
                st.markdown(f"<font face ='Mona-Sans'>Read more: [TechCrunch]({article['link']})</font>",
                            unsafe_allow_html=True)
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button(":card_file_box: Read Later",use_container_width=True, key=count) :
                        st.success("Saved")
                with col2:
                    st.button(":link: Share",use_container_width=True, key=count+9)
                count = count + 7