from source.scrape import scrape_articles
from source.generate import summarise
from source.exp_github import update

scrape_articles()
summarise()
update()
