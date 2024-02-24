import json
import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

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

def load_json_data(file_path):
    with open(file_path, "r", encoding="utf-8") as json_file:
        return json.load(json_file)

def save_json_data(data, file_path):
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

def generate_summary(model, article_content):
    prompt = f"{article_content}\n---\nYour task is to summarize the above article into 3-5 bullet points. Try to include the most important information which provides an overview of the article.\n---\n"
    try:
        response = model.generate_content(prompt)
        return response.text.strip().replace("\n\n", "\n")
    except Exception as e:
        print(f"Error generating summary: {e}")
        print(f"Blocked Reason: {response.prompt_feedback}")
        return "Error: Summary generation failed."

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
    except Exception as e:
        print(f"Error generating title: {str(e)}")
        return f"Error: Title generation failed for '{article_title}'."

def update_json_with_titles(json_data, model):
    for article in json_data["articles"]:
        article["revised_title"] = generate_revised_title(model, article["title"], article["content"])

def summarise():
    model = configure_generative_model()

    # Generating Summaries
    json_path_summaries = "TechCrunch.json"
    json_data_summaries = load_json_data(json_path_summaries)
    update_json_with_summaries(json_data_summaries, model)
    save_json_data(json_data_summaries, json_path_summaries)
    print(f"JSON file '{json_path_summaries}' updated with summaries.")

    # Generating Titles
    json_path_titles = "TechCrunch.json"
    json_data_titles = load_json_data(json_path_titles)
    update_json_with_titles(json_data_titles, model)
    save_json_data(json_data_titles, json_path_titles)
    print(f"JSON file '{json_path_titles}' updated with generated titles.")