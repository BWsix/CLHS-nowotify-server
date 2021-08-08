import logging
import os
import json
import requests
from dataclasses import dataclass, field

from .database import db, db_get_ids_on_latest_date, db_update_news_ids
from data import UID_TABLE, KEYWORD_TABLE


API_ENTRY = "https://www.clhs.tyc.edu.tw/ischool/widget/site_news/news_query_json.php"
API_HEADER = {'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
API_BODY = "field=time&order=DESC&pageNum=0&maxRows={1}&keyword=&uid={0}&tf=1&auth_type=user&use_cache=1"


@dataclass(frozen=True)
class News:
  """News. will be compared based on only publish/update date"""
  
  date: str       
  id: int
  content: str
  office: str
  news_type: str
  is_pinned: bool
  group: str
  keyword_ids: list[int]

  def __str__(self):
    return f"date:{self.date},id:{self.id},group:{self.group}{'(pinned)' if self.is_pinned else ''}\ncontent:{self.content}"


def get_news(group: str, data_count: int = 40) -> list[News]:
  """fetches first n news from a certain page(group).  

  Args :
    `group` : `"main"` or `"first_grade"`.  
    `data_count` : how many news to fetch. (40 by default).  
  Returns :
    `news_list` : list[`News`].  
  """

  res = requests.post(
    API_ENTRY,
    headers=API_HEADER,
    data=API_BODY.format(UID_TABLE[group], data_count),
  )
  data = json.loads(res.text)[1:]

  news_list: list[News] = []

  for elem in data:
    content = elem.get("title")
    matched_keywords = []
    
    for idx, keyword_list in KEYWORD_TABLE.items():
      for keyword in keyword_list:
        if content.find(keyword) != -1:
          matched_keywords.append(idx)
          break

    news = News(
      id          = int(elem["newsId"]),
      content     = content,
      office      = elem["name"],
      news_type   = elem["attr_name"],
      date        = elem["time"],
      is_pinned   = elem["top"],
      group       = group,
      keyword_ids = matched_keywords,
    )

    news_list.append(news)

  return news_list


def get_news_on_latest_date(group: str) -> tuple[str, list[News]]:
  """filters out news on the latest date.  

  Args :
    `group` : `"main"` or `"first_grade"`.  
  Returns :
    `latest_date` : str.  
    `news_on_latest_date` : list[`News`].  
  """

  news_list = get_news(group)
  latest_date = max(news.date for news in news_list)
  
  return latest_date, (news for news in news_list if news.date == latest_date)


def get_new_news(group: str) -> list[News]:
  """compares all the news on the latest date with the existing news from the database.\n
  if new news being found, updates the database.
  
  Args :
    `group` : `"main"` or `"first_grade"`.  
  Retruns :
    `news_on_latest_date` : list[`News`]
  """

  latest_date, news_on_latest_date = get_news_on_latest_date(group)
  doc_ref = db.collection(u"stats").document(group)

  news_ids_on_latest_date = db_get_ids_on_latest_date(latest_date, doc_ref)

  new_news = []
  for news in news_on_latest_date:
    if news.id in news_ids_on_latest_date:
      continue

    new_news.append(news)

  if new_news:
    db_update_news_ids([news.id for news in new_news], doc_ref)
  
  return new_news

