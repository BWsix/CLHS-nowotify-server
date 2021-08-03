from news_api import get_news
from database import db_get_all_nowotify, db_get_new_news
from notify import notify_users

import logging
logging.basicConfig(
  filename='logs/main.log',
  format='%(asctime)s - [%(levelname)s]%(message)s',
  encoding='utf-8',
  level=logging.INFO
)


def checker() -> None:
  """
  checks whether there's new news.
  
  if there's new news, this function will:
    1. update datebase
    2. send notifications to users
  """

  fetched_news = get_news()
  new_news = db_get_new_news(fetched_news)

  if not new_news: return 
  
  all_nowotify = db_get_all_nowotify()

  for news in new_news:
    notify_users(news, all_nowotify)

