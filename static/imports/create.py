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
title = "dd"
image = 0
author = "dddd"
spells = ["spark" , "damage"]
date = "dddd"
description = "very simple spark damage ! so fun !"
def create(title, image, author, spells, date, description):

    r = open('db.json', encoding="utf8")
    items = json.load(r)
    r.close()

    build["title"] = title
    build["image"] = image
    build["author"] = author
    r = open('latest.txt', encoding="utf8")
    id = int(json.load(r))
    r.close()
    build["id"] = id
    r = open('latest.txt', 'w', encoding="utf8")
    id = id + 1
    r.write(str(id))
    r.close()
    build["spells"] = spells
    build["size"] = len(build["spells"])
    build["date"] = date
    build["description"] = description
    items.append(build)
    f = open('db.json', 'w', encoding="utf8")
    json.dump(items, f, indent=2, sort_keys=True)
    f.close()

create(title, image, author, spells, date, description)
