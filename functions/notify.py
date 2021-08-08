import logging
import requests
from line_notify import LineNotify

from .news_api import News
from .database import Nowotify, db_get_all_nowotify

NEWS_LINK = "https://www.clhs.tyc.edu.tw/ischool/public/news_view/show.php?nid={0}"


def create_notify_contents(news: News) -> tuple[str, str]:
  """return a tuple of contents : `[content_discord, content_line]`"""
  
  content_discord = {
    "embeds": [{
      "title": f"{news.office} {news.news_type}" + ( " **(重要通知 !)**" if news.is_pinned else ""),
      "description": f"發布日期 : {news.date}\n公告內容 :\n{news.content}",
      "url": NEWS_LINK.format(str(news.id)),
      "color": 14177041 if news.is_pinned else 0,
      "author": {
        "name": "CLHS nowotify",
        "url": "https://bwsix.github.io/CLHS-nowotify",
      },
    }],
  }

  content_line = f"{news.office} {news.news_type}"
  if(news.is_pinned): content_line += " *(重要通知 !)*"
  content_line += f"""\n發布日期 : {news.date}
公告內容 :
{news.content}

前往學校官網查看詳細內容 :
{NEWS_LINK.format(str(news.id))}
"""

  return content_discord, content_line


def notify_discord_user(webhook_url: str, content: str) -> None:
  """sends `content` to a discord channel using the `webhook_url`"""
  
  try:
    requests.post(webhook_url, json=content)
    logging.info(f"[notify] a discord channel gets notified")
  except:
    logging.warn(f"[notify] failed to send message to discord channel, webhook url: {webhook_url}")
    pass
    # please help me out if you have any idea how to properly handle any potentail errors, thanks!


def notify_line_user(token: str, content: str) -> None:
  """send `content` to a line group using the `token`"""
  
  try:
    LineNotify(token).send(content)
    logging.info(f"[notify] a line group gets notified")
  except:
    logging.warn(f"[notify] failed to send message to line group, lotify token: {token}")
    pass
    # please help me out if you have any idea how to properly handle any potentail errors, thanks!


def notify_users(news: News, all_nowotify: list[Nowotify]) -> None:
  """notify all users.\n
  if `only_pinned` is true, the user will not gets notified by unpinned news"""

  content_discord, content_line = create_notify_contents(news)

  logging.info(f"[notify]started notifying all users.(news id {news.id})")
  for nowotify in all_nowotify:
    if not news.group in nowotify.groups:
      continue
    
    if nowotify.only_pinned and not news.is_pinned:
      continue
      
    if any(map(lambda id: id in nowotify.blocked_keyword_ids, news.keyword_ids)):
      continue

    if nowotify.type == "discord":
      notify_discord_user(nowotify.data, content_discord)
    if nowotify.type == "line":
      notify_line_user(nowotify.data, content_line)


def send_system_message(title: str, message: str) -> None:
  """sends message to all users."""

  content_line = f"[系統公告] {title}\n{message}"
  content_discord = {
    "embeds": [{
      "title": f"[系統公告] {title}",
      "description": message,
      "url": "https://bwsix.github.io/CLHS-nowotify",
      "color": 14177041,
      "author": {
        "name": "CLHS nowotify",
        "url": "",
      },
    }],
  }

  nowotifys = db_get_all_nowotify()

  for nowotify in nowotifys:
    if nowotify.type == "discord":
      notify_discord_user(nowotify.data, content_discord)
    if nowotify.type == "line":
      notify_line_user(nowotify.data, content_line)

