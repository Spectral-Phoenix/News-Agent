from flask import Flask, jsonify

from core.exp_github import update
from core.generate import summarise
from core.scrape import scrape_articles

#app = Flask(__name__)
#
#@app.route('/process', methods=['GET'])
def process_data():
    # Call all the functions here
    scrape_articles()
    summarise()
    update()
    
    return jsonify({"message": "Scraping, summarization, and update completed."})

#if __name__ == '__main__':
    #app.run(debug=True)
process_data()