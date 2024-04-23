import json
build={
    "title": "",
    "image": "",
    "id": 0,
    "spells": [],
    "size": 0,
    "likes": 0,
    "description": "",
    "date": ""
}
def create(title, image, spells, date, description, authorid):

    r = open('db.json', encoding="utf8")
    items = json.load(r)
    r.close()
    build["author-id"] = authorid
    build["title"] = title
    build["image"] = image
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

def get_builds():
    f = open('db.json', encoding="utf8")
    builds = json.load(f)
    f.close
    return builds

def edit_build(title, image, description, id):
    f = open('db.json', encoding="utf8")
    builds = json.load(f)
    f.close
    loop = 0
    for build in builds:
        if builds[loop]["id"] == id:
            break
    else:
        return "Error 10: Build not found."
    builds[loop]["title"] = title
    builds[loop]["image"] = image
    builds[loop]["description"] = description
    f = open('db.json', 'w', encoding="utf8")
    json.dump(builds, f, indent=2, sort_keys=True)
    f.close()

def delete_build(id):
    f = open('db.json', encoding="utf8")
    builds = json.load(f)
    f.close
    loop = 0
    for build in builds:
        if builds[loop]["id"] == id:
            break
    else:
        return "Error 10: Build not found."
    builds.pop(loop)
    f = open('db.json', 'w', encoding="utf8")
    json.dump(builds, f, indent=2, sort_keys=True)
    f.close()
