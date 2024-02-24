from core.exp_github import update
from core.generate import summarise
from core.scrape import scrape_articles

scrape_articles()
summarise()
update()
