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

co = cohere.Client(os.environ.get('COHERE_API_KEY'))

def configure_generative_model():
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
        model_name="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )

def cohere_summarize(content):

    response = co.summarize( 
      text=content,
      length='medium',
      format='bullets',
      model='command-nightly',
      additional_command='',
      temperature=0.3,
    ) 
    return response.summary

def cohere_title(question):

    response = co.generate(
      model='command',
      prompt= question,
      max_tokens=300,
      temperature=0.9,
      k=0,
      stop_sequences=[],
      return_likelihoods='NONE')

    return response.generations[0].text

def load_json_data(json_data):
    return json.loads(json_data)


def save_json_data(data, file_path):
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)


def generate_summary(model, article_content):
    prompt = f"{article_content}\n---\nYour task is to summarize the above article into 3 bullet points. Try to include the most important information which provides an overview of the article.\n---\n"
    try:
        answer = model.generate_content(prompt)
        return answer.text.strip().replace("\n\n", "\n")
    except Exception:
        logging.error("Error: Summary generation failed, Switching to Fallback Model")
        fallback_content = cohere_summarize(prompt)
        return fallback_content
    
def update_json_with_summaries(json_data, model):
    for article in json_data["articles"]:
        article["Summary"] = generate_summary(model, article["content"])


def generate_revised_title(model, article_title, article_content):
    revised_title_prompt = (
        f"Title:\n{article_title}\nContent:\n{article_content}\n---\nYour task is to give a revised title for the above article, do not include any clickbait words and represent the actual content of the article\n---\n"
    )
    try:
        response = model.generate_content(revised_title_prompt)
        return response.text.strip()
    except Exception:
        logging.error("Error: Title generation failed, Switching to Fallback Model")
        fallback_title_content = cohere_title(revised_title_prompt)
        return fallback_title_content

def update_json_with_titles(json_data, model):
    for article in json_data["articles"]:
        article["revised_title"] = generate_revised_title(model, article["title"], article["content"])

def summarise(json_buffer):
    model = configure_generative_model()
    json_data = load_json_data(json_buffer)
    update_json_with_summaries(json_data, model)
    update_json_with_titles(json_data, model)
    return json_data