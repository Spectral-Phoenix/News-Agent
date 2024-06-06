import json
import time
from datetime import date
from langchain_google_genai import ChatGoogleGenerativeAI
from supa_base import upload
from openai import OpenAI

today = str(date.today())

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key="AIzaSyCVamDnNAeezeywfPTet9t_Fvd_DTTIuu0",
)

with open(f'data/the_hindu/{today}_the_hindu.json', 'r') as f:
    data = json.load(f)

articles = data['articles']

def summarize_article(article):

    prompt = f"""
        Your task is to summarize the given article text into 3 concise bullet points. Follow these guidelines:

        - Read the article carefully and identify the main ideas or key points.
        - Summarize each main idea or key point in a clear, concise sentence.
        - Keep each bullet point brief, ideally no more than 20 words.
        - Do not include unnecessary details or examples from the article.
        - Write in an objective and impartial tone, avoiding personal opinions or biases.
        - Use proper grammar, spelling, and punctuation.
        - Donot include any markdown formatting like ```, #, *,etc.

        Input:

        Article: {article['title']}

        Text: {article['text']}

        Summary:

        - [Bullet point 1]
        - [Bullet point 2]
        - [Bullet point 3]
    """

    response = llm.invoke(prompt)
    return response.content

def categorise(article):
    prompt = f"""
        Students preparing for competitive exams like UPSC often rely on newspapers for current affairs, but some articles simply do not contain any useful information.
        Your task is to categorize articles from 'The Hindu' newspaper into the following categories and return a JSON Output:

        Categories:
        - World: Any events that occurred outside India
        - National: Events that occurred in India
        - Business: News related to companies and startups
        - Technology: News related to tech companies and their products
        - Science: Scientific news and discoveries
        - Sports
        - Entertainment
        - Culture
        - Lifestyle
        - Politics: News related to political parties, elections, etc.
        - Economy: Financial news
        - Health
        - Education
        - Environment
        - Crime
        - Weather
        - Traffic
        - Local

        Guidelines:
        1. Categorize the article into one or more relevant categories.

        2. Mark an article as "important" if it meets the following criteria:

            The article covers a current affairs topic that is directly relevant to the UPSC syllabus or exam pattern.
            The topic is related to India's national interest, international relations, economy, science and technology, environment, education, health, or any other subject area that is a part of the UPSC curriculum.
            The article provides in-depth analysis, facts, figures, or insights that can enhance the aspirant's understanding of the topic.
            The article discusses a significant event, policy, or decision that has far-reaching implications for the country or the world.

        3. Mark an article as "not important" if it falls into any of the following categories:

            Politics: Articles focusing solely on political parties, elections, or partisan politics.
            Crime: Articles covering criminal incidents or law enforcement activities, unless they involve high-profile cases or have broader implications for society or governance.
            Sports: Articles related to sports events, players, or teams, unless they cover a major international event or a sports policy issue.
            Entertainment: Articles about movies, music, celebrities, or the entertainment industry.
            Culture: Articles on cultural events, festivals, or traditions, unless they discuss a significant cultural issue or policy.
            Lifestyle: Articles covering fashion, food, travel, or personal interests.
            Weather: Articles reporting routine weather updates or forecasts.
            Traffic: Articles focusing on local traffic conditions or updates.
            Local: Articles covering hyperlocal events or issues that have limited broader relevance.
            World: Articles focusing on world events that are not directly related to India or the UPSC syllabus.

            Additionally, you can mark an article as "not important" if it lacks depth, analysis, or meaningful insights, and merely provides a surface-level or sensational account of an event or issue.
            Strictly mark articles as not important if they are analysis, editorials, essays or something like that.
            
        4. Do not provide any additional information or explanations; only return the JSON content.
        5. Do not add any markdown formatting for the JSON content like ```json, #, *,etc.; return it in plain text format.

        Input :
        -\-\-
        Title: {article['title']}
        Article: {article['text']}

        -\-\-

        Output Format (JSON):
        {{
          "category": ["category1", "category2", ...],
          "relevance": "important" or "not important"
        }}

        Output:

    """
    # Add Prompt Length management

    completion = client.chat.completions.create(
      model="microsoft/phi-3-small-8k-instruct",
      messages=[{"role":"user","content":f"{prompt}"}],
      temperature=0.4,
      top_p=0.7,
      max_tokens=1024,
      stream=False
    )
    try:
        response = completion.choices[0].message.content
        category_data = json.loads(response)
        
        if isinstance(category_data, list) and len(category_data) > 0:
            category_data = category_data[0]
            
        return category_data['category'], category_data['relevance']
    except json.JSONDecodeError:
        print(f"Error parsing JSON for article: {article['title']}")
        return None, None
    except (TypeError, KeyError) as e:
        print(f"Error accessing response data: {e}")
        return None, None

def main():
    count = 0
    length = len(articles)

    for article in articles:
        print(f"Categorising article {count+1}/{length}")
        try:
          category, relevance = categorise(article)
        except Exception as e:
          print(f"Error categorising article: {e}")
          category = "Unknown"
          relevance = 0

        if category and relevance:
            article["category"] = category
            article["relevance"] = relevance
            print(category, relevance)
        else:
            print(f"Skipping article: {article['title']}")
        count += 1
        time.sleep(1)

    count = 0
    length = len(articles)

    for article in articles:
        print(f"Summarising article {count+1}/{length}")
        summary = summarize_article(article)
        article["summary"] = summary.split("\n")
        count += 1

    with open(f'data/the_hindu/{today}_the_hindu.json', 'w') as f:
        json.dump(data, f, indent=4)

    file_path = f"{today}_the_hindu.json"
    upload("tech-crunch", file_path, f"data/the_hindu/{file_path}")
    print("Summaries Updated to Supabase")

if __name__ == "__main__":
    main()