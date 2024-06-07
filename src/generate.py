import json
import logging
import os

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
    """
    Configure the Google Generative AI model with specific generation settings and safety configurations.
    
    Returns:
        genai.GenerativeModel: Configured generative model.
    """
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

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
    """
    Summarize content using Cohere's summarization model.
    
    Parameters:
        content (str): The content to summarize.
    
    Returns:
        str: The summary of the content.
    """
    response = co.summarize(
        text=content,
        length='medium',
        format='bullets',
        model='command-r-plus',
        additional_command='',
        temperature=0.3,
    ) 
    return response.summary

def cohere_title(question: str) -> str:
    """
    Generate a title using Cohere's generation model.
    
    Parameters:
        question (str): The prompt for title generation.
    
    Returns:
        str: The generated title.
    """
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

def load_json_data(file_path: str) -> dict:
    """
    Load JSON data from a file.
    
    Parameters:
        file_path (str): The path to the JSON file.
    
    Returns:
        dict: The loaded JSON data.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json_data(data: dict, file_path: str) -> None:
    """
    Save JSON data to a file.
    
    Parameters:
        data (dict): The data to save.
        file_path (str): The path to the file.
    """
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

def generate_summary(model, article_content: str) -> str:
    """
    Generate a summary for given article content using the configured model.
    
    Parameters:
        model: The generative model.
        article_content (str): The content of the article.
    
    Returns:
        str: The generated summary.
    """
    prompt = (f"{article_content}\n---\nYour task is to summarize the above article into 3 bullet points. "
              "Try to include the most important information which provides an overview of the article.\n---\n")
    try:
        answer = cohere_summarize(article_content)
        return answer
    except Exception:
        logging.error("Error: Summary generation failed, Switching to Fallback Model")
        answer = model.generate_content(prompt)
        return answer.text.strip().replace("\n\n", "\n")
        logging.info("Successfully generated summary using fallback model")

def update_json_with_summaries(json_data: dict, model) -> None:
    """
    Update JSON data with summaries for each article.
    
    Parameters:
        json_data (dict): The JSON data containing articles.
        model: The generative model.
    """
    for article in json_data["articles"]:
        article["Summary"] = generate_summary(model, article["content"])

def generate_revised_title(model, article_title: str, article_content: str) -> str:
    """
    Generate a revised title for an article using the configured model.
    
    Parameters:
        model: The generative model.
        article_title (str): The original title of the article.
        article_content (str): The content of the article.
    
    Returns:
        str: The generated revised title.
    """
    revised_title_prompt = (f"Title:\n{article_title}\nContent:\n{article_content}\n---\n"
                            "Your task is to give a revised title for the above article, do not include any clickbait words "
                            "and represent the actual content of the article\n---\n")
    try:
        response = model.generate_content(revised_title_prompt)
        return response.text.strip()
    except Exception:
        logging.error("Error: Title generation failed, Switching to Fallback Model")
        return cohere_title(revised_title_prompt)

def update_json_with_titles(json_data: dict, model) -> None:
    """
    Update JSON data with revised titles for each article.
    
    Parameters:
        json_data (dict): The JSON data containing articles.
        model: The generative model.
    """
    for article in json_data["articles"]:
        article["revised_title"] = generate_revised_title(model, article["title"], article["content"])

def summarise(json_file_path: str) -> None:
    """
    Summarize and generate revised titles for articles in a JSON file.
    
    Parameters:
        json_file_path (str): The path to the JSON file containing articles.
    """
    json_data = load_json_data(json_file_path)
    model = configure_generative_model()
    update_json_with_summaries(json_data, model)
    update_json_with_titles(json_data, model)
    save_json_data(json_data, json_file_path)

# if __name__ == "__main__":
#     json_file_path = "data/techcrunch_articles_2024-06-06.json"
#     summarise(json_file_path)