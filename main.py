import json
report={
    "user": "",
    "report": "",
    "reported": "",
    "post-id": "",
}
comment={
    "author": "",
    "content": "",
    "parent-id": 0,
    "id": 0,
    "layer" : 0
}

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

def create_comment(post_id, type, content, parent_layer, author):
    new_comment = {}
    r = open('latest.txt', encoding="utf8")
    id = int(json.load(r))
    r.close()
    new_comment["id"] = id
    r = open('latest.txt', 'w', encoding="utf8")
    id = id + 1
    r.write(str(id))
    r.close()
    if type == "post":
        new_comment["layer"] = 0
    elif type == "comment":
        new_comment["layer"] = parent_layer + 1
    new_comment["content"] = content
    new_comment["parent-id"] = post_id
    new_comment["id"] = id
    new_comment["author"] = author
    f = open('dbc.json', 'w', encoding="utf8")
    json.dump(new_comment, f, indent=2, sort_keys=True)
    f.close()

def create_report(post_id, user, reported, reason):
    new_report = {}
    new_report["post-id"] = post_id
    new_report["user"] = user
    new_report["reported"] = reported
    new_report["reason"] = reason
    f = open('dbr.json', 'w', encoding="utf8")
    json.dump(new_report, f, indent=2, sort_keys=True)
    f.close()
