from database import db_get_all_nowotify
import logging
from news_api import get_new_news
from notify import notify_users

# from dotenv import load_dotenv
# load_dotenv()

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
  
  new_news = get_new_news()
  if not new_news:
    logging.info("(no new news)")
    return 

  all_nowotify = db_get_all_nowotify()

  for news in new_news:
    logging.info(f"[NEW NEWS]date:{news.date},id:{news.id},content:{news.content}")
    notify_users(news, all_nowotify)

