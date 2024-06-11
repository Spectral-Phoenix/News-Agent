import json
import logging
import os

import google.generativeai as genai
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)

def load_configurations():
    """Loads environment variables and configures the Google Gemini model."""
    try:
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)

        generation_config = {
            "temperature": 0.5,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ],
            system_instruction=(
                "Rules for Article Evaluation:\n"
                "Breaking News Priority: Prioritize articles that report on the latest breaking news in the tech industry. Focus on events that have just happened or are unfolding, not opinions or analysis.\n"
                "Tech Industry Focus: The article should cover core technology sectors and events that significantly impact the industry:\n"
                "Major product launches (e.g., new iPhone, groundbreaking AI models)\n"
                "Substantial tech acquisitions or mergers\n"
                "Regulatory changes affecting tech giants\n"
                "Critical cybersecurity breaches or vulnerabilities\n"
                "Breakthrough scientific or technological achievements\n"
                "Global Impact: Favor news that has wide-reaching effects on the global tech landscape, not just niche or local stories.\n"
                "Fundraising Selectivity: Include fundraising news only for exceptionally large rounds (e.g., over $100 million) or for highly influential companies (e.g., OpenAI, SpaceX).\n"
                "Authoritative Sources: Prioritize articles quoting or sourced from industry leaders, respected tech journalists, or official company announcements.\n"
                "Instructions for the LLM:\n"
                "Rapidly assess each article's content for breaking news value.\n"
                "Strictly avoid product reviews, Weekly reviews and other unencessary articles\n"
                "Assign a 'newsworthiness score' (1-10) based on the above rules, with higher scores for fresher, more impactful news.\n"
                "Sort articles in descending order of their newsworthiness scores.\n"
                " Only Return the articles which are important. be careful, you should never send an unecessary article, if you do so the trust on the news service will be reduced, so be extremely careful!!\
                    if there are no important articles, just return nothing.\n"
                "JSON Format:\n"
                "[\n"
                "    {\n"
                "        \"article_title\" : ......\n"
                "        \"article_link\" : .......\n"
                "        \"newsworthiness_score\" : ....\n"
                "    }\n"
                "]\n"
            ),
        )
        return model
    except Exception as e:
        logging.error(f"Error loading configurations: {e}")
        return None

def load_data(data):
    """Loads articles data from the provided dictionary."""
    try:
        return json.dumps(data)
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return None

def extract_json_content(response_text):
    """Extracts JSON content from the response text."""
    try:
        if "```json" in response_text:
            lines = response_text.splitlines()
            return '\n'.join(lines[1:-1])
        return None
    except Exception as e:
        logging.error(f"Error extracting JSON content: {e}")
        return None

def find_matching_articles(parsed_json, articles_with_content):
    """Finds and returns matching articles based on their links."""
    matching_articles = []
    try:
        for article in parsed_json:
            article_link = article.get('article_link')  # Use .get() to handle missing keys
            if not article_link:
                logging.warning(f"Missing 'article_link' in parsed JSON: {article}")
                continue 

            for content_article in articles_with_content['articles']:
                if content_article['link'] == article_link:
                    matching_articles.append({
                        'title': content_article.get('title'),
                        'image_links': content_article.get('image_links'),
                        'link': article_link,
                        'Summary': content_article.get('Summary'),
                        'revised_title': content_article.get('revised_title')
                    })
    except Exception as e:
        logging.error(f"Error finding matching articles: {e}")

    return matching_articles


def rank_articles(articles_data):
    """Ranks the provided articles using the configured model."""
    model = load_configurations()
    if not model:
        logging.error("Model loading failed. Cannot rank articles.")
        return None

    prompt = load_data(articles_data)
    if not prompt:
        logging.error("Data loading failed. Cannot rank articles.")
        return None

    try:
        response_text = model.generate_content(prompt).text
        json_content = extract_json_content(response_text)

        if json_content:
            try:
                parsed_json = json.loads(json_content)
                matching_articles = find_matching_articles(parsed_json, articles_data)
                output_data = {
                    "source": "TechCrunch",
                    "date": articles_data.get('date'), 
                    "no_of_articles": len(matching_articles),
                    "articles": matching_articles
                }
                return output_data
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON: {e}")
                return None
        else:
            logging.warning("No JSON content found in the response.")
            return None

    except Exception as e:
        logging.error(f"Error during article ranking: {e}")
        return None