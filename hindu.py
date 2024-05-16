import newspaper
import os

cnn_paper = newspaper.build('https://cnn.com')

for article in cnn_paper.articles:
    print(article.url)