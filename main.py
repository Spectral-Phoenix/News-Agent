from core.scrape import scrape_articles
from core.generate import summarise
from core.exp_github import update

scrape_articles()
summarise()
update()
