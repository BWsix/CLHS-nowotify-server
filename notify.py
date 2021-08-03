import logging
import requests
from line_notify import LineNotify
from news_api import News
from database import Nowotify

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
  except:
    logging.warn(f"[notify_discord] failed to send message to {webhook_url}")
    pass
    # please help me out if you have any idea how to properly handle any potentail errors, thanks!


def notify_line_user(token: str, content: str) -> None:
  """send `content` to a line group using the `token`"""
  
  try:
    LineNotify(token).send(content)
  except:
    logging.warn(f"[notify_line] failed to send message to {token}")
    pass
    # please help me out if you have any idea how to properly handle any potentail errors, thanks!


def notify_users(news: News, all_nowotify: list[Nowotify]) -> None:
  """notify all users.\n
  if `only_pinned` is true, the user will not gets notified by unpinned news"""

  content_discord, content_line = create_notify_contents(news)

  for nowotify in all_nowotify:
    if nowotify.only_pinned and not news.is_pinned:
      continue

    if nowotify.type == "discord":
      notify_discord_user(nowotify.data, content_discord)
    if nowotify.type == "line":
      notify_line_user(nowotify.data, content_line)

