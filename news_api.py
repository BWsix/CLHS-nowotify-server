import logging
from database import db, db_get_ids_on_latest_date, db_update_news_ids
import os
import json
import requests
from dataclasses import dataclass, field
from keywords import KEYWORD_TABLE


API_ENTRY = "https://www.clhs.tyc.edu.tw/ischool/widget/site_news/news_query_json.php"
API_HEADER = {'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
API_BODY = "field=time&order=DESC&pageNum=0&maxRows={0}&keyword=&uid="+os.environ["uid"]+"&tf=1&auth_type=user&use_cache=1"

@dataclass(frozen=True, eq=True, order=True)
class News:
  """News. will be compared based on only publish/update date"""
  
  id: int         = field(compare=False)
  content: str    = field(compare=False)
  office: str     = field(compare=False)
  news_type: str  = field(compare=False)
  date: str       
  is_pinned: bool = field(compare=False)
  keyword_ids: list[int] = field(compare=False, default_factory=list)

  def __str__(self):
    return f"({self.date}){self.id} :{'pinned' if self.is_pinned else ''} {self.content}"


def get_news(data_count: int = 40) -> list[News]:
  """returns latest news from school.(return 40 news by default)"""

  res = requests.post(API_ENTRY, headers=API_HEADER, data=API_BODY.format(data_count))
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
      int(elem["newsId"]),
      content,
      elem["name"],
      elem["attr_name"],
      elem["time"],
      elem["top"],
      matched_keywords,
    )

    news_list.append(news)

  return news_list


def get_news_on_latest_date() -> tuple[str, list[News]]:
  """returns a tuple[`latest date`,`list[news on that day]`]"""

  news_list = get_news()
  latest_date = max(news_list).date

  return latest_date, [news for news in news_list if news.date == latest_date]


def get_new_news() -> list[News]:
  """returns a list of new news on the latest date."""

  latest_date, news_on_latest_date = get_news_on_latest_date()
  doc_ref = db.collection(u"stats").document(u"news")

  news_ids_on_latest_date = db_get_ids_on_latest_date(latest_date, doc_ref)

  new_news = []
  for news in news_on_latest_date:
    if news.id in news_ids_on_latest_date:
      continue

    new_news.append(news)

  if new_news:
    db_update_news_ids([news.id for news in new_news], doc_ref)
  
  return new_news

