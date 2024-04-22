from flask import Flask, flash, redirect, render_template, request, session, current_app
import json
import static.imports.create as db

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/builds/search")
def searchBuild():
    return render_template("index.html")

@app.route("/builds/create", methods=["GET", "POST"])
def createBuild():
    f = open("static\spells.json", encoding="utf8")
    SPELLS = json.load(f)
    f.close()   

    if request.method == "POST":
        print("tata")
        currentSpells = []

        for spls in list(map(int,request.form.get('spell-list').split(","))):
            currentSpells.append(SPELLS[spls-1])

        db.create(request.form.get('build-title'), 
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
        spl['img_html'] = f"""<div class="pi-image spell-icon-sm" style="background-image: url(/static/img/spells{spl['img']}"></div>"""
    
    return render_template("formBuild.html", spells=SPELLS)
