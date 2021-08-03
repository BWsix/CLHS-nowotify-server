import logging
import requests
from news_api import News
from line_notify import LineNotify

NEWS_LINK = "https://www.clhs.tyc.edu.tw/ischool/public/news_view/show.php?nid={0}"


def notify_discord(news: News, webhooks: list[str]) -> None:
  """sends messages to discord users using discord webhook."""
  
  def create_request_data() -> dict:
    """return a dict with request data."""
    
    return {
      "embeds": [{
        "title": f"{news.office} {news.news_type}" + ( " **(重要通知 !)**" if news.is_pinned else ""),
        "description": f"發布日期 : {news.date}\n公告內容 :\n{news.content}",
        "url": NEWS_LINK.format(str(news.id)),
        "color": 14177041 if news.is_pinned else 0,
        "author": {
          "name": "CLHS nowotify",
          "url": "https://github.com/BWsix", # TODO change this url to github page after deploy
        },
      }],
    }
  
  request_data = create_request_data()

  for url in webhooks:
    try:
      requests.post(url, json=request_data)
    except:
      logging.warn(f"[notify_discord] failed to send message to {url}")
      pass
      # please help me out if you have any idea how to properly handle any potentail errors, thanks!


def notify_line(news: News, lotify_tokens: list[str]) -> None:
  """sends messages to line users using line notify."""

  def create_message() -> str:
    """creates message for line notify"""

    content = f"{news.office} {news.news_type}"
    if(news.is_pinned):
      content += " *(重要通知 !)*"
    content += f"""\n發布日期 : {news.date}
公告內容 :
{news.content}

前往學校官網查看詳細內容 :
{NEWS_LINK.format(str(news.id))}
"""

    return content

  message = create_message()

  for token in lotify_tokens:
    try:
      LineNotify(token).send(message)
    except:
      logging.warn(f"[notify_line] failed to send message to {token}")
      pass
      # please help me out if you have any idea how to properly handle any potentail errors, thanks!

