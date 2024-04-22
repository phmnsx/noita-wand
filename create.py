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
def create(title, image, author, spells, date, description, authorid):

    r = open('db.json', encoding="utf8")
    items = json.load(r)
    r.close()
    build["author-id"] = authorid
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
    
    f = open('dbusers.json', encoding="utf8")
    users = json.load(f)
    loop = 0
    for person in users:
        if person["id"] == authorid:
            users[loop]["builds"].append(id)
            break
        loop += 1
    else:
        return "Error 6: User not found"
    f.close()
    f = open('dbusers.json', 'w', encoding="utf8")
    json.dump(users, f, indent=2, sort_keys=True)
    f.close()
    f = open('db.json', 'w', encoding="utf8")
    json.dump(items, f, indent=2, sort_keys=True)
    f.close()

create(title, image, author, spells, date, description, "2")
