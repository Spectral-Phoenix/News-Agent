import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

def load_configurations():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 0.5,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ],
        system_instruction=(
            "Rules for Article Evaluation:\n"
            "Relevance to Tech: The article should focus on core technology topics relevant to tech-savvy users, such as:\n"
            "Emerging technologies (AI, blockchain, quantum computing, etc.)\n"
            "Software development (programming languages, frameworks, etc.)\n"
            "Hardware and devices (new gadgets, advancements in chipsets, etc.)\n"
            "Cybersecurity and privacy\n"
            "Startup and investment news\n"
            "Tech industry trends and analysis\n"
            "News Worthiness: The article should cover recent developments, not rehashing older news or providing general information.\n"
            "Impact and Significance: The article should address topics with potential significant impact on the tech world or users.\n"
            "Author Credibility: Consider the author's reputation and expertise in the tech industry.\n"
            "Article Quality: The article should be well-written, informative, and free from clickbait or sensationalism.\n"
            "Instructions for the LLM:\n"
            "Read and understand each article's content.\n"
            "Assign an \"importance score\" to each article based on the above rules.\n"
            "Sort the articles in descending order of their importance scores.\n"
            "Return the top 7 articles in the specified JSON format.\n"
            "JSON Format:\n"
            "[\n"
            "    {\n"
            "        \"article_title\" : ......\n"
            "        \"article_link\" : .......\n"
            "        \"relevance_score\" : ....\n"
            "    }\n"
            "]\n"
        ),
    )
    return model

def load_prompt(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def extract_json_content(response_text):
    if "```json" in response_text:
        lines = response_text.splitlines()
        return '\n'.join(lines[1:-1])
    return None

def find_matching_articles(parsed_json, articles_with_content):
    matching_articles = []
    for article in parsed_json:
        article_link = article['article_link']
        for content_article in articles_with_content['articles']:
            if content_article['link'] == article_link:
                matching_articles.append({
                    'title': content_article['title'],
                    'image_links': content_article['image_links'],
                    'link': article_link,
                    'Summary': content_article['Summary'],
                    'revised_title': content_article['revised_title']
                })
    return matching_articles

def rank(date):
    load_configurations()
    model = load_configurations()
    prompt = load_prompt('data/2024-06-07_techcrunch.json')
    response_text = model.generate_content(prompt).text
    json_content = extract_json_content(response_text)

    if json_content:
        try:
            parsed_json = json.loads(json_content)
            with open(f'data/{date}_techcrunch.json', 'r') as file:
                articles_with_content = json.load(file)
            matching_articles = find_matching_articles(parsed_json, articles_with_content)

            output_data = {
                "source": "TechCrunch",
                "date": articles_with_content['date'],
                "no_of_articles": len(matching_articles),
                "articles": matching_articles
            }

            with open('extracted_articles.json', 'w') as file:
                json.dump(output_data, file, indent=4)
            print("Matching articles saved to extracted_articles.json")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
    else:
        print("No JSON content found in the response.")

rank("2024-06-07")