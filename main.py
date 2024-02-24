from flask import Flask, jsonify

from core.exp_github import update
from core.generate import summarise
from core.scrape import scrape_articles

app = Flask(__name__)

@app.route('/scrape', methods=['GET'])
def scrape_and_summarize():
    scrape_articles()
    summarise()
    return jsonify({"message": "Scraping and summarization completed."})

@app.route('/update', methods=['GET'])
def github_update():
    return jsonify({"message": update()})

if __name__ == '__main__':
    app.run(debug=True)
