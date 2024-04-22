import json

build={
    "title": "",
    "image": "",
    "author": "",
    "id": 0,
    "spells": [],
    "size": 0,
    "likes": 0,
    "description": "",
    "date": ""
}

def search_blind(size, spell):
    if len(spell) == 0:
        return "Error 1: No spells selected"
    if size <= 0:
        return "Error 2: Invalid wand capacity (Must be more than 0)"
    if size > 26:
        return "Error 2: Invalid wand capacity (Must be less than 26)"
    r = open('db.json', encoding="utf8")
    search = json.load(r)
    r.close()
    result = []
    for item in search:
        if item["size"] <= size and set(item["spells"]).issubset(set(spell)):
            result.append(item)
    if len(result) == 0:
        return "No results."
    else:
        return result

def search_name(name):
    if len(name) == 0:
        return "Error 3: No name inserted."
    r = open('db.json', encoding="utf8")
    search = json.load(r)
    r.close
    result = []
    for item in search:
        if set(item["title"]).issubset(set(name)):
            result.append(item)
    if len(result) == 0:
        return "No results."
    else:
        return result
