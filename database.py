import os
import logging
from dataclasses import dataclass
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import Client, DocumentSnapshot
from news_api import News


# from dotenv import load_dotenv
# load_dotenv()

credential = {
  "type": os.environ['type'],
  "project_id": os.environ["project_id"],
  "private_key_id": os.environ["private_key_id"],
  "private_key": os.environ["private_key"],
  "client_email": os.environ["client_email"],
  "client_id": os.environ["client_id"],
  "auth_uri": os.environ["auth_uri"],
  "token_uri": os.environ["token_uri"],
  "auth_provider_x509_cert_url": os.environ["auth_provider_x509_cert_url"],
  "client_x509_cert_url": os.environ["client_x509_cert_url"],
}

cred = credentials.Certificate(credential)
firebase_admin.initialize_app(cred)
db: Client = firestore.client()


@dataclass
class Nowotify:
  type: str
  data: str
  only_pinned: bool


def db_get_last_id() -> int:
  """returns the latest news id in the database."""

  doc: DocumentSnapshot = db.collection(u"stats").document("news").get()

  return doc.get("last_id")


def db_update_last_id(id: int) -> None:
  """updates database with the given news id."""

  db.collection(u"stats").document("news").update({
    "last_id": id
  })


def db_get_new_news(news_list: list[News]) -> list[News]:
  """retruns a list of new `news`."""

  last_id = db_get_last_id()
  new_last_id = 0
  new_news: list[News] = []

  for news in news_list:
    if news.id <= last_id:
      continue

    logging.info(f"[db_get_new_news]:{news}")
    
    new_news.append(news)
    new_last_id = max(new_last_id, news.id)

  if new_last_id == 0:
    return []

  db_update_last_id(new_last_id)
  return new_news[::-1] # old -> new


def db_get_all_nowotify() -> list[Nowotify]:
  """returns `list[Nowotify]`"""

  docs : list[DocumentSnapshot] = db.collection(u"links").get()

  return [
    Nowotify(doc.get("type"), doc.get("data"), doc.get("only_pinned")) 
  for doc in docs]

