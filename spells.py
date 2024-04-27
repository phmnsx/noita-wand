import json

def get_spell(id):
    f = open('static/spells.json', encoding="utf8")
    spells = json.load(f)
    f.close
    for spell in spells:
        if spell["ID"] == id:
            return spell
    else:
        return "Error 11: Spell not found."