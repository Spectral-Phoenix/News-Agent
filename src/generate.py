import logging
import os
import time

import cohere
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Cohere client
co = cohere.Client(os.getenv('COHERE_API_KEY'))

def configure_generative_model():
    """Configures and returns the Google Gemini generative model."""
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    except Exception as e:
        logging.error(f"Error configuring Gemini: {e}")
        raise  # Re-raise the exception to halt execution

    generation_config = {
        "temperature": 0.9,
        "top_p": 0.1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

def cohere_summarize(content: str) -> str:
    """Generates a summary of the given content using the Cohere API."""
    try:
        response = co.summarize(
            text=content,
            length='medium',
            format='bullets',
            model='command-r-plus',
            additional_command='',
            temperature=0.3,
        )
        return response.summary
    except Exception as e:
        logging.error(f"Error generating summary with Cohere: {e}")
        return "Error: Unable to generate summary."

def cohere_title(question: str) -> str:
    """Generates a title for the given question using the Cohere API."""
    try:
        response = co.generate(
            model='command-r-plus',
            prompt=question,
            max_tokens=300,
            temperature=0.9,
            k=0,
            stop_sequences=[],
            return_likelihoods='NONE'
        )
        return response.generations[0].text
    except Exception as e:
        logging.error(f"Error generating title with Cohere: {e}")
        return "Error: Unable to generate title."

def generate_summary(model, article_content: str) -> str:
    """Generates a 3-bullet point summary of the given article content."""
    prompt = (f"""
    {article_content}
    Instructions:
    Your task is to summarize the above article into 3 bullet points.
    Try to include the most important information which provides an overview of the article.
    Donot Include any explanation or pre summary text, just send me the Summary.
    Donot Include any markdown formatting, return simple plain text with each point starting by '- '
    """)
    try:
        answer = model.generate_content(prompt)
        return answer.text.strip().replace("\n\n", "\n")
    except Exception as e:
        logging.error(f"Error generating summary with Gemini: {e}. Switching to fallback model.")
        try:
            answer = cohere_summarize(article_content)
            logging.info("Successfully generated summary using fallback model.")
            return answer
        except Exception as e:
            logging.error(f"Error generating summary with fallback model (Cohere): {e}")
            return "Error: Unable to generate summary."

def clean_title(title: str) -> str:
    """Removes leading '#' and whitespace from a title."""
    return title.lstrip('#').strip()

def generate_revised_title(model, article_title: str, article_content: str) -> str:
    """Generates a revised title for the article."""
    revised_title_prompt = (f"""
    Title:{article_title}
    Content:{article_content}
    Your task is to give a revised title for the above article, do not include any clickbait words
    and represent the actual content of the article
    Just return a single revised title, donot include any explanation or markdown formatting.
    """)

    try:
        response = model.generate_content(revised_title_prompt)
        return clean_title(response.text.strip())
    except Exception as e:
        logging.error(f"Error generating revised title with Gemini: {e}. Switching to fallback model.")
        try:
            revised_title = clean_title(cohere_title(revised_title_prompt))
            logging.info("Successfully generated revised title using fallback model.")
            return revised_title
        except Exception as e:
            logging.error(f"Error generating revised title with fallback model (Cohere): {e}")
            return "Error: Unable to generate revised title."

def generate_summaries_and_titles(articles_data: dict) -> dict:
    """Generates summaries and revised titles for articles in the given data."""
    try:
        model = configure_generative_model()
    except Exception as e:
        logging.error(f"Error configuring generative model: {e}")
        return articles_data  # Return original data if model configuration fails

    for article in articles_data["articles"]:
        article["Summary"] = generate_summary(model, article["content"])
        article["revised_title"] = generate_revised_title(model, article["title"], article["content"])
        time.sleep(3) 
    return articles_data

# Example Usage (Commented out)
# if __name__ == "__main__":
#     with open("data/techcrunch_articles_2024-06-06.json", 'r', encoding='utf-8') as file:
#         json_data = json.load(file)
#     updated_data = generate_summaries_and_titles(json_data)
#     print(updated_data)