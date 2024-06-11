import streamlit as st
import json

def main():

    st.text("")

    # Load the JSON data
    with open("2024-06-10_techcrunch.json", "r") as f:
        data = json.load(f)

    # Display articles with checkboxes, using unique keys
    selected_articles = []
    for i, article in enumerate(data["articles"]):
        st.markdown(f"### {article['revised_title']}")
        st.write(article["Summary"])
        key = f"checkbox_{i}"  # Create a unique key for each checkbox
        if st.checkbox("Select this article", key=key):
            selected_articles.append(article)
        st.divider()

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