import logging

from .database import db_get_all_nowotify
from .news_api import News, UID_TABLE, get_new_news
from .notify import notify_users


import logging
logging.basicConfig(
  filename='logs/main.log',
  format='%(asctime)s - [%(levelname)s]%(message)s',
  encoding='utf-8',
  level=logging.INFO
)

GROUPS = UID_TABLE.keys()

def checker() -> None:
  """
  checks whether there's new news.
  
  if there's new news, this function will:
    1. update datebase
    2. send notifications to users
  """
  
  new_news: list[News] = []
  for group in GROUPS:
    new_news += get_new_news(group)

  if not new_news:
    logging.info("(no new news)")
    return 
  
  all_nowotify = db_get_all_nowotify()

  for news in new_news:
    logging.info(f"[NEW NEWS]\ndate:{news.date},id:{news.id},group:{news.group}\ncontent:{news.content}")
    notify_users(news, all_nowotify)

