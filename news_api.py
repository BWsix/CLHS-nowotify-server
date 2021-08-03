import os
import json
import requests
from dataclasses import dataclass

# from dotenv import load_dotenv
# load_dotenv()

API_ENTRY = "https://www.clhs.tyc.edu.tw/ischool/widget/site_news/news_query_json.php"
API_HEADER = {'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
API_BODY = "field=time&order=DESC&pageNum=0&maxRows={0}&keyword=&uid="+os.environ["uid"]+"&tf=1&auth_type=user&use_cache=1"


@dataclass
class News:
  id: int         # 27495
  content: str    # 本校110學年第2次代理教師甄選簡章公告
  office: str     # 人事室
  news_type: str  # 公告
  date: str       # 2021/07/28
  is_pinned: bool # 0 or 1 

  def __str__(self):
    return f"({self.date}){self.id} :{'pinned' if self.is_pinned else ''} {self.content}"


def get_news(data_count: int = 40) -> list[News]:
  """returns latest news from school.(return 40 news by default)"""

  res = requests.post(API_ENTRY, headers=API_HEADER, data=API_BODY.format(data_count))
  data = json.loads(res.text)[1:]

  news_list: list[News] = []

  for elem in data:
    news_list.append(News(
      int(elem["newsId"]),
      elem["title"],
      elem["name"],
      elem["attr_name"],
      elem["time"],
      elem["top"],
    ))

  return news_list

