import create, spells, main

class formatSpell:
    def toCssType(self, spell):
        match spell['Type']:
            case "Projectile":
                return 'type-projectile'
            case "Static projectile":
                return 'type-static-projectile'
            case "Passive":
                return 'type-passive'
            case "Utility":
                return 'type-utility'
            case "Projectile modifier":
                return 'type-modifier-projectile'
            case "Material":
                return 'type-material'
            case "Multicast":
                return 'type-multicast'
            case "Other":
                return 'type-other'

    def toHTML(self, spell):
        return f"""<div class="pi-image spell-icon-sm" style="background-image: url(/static/img/spells{spell['img']})"></div>"""
        
class formatBuild:
    def searchPage(self, page: int):
        BUILDS = create.get_builds()
        if page == 0:
            MIN_PAGE = 0
        else:
            MIN_PAGE = 1+10*page

        if MIN_PAGE > len(BUILDS):
            return "Invalid Page"
        if len(BUILDS) > 10*page+10:
            MAX_PAGE = 10*page+10
        else:
            MAX_PAGE = len(BUILDS)

        spell_form = []
        builds = BUILDS[MIN_PAGE:MAX_PAGE]
        for bld in builds:
            for id in bld['spells']:
                try:
                    spell = spells.get_spell(id)
                    spell_form.append(spell)
                    spell_form[len(spell_form)-1]['css_type'] = fmts.toCssType(spell)
                    spell_form[len(spell_form)-1]['img_html'] = fmts.toHTML(spell)
                except:
                    print("lol")
            
            bld['spells'] = spell_form
            spell_form = []
            bld['author'] = main.get_user(bld['author-id'])
            bld['comments'] = main.get_comments(bld['id'])

            for cmt in bld['comments']:
                cmt['author'] = main.get_user(cmt['author-id'])
        
        return builds
        
fmts = formatSpell()