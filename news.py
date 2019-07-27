import sqlite3
import sys

import json

database_location = './data/NewsApiData.db'
datafile_location = './data/data.json'

from datetime import datetime, timedelta
from news import *
from newsapi import NewsApiClient



def main():
    key_words = ''
    is_error = False

    with open(datafile_location) as f:
        data = json.load(f)

    api_key_gnews = str(data["api_key_gnews"])

    # Initialise
    newsapi = NewsApiClient(api_key=api_key_gnews)

    for key_words in data["key_words"]:
        print(key_words)
        search(newsapi, str(key_words), 1)


def search(newsapi, key_words, page):
    today = datetime.now()  # get_date_ago(0)
    N = 29
    tweek_ago = datetime.now() - timedelta(days=N)  # get_date_ago(29)

    news = newsapi.get_everything(q=key_words.replace(",", " OR "),
                                  from_param=tweek_ago.strftime("%Y-%m-%d, %H:%M:%S"),
                                  to=today.strftime("%Y-%m-%d, %H:%M:%S"),
                                  language='en',
                                  sort_by='relevancy',
                                  page=page,
                                  page_size=100
                                  )

    for news_article in news['articles']:
        author = news_article['author']
        title = news_article['title']
        description = news_article['description']
        url = news_article['url']
        urlToImage = news_article['urlToImage']
        publishedAt = news_article['publishedAt']
        content = news_article['content']

        save_data(key_words,
                  author,
                  title,
                  description,
                  url,
                  urlToImage,
                  publishedAt,
                  content)


def save_data(key_words,
              author,
              title,
              description,
              url,
              urlToImage,
              publishedAt,
              content):
    conn = sqlite3.connect(database_location)
    c = conn.cursor()

    csid = 0

    for row in c.execute('SELECT url FROM Details where url = ?', (url,)).fetchall():
        csid = str(row[0])
        if csid != 0:
            continue
    if csid == 0:
        print("Insert: ", key_words, url)
        c.execute('''INSERT INTO Details VALUES(
                                  NULL,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?,
                                  ?
                              )''', (
            key_words,
            author,
            title,
            description,
            url,
            urlToImage,
            publishedAt,
            content
        ))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
