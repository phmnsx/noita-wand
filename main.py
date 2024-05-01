import json
users={
    "id": "",
    "img": "",
    "name": "",
    "builds": [],
    "liked-posts": []

}
report={
    "user": "",
    "report": "",
    "reported": "",
    "post-id": "",
    "date" : ""
}
comment={
    "author-id": "",
    "content": "",
    "is-deleted": 0,
    "parent-id": 0,
    "build-id": 0,
    "id": 0,
    "layer" : 0,
    "date" : ""
}
build={
    "title": "",
    "image": "",
    "author": "",
    "author-id": "",
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
        if item["size"] <= size and set(spell).issubset(item["spells"]):
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
    r.close()
    result = []
    for item in search:
        if name.lower() in item["title"].lower():
            result.append(item)
    if len(result) == 0:
        return "No results."
    else:
        return result

def create_comment(parent_id, type, content, parent_layer, author_id, date, build_id):
    new_comment = {}
    if len(content.replace(" ", "")) == 0:
        return "Error 4: No text inserted."
    if len(content) > 400:
        return "Error 5: Comment too long."
    r = open('latest.txt', encoding="utf8")
    id = int(json.load(r))
    r.close()
    new_comment["id"] = id
    r = open('latest.txt', 'w', encoding="utf8")
    id = id + 1
    r.write(str(id))
    r.close()
    if type == "build":
        new_comment["layer"] = 0
    elif type == "comment":
        new_comment["layer"] = parent_layer + 1
    new_comment["content"] = content
    new_comment["parent-id"] = parent_id
    new_comment["id"] = id
    new_comment["build-id"] = build_id
    new_comment["author-id"] = author_id
    new_comment["date"] = date
    new_comment["is-deleted"] = False
    f = open('dbc.json', encoding="utf8")
    ccomments = json.load(f)
    f.close()
    ccomments.append(new_comment)
    f = open('dbc.json', 'w', encoding="utf8")
    json.dump(ccomments, f, indent=2, sort_keys=True)
    f.close()

def edit_comment(comment_id, content):
    if len(content.replace(" ", "")) == 0:
       return "Error 4: No text inserted."
    if len(content) > 400:
        return "Error 5: Comment too long."
    f = open('dbc.json', encoding="utf8")
    comments = json.load(f)
    f.close()
    loop = 0
    for comment in comments:
        if comments[loop]["id"] == comment_id:
            comments[loop]["content"] = content
            break
        loop += 1
    else:
        return "Error 8: Comment not found."
    f = open('dbc.json', 'w', encoding="utf8")
    json.dump(comments, f, indent=2, sort_keys=True)
    f.close()

def delete_comment(comment_id):
    f = open('dbc.json', encoding="utf8")
    comments = json.load(f)
    f.close()

    loop = 0
    for comment in comments:
        if comments[loop]["id"] == comment_id:
            comments[loop]["is-deleted"] = True
            break
        loop += 1
    else:
        return "Error 8: Comment not found."
    
    f = open('dbc.json', 'w', encoding="utf8") 
    json.dump(comments, f, indent=2, sort_keys=True)
    f.close()

def return_comments():
    f = open('dbc.json', encoding="utf8")
    comments = json.load(f)
    f.close()
    return comments

def create_report(post_id, user, reported, reason, date):
    new_report = {}
    if len(reason.replace(" ", "")) == 0:
        return "Error 4: No text inserted."
    if len(reason) > 400:
        return "Error 6: Reason too long."
    new_report["post-id"] = post_id
    new_report["user"] = user
    new_report["reported"] = reported
    new_report["reason"] = reason
    new_report["date"] = date
    f = open('dbr.json', 'w', encoding="utf8")
    json.dump(new_report, f, indent=2, sort_keys=True)
    f.close()

def like(user_id, post_id):
    f = open('dbusers.json', encoding="utf8")
    users = json.load(f)
    f.close()
    f = open('db.json', encoding="utf8")
    builds = json.load(f)
    f.close()
    loop = 0
    loopb = 0
    for build in builds:
        if builds[loopb]["id"] == post_id:
            break
        loopb += 1

    for person in users:
        if users[loop]["id"] == user_id:
            break
        loop += 1
    print(loopb)
    if post_id in users[loop]["liked-posts"]:
        users[loop]["liked-posts"].remove(post_id)
        builds[loopb]["likes"] -= 1
    else:
        users[loop]["liked-posts"].append(post_id)
        builds[loopb]["likes"] += 1
    
    f = open('dbusers.json', 'w', encoding="utf8")
    json.dump(users, f, indent=2, sort_keys=True)
    f.close()
    f = open('db.json', 'w', encoding="utf8")
    json.dump(builds, f, indent=2, sort_keys=True)
    f.close()

def get_user(user_id):
    f = open('dbusers.json', encoding="utf8")
    users = json.load(f)
    f.close()
    loop = 0
    for person in users:
        if users[loop]["id"] == user_id:
            break
        loop += 1
    else:
        return "User not found."
    return users[loop]

def create_user(id, name, img):
    f = open('dbusers.json', encoding="utf8")
    users = json.load(f)
    f.close()
    newUser = {
    "id": "",
    "name": "",
    "img": "",
    "builds": [],
    "liked-posts": []
    }
    
    newUser["id"] = id
    newUser["name"] = name
    newUser["img"] = img

    users.append(newUser)
    f = open('dbusers.json', 'w', encoding="utf8")
    json.dump(users, f, indent=2, sort_keys=True)
    f.close()

def get_comments(id):
    f = open("dbc.json", encoding="utf8")
    comments = json.load(f)
    f.close()
    comments.reverse()
    result = []
    for comment in comments:
        if comment["build-id"] == id:
            result.append(comment)
    return result

def get_comments_id(id):
    f = open('dbc.json', encoding="utf8")
    comments = json.load(f)
    f.close()
    comments.reverse()
    for comment in comments:
        if comment["id"] == id:
            return comment
    else:
        return "Comment not found"

def search_spell(name):
    f = open('static/spells.json', encoding="utf8")
    spells = json.load(f)
    f.close()
    result = []
    for spell in spells:
        if name.lower() in spell["title"].lower():
            result.append(spell)
    if len(result) == 0:
        return "No spells found :("
    else:
        return result