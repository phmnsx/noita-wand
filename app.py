from flask import Flask, jsonify, flash, redirect, render_template, request, current_app
from flask import session as login_session
import requests
import json, random, string

import create
import main
from static.imports.credentials import client_id, client_secret
from helpers import login_required

app = Flask(__name__)
app.secret_key = "JKGDhsMBGOLZinsjz0GCvNpbZ5riGBzG"

authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'
request_url = 'https://api.github.com'

@app.route("/")
def index():
    resp = {}
    if 'access_token' in login_session:
        if 'user' not in login_session:
            access_token_url = request_url + '/user'
            headers = {
                'Authorization': "Bearer " + login_session['access_token']
                }
        
            r = requests.get(access_token_url, headers=headers)

            try:
                resp = r.json()
                login_session['user'] = resp
                if main.get_user(login_session['user']['id']) == "User not found.":
                    main.create_user(login_session['user']['id'], login_session['user']['login'])
            except AttributeError:
                app.logger.debug('error getting username from github, whoops')
                return "I don't know who you are; I should, but regretfully I don't", 500
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template("index.html", state=state, login_session=login_session)

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
def searchBuild():
    return render_template("index.html")

@app.route("/builds/create", methods=["GET", "POST"])
@login_required
def createBuild():
    f = open("static\spells.json", encoding="utf8")
    SPELLS = json.load(f)
    f.close()   

    if request.method == "POST":
        print("tata")
        currentSpells = []

        for spls in list(map(int,request.form.get('spell-list').split(","))):
            currentSpells.append(SPELLS[spls-1])

        create.create(request.form.get('build-title'), 
                  request.form.get('build-icon'), 
                  "EU", 
                  currentSpells,
                  request.form.get('build-date'), 
                  request.form.get('build-description'))
        
    for spl in SPELLS:
        match spl['Type']:
            case "Projectile":
                spl['css_type'] = 'type-projectile'

            case "Static projectile":
                spl['css_type'] = 'type-static-projectile'

            case "Passive":
                spl['css_type'] = 'type-passive'

            case "Utility":
                spl['css_type'] = 'type-utility'

            case "Projectile modifier":
                spl['css_type'] = 'type-modifier-projectile'
                
            case "Material":
                spl['css_type'] = 'type-material'

            case "Multicast":
                spl['css_type'] = 'type-multicast'
                
            case "Other":
                spl['css_type'] = 'type-other'
        spl['img_html'] = f"""<div class="pi-image spell-icon-sm" style="background-image: url(/static/img/spells{spl['img']})"></div>"""
    
    return render_template("formBuild.html", spells=SPELLS, login_session=login_session)
