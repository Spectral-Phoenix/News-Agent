import streamlit as st
import json

def main():
    st.title("TechCrunch Article Selector")

    # Load the JSON data
    with open("2024-06-10_techcrunch.json", "r") as f:
        data = json.load(f)

    # Display articles with checkboxes
    selected_articles = []
    for article in data["articles"]:
        with st.expander(article["title"]):
            st.write(article["content"])
            if st.checkbox("Select this article"):
                selected_articles.append(article)

    # Save selected articles to a new JSON file
    if st.button("Save Selected Articles"):
        if selected_articles:
            with open("selected_techcrunch_articles.json", "w") as f:
                json.dump({"articles": selected_articles}, f, indent=4)
            st.success("Selected articles saved to selected_techcrunch_articles.json")
        else:
            st.warning("No articles selected.")

if __name__ == "__main__":
    main()