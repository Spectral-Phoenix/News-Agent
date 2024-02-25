from flask import Flask, jsonify

from core.exp_github import update
from core.generate import summarise
from core.scrape import scrape_articles

app = Flask(__name__)

@app.route('/')
def home():
    return "<h2> News Agent - Flask App</h2>"

@app.route('/process', methods=['GET'])
def process_data():
    content = scrape_articles()
    summarised_content = summarise(content)
    update(summarised_content)
    
    return jsonify({"message": "Scraping, summarization, and update completed."})
