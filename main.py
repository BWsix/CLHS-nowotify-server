from news_api import get_news
from notify import notify_discord, notify_line
from database import db_get_data, db_get_new_news

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

  webhook_urls = db_get_data("discord")
  lotify_tokens = db_get_data("line")

  for news in new_news:
    notify_discord(news, webhook_urls)
    notify_line(news, lotify_tokens)
