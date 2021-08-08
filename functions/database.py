import os
import logging
from dataclasses import dataclass
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore import Client, DocumentSnapshot
from google.cloud.firestore_v1.document import DocumentReference

import dotenv
dotenv.load_dotenv()

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
  blocked_keyword_ids: list[int]
  groups: list[str]


def db_get_all_nowotify() -> list[Nowotify]:
  """returns `list[Nowotify]`"""

  docs : list[DocumentSnapshot] = db.collection(u"links").get()
  logging.info(f"[DB]fetched all nowotifys from the database.({len(docs)} in total)")

  return [
    Nowotify(
      type        = doc.get("type"),
      data        = doc.get("data"),
      groups      = doc.get("group"),
      only_pinned = doc.get("only_pinned"),
      blocked_keyword_ids = doc.get("blocked_keyword_ids"),
    )
  for doc in docs]


def db_get_ids_on_latest_date(latest_date: str, doc_ref: DocumentReference) -> list[str]:
  """returns a list of ids on the latest date."""

  doc = doc_ref.get()

  if doc.get("date") != latest_date:
    doc_ref.set({
      "date": latest_date,
      "news_ids": []
    })
    doc = doc_ref.get()

  return doc.get("news_ids")


def db_update_news_ids(ids: list[str], doc_ref: DocumentReference) -> None:
  """updates the database with the new ids."""

  doc_ref.update({
    "news_ids": firestore.firestore.ArrayUnion(ids)
  })
  logging.info(f"[DB]updated new news ids.({','.join(map(str, ids))})")

