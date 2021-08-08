import json


with open("data/groups.json", "r", encoding="utf-8") as f:
  tmp_groups = json.load(f)

  UID_TABLE = {id:detail["data"] for id, detail in tmp_groups.items()}  

with open("data/keywords.json", "r", encoding="utf-8") as f:
  keyword_list = json.load(f)
  tmp_keyword_table: dict[int, list[str]] = {}

  for idx, keys in enumerate(keyword_list):
    tmp_keyword_table[idx] = keys[1:]

  KEYWORD_TABLE = tmp_keyword_table
