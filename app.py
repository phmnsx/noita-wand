from flask import Flask, jsonify, flash, redirect, render_template, request, current_app
from flask import session as login_session
import requests
import json, random, string

import create as build
import main
from static.imports.credentials import client_id, client_secret, app_secret_key
from helpers import login_required
import spells
import formatting

fmts = formatting.formatSpell()
fmtb = formatting.formatBuild()

app = Flask(__name__)
app.secret_key = app_secret_key

authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'
request_url = 'https://api.github.com'

COMMENT_POST = "build"
COMMENT_REPLY = "comment"


@app.route("/")
def index():
    if 'access_token' in login_session:
        if 'user' not in login_session:
            startUser()
        else:
            updateUser()
            
    return render_template("index.html", state=updateState(), login_session=login_session)

@app.route("/handleLogin", methods=["GET"])
def handleLogin():
    if login_session['state'] == request.args.get('state'):
        fetch_url = authorization_base_url + \
                    '?client_id=' + client_id + \
                    '&state=' + login_session['state'] + \
                    '&scope=user%20repo%20public_repo' + \
                    '&allow_signup=true'
        return redirect(fetch_url)
    else:
        return jsonify(invalid_state_token="invalid_state_token")

@app.route("/callback", methods=["GET", "POST"])
def callback():
    if request.args.get('state') != login_session['state']:
        return redirect('/')

    if 'code' in request.args:
        #return jsonify(code=request.args.get('code'))
        
        payload = {
            'client_id': client_id,
            'client_secret': client_secret,
            'code': request.args['code']
        }

        headers = {'Accept': 'application/json'}
        req = requests.post(token_url, params=payload, headers=headers)
        resp = req.json()

        if 'access_token' in resp:
            login_session['access_token'] = resp['access_token']
            return redirect('/')
        else:
            return jsonify(error="Error retrieving access_token"), 404
    else:
        return jsonify(error="404_no_code"), 404
    
@app.route("/logout")
def logout():
    login_session.clear()
    return redirect('/')

@app.route("/builds/search")
def searchBuild_main():
    return render_template("search.html", page=0, state=updateState(), login_session=login_session)

@app.route("/builds/search/<int:page>")
def searchBuild(page):
    return render_template("search.html", page=page, state=updateState(), login_session=login_session)

@app.route("/builds/searchBySpell")
def searchBySpell():
    f = open("static\spells.json", encoding="utf8")
    SPELLS = json.load(f)
    f.close()
    for spl in SPELLS:
        spl['css_type'] = fmts.toCssType(spl)
        spl['img_html'] = fmts.toHTML(spl)
    return render_template("searchbySpell.html", page=0, spells=SPELLS, state=updateState(), login_session=login_session)

@app.route("/builds/getRecentBuilds/<int:page>")
def getRecentBuilds(page):
    builds, next_page = fmtb.searchPage(page, search=None)
    if builds == "Invalid Page":
        return redirect("/builds/search")
    return render_template("buildResult.html",is_likes=False, page=page, next_page=next_page, builds=builds,state=login_session['state'],login_session=login_session)

@app.route("/builds/getBuildBySpell/<int:page>", methods=["GET", "POST"])
def getBuildBySpell(page):
    currentSpells = []
    f = open("static\spells.json", encoding="utf8")
    SPELLS = json.load(f)
    f.close()
    if len(request.json['spells']) != 0:    
        for spls in list(map(int,request.json['spells'].split(","))):
            currentSpells.append(SPELLS[spls-1]['ID'])
    else:
        return render_template("buildResult.html",is_likes=False, next_page=False,page=page, builds="No results.", state=login_session['state'],login_session=login_session)
        
    builds, next_page = fmtb.searchPage(page, search=None, spells_list=currentSpells, slots=request.json['slots'])

    if builds == "Invalid Page":
        return redirect("/builds/search")
    return render_template("buildResult.html",is_likes=False, next_page=next_page, page=page, builds=builds,state=login_session['state'],login_session=login_session)

@app.route("/builds/getBuildsbyTitle/<int:page>", methods=["GET", "POST"])
def getBuildsbyTitle(page):
    if request.method == "GET":
        builds, next_page = fmtb.searchPage(page, search=request.args.get('search'))
        return render_template("buildResult.html",is_likes=False,page=page, next_page=next_page, builds=builds,state=login_session['state'],login_session=login_session)
    else:
        return render_template("buildResult.html",is_likes=False,page=page, next_page=next_page, builds="No results.", state=login_session['state'], login_session=login_session)

@app.route("/builds/create", methods=["GET", "POST"])
@login_required
def createBuild():
    f = open("static\spells.json", encoding="utf8")
    SPELLS = json.load(f)
    f.close()   

    if request.method == "POST":
        currentSpells = []
        if len(request.form.get('spell-list')) != 0:
            for spls in list(map(int,request.form.get('spell-list').split(","))):
                currentSpells.append(SPELLS[spls-1]['ID'])
        else:
            return redirect("/")


        date = request.form.get('build-date')[:24]
        build.create(request.form.get('build-title'), 
                  request.form.get('build-icon'),  
                  currentSpells,
                  date, 
                  request.form.get('build-description'),
                  str(login_session['user']['id']))
        
        updateUser()
        return redirect(f"/user/{login_session['user']['id']}")
    
    for spl in SPELLS:
        spl['css_type'] = fmts.toCssType(spl)
        spl['img_html'] = fmts.toHTML(spl)

    #spell_type = ["Projectile","Static projectile", "Passive", "Utility", "Projectile modifier","Material", "Other", "Multicast"]
    
    #final_spells = []
    #for type in spell_type:
    #    for spl in SPELLS:
    #        if spl['Type'] == type:
    #            final_spells.append(spl)
    updateUser()
    return render_template("formBuild.html", spells=SPELLS, login_session=login_session)

@app.route("/addComment/<int:id>", methods=["GET","POST"])
@login_required
def sendComment(id):
    if request.method == "POST":
        date = request.json['date'][:24]
        main.create_comment(
            0,
            COMMENT_POST,
            request.json['comment'],
            0,
            str(login_session['user']['id']),
            date,
            id
        )
        updateUser()
        return "OK"
    else:
        return redirect('/')

@app.route("/addReply/<int:build_id>/<int:parent_id>", methods=["GET","POST"])
@login_required
def sendReply(build_id, parent_id):
    if request.method == "POST":
        parent_layer = main.get_comments_id(parent_id)['layer']
        date = request.json['date'][:24]
            
        main.create_comment(
            parent_id,
            COMMENT_REPLY,
            request.json['comment'],
            parent_layer,
            str(login_session['user']['id']),
            date,
            build_id
        )
            
        updateUser()
        return "OK"
    else:
        return redirect('/')

@app.route("/removeComment/<int:id_comment>", methods=["GET"])
@login_required
def removeComment(id_comment):
    if request.method == "GET":
        main.delete_comment(id_comment)
        updateUser()
        return 'OK'
    else:
        return redirect('/')

@app.route("/user/<string:id>")
def userPage(id):
    updateUser()
    user = main.get_user(id)
    return render_template("userPage.html", user=user, login_session=login_session)

@app.route("/updateLike/<int:id>", methods=["GET"])
@login_required
def likeBuild(id):
    if request.method == "GET":
        main.like(login_session['user']['id'], id)
        updateUser()
        return "ok"
    else:
        updateUser()
        return redirect('/')

@app.route("/getUserLikes/<string:id>/<int:page>", methods=["GET"])
def getUserLikes(id, page):
    builds, next_page = fmtb.searchPage(page, user_id=id, type_user="LIKED")
    return render_template("buildResult.html", is_likes=True, page=page, next_page=next_page, builds=builds,state=login_session['state'],login_session=login_session)

@app.route("/getUserBuilds/<string:id>/<int:page>", methods=["GET"])
def getUserBuilds(id, page):
    builds, next_page = fmtb.searchPage(page, user_id=id, type_user="CREATED")
    return render_template("buildResult.html", is_likes=False, page=page, next_page=next_page, builds=builds,state=login_session['state'],login_session=login_session)

@app.route("/deleteBuild/<int:build_id>", methods=["POST"])
@login_required
def deleteBuild(build_id):
    if request.method == "POST":
        if build.is_build_user(build_id, login_session['user']['id']):
            print(build_id)
            updateUser()
            print(build.delete_build(build_id))
            return "OK"
    else:
        return redirect('/')

def startUser():
    resp = {}
    access_token_url = request_url + '/user'
    headers = {
        'Authorization': "Bearer " + login_session['access_token']
        }
        
    r = requests.get(access_token_url, headers=headers)

    try:
        resp = r.json()
        id_str = str(resp['id'])

        if main.get_user(id_str) == "User not found.":
            main.create_user(
                id_str, 
                resp['login'], 
                resp['avatar_url']
            )

            login_session['user'] = main.get_user(id_str)
        else:
            login_session['user'] = main.get_user(id_str)
    except AttributeError:
        app.logger.debug('error getting username from github, whoops')
        return "I don't know who you are; I should, but regretfully I don't", 500

def updateUser():
    login_session['user'] = main.get_user(login_session['user']['id'])

def updateState():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return state