from flask import Flask, jsonify, flash, redirect, render_template, request, current_app
from flask import session as login_session
import requests
import json, random, string

import create
import main
from static.imports.credentials import client_id, client_secret
from helpers import login_required
import spells
import formatting

fmts = formatting.formatSpell()
fmtb = formatting.formatBuild()

app = Flask(__name__)
app.secret_key = "JKGDhsMBGOLZinsjz0GCvNpbZ5riGBzG"

authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'
request_url = 'https://api.github.com'

COMMENT_POST = "build"
COMMENT_REPLY = "comment"

def updateUser():
    resp = {}
    access_token_url = request_url + '/user'
    headers = {
        'Authorization': "Bearer " + login_session['access_token']
        }
        
    r = requests.get(access_token_url, headers=headers)

    try:
        resp = r.json()
        login_session['user'] = resp
        login_session['user']['id'] = str(login_session['user']['id'])
        id_str = login_session['user']['id']
        login_session['user']['liked-posts'] = main.get_user(id_str)['liked-posts']
        print(login_session['user']['liked-posts'])
        if main.get_user(id_str) == "User not found.":
                main.create_user(id_str, login_session['user']['login'], login_session['user']['avatar_url'])
    except AttributeError:
        app.logger.debug('error getting username from github, whoops')
        return "I don't know who you are; I should, but regretfully I don't", 500

@app.route("/")
def index():
    if 'access_token' in login_session:
        if 'user' not in login_session:
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
    builds = fmtb.searchPage(0)

    login_session['page-search'] = 0
    return render_template("search.html", page=0, state=updateState(), builds=builds,login_session=login_session)

@app.route("/builds/search/<int:page>")
def searchBuild(page):
    builds = fmtb.searchPage(page)

    if builds == "Invalid Page":
        return redirect("/builds/search")
    
    login_session['page-search'] = page
    return render_template("search.html", page=page, state=updateState(), builds=builds, login_session=login_session)

@app.route("/builds/create", methods=["GET", "POST"])
@login_required
def createBuild():
    f = open("static\spells.json", encoding="utf8")
    SPELLS = json.load(f)
    f.close()   

    if request.method == "POST":
        currentSpells = []

        for spls in list(map(int,request.form.get('spell-list').split(","))):
            currentSpells.append(SPELLS[spls-1]['ID'])

        date = request.form.get('build-date')[:24]
        create.create(request.form.get('build-title'), 
                  request.form.get('build-icon'),  
                  currentSpells,
                  date, 
                  request.form.get('build-description'),
                  str(login_session['user']['id']))
        
    for spl in SPELLS:
        spl['css_type'] = fmts.toCssType(spl)
        spl['img_html'] = fmts.toHTML(spl)
    updateUser()
    return render_template("formBuild.html", spells=SPELLS, login_session=login_session)

@app.route("/addComment/<int:id>", methods=["POST"])
@login_required
def sendComment(id):
    if request.method == "POST":
        if request.args.get('state') == login_session['state']:
            date = request.form.get('date')[:24]
            main.create_comment(
                0,
                COMMENT_POST,
                request.form.get('comment'),
                0,
                str(login_session['user']['id']),
                date,
                id
            )
            updateUser()
            if login_session['page-search'] > 0:
                return redirect("/builds/search/"+str(login_session['page-search'])+"#build-"+str(id))
            else:
                return redirect("/builds/search"+"#build-"+str(id))
        else:
            return redirect('/logout')
    else:
        return redirect('/')
        
@app.route("/removeComment/<int:id_comment>", methods=["GET"])
@login_required
def removeComment(id_comment):
    if request.method == "GET":
        if request.args.get('state') == login_session['state']:
            main.delete_comment(id_comment)
            
            id = request.args.get('buildID')
            updateUser()
            if login_session['page-search'] > 0:
                return redirect("/builds/search/"+str(login_session['page-search'])+"#build-"+str(id))
            else:
                return redirect("/builds/search"+"#build-"+str(id))
        else:
            return redirect('/logout')
    else:
        return redirect('/')

@app.route("/updateLike/<int:id>", methods=["GET"])
@login_required
def likeBuild(id):
    if request.method == "GET":
        if request.args.get('state') == login_session['state']:
            main.like(login_session['user']['id'], id)
            updateUser()
            if login_session['page-search'] > 0:
                return redirect("/builds/search/"+str(login_session['page-search'])+"#build-"+str(id))
            else:
                return redirect("/builds/search"+"#build-"+str(id))
        else:
            return redirect('/logout')
    else:
        updateUser()
        return redirect('/')

def updateState():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return state