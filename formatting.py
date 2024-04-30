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
        return f"""
        <div 
            class="pi-image spell-icon-sm" 
            style="background-image: url(/static/img/spells{spell['img']})"
            data-bs-toggle="popover" 
            data-bs-trigger="hover focus" 
            tabindex="0"
            data-bs-html="true"
            data-bs-placement="top"
            data-bs-content="<div class='n-box' style='justify-content:center; background-color: rgba(0,0,0,1);'><div style='display:flex; flex-direction:column;'><span class='np-font'><b>{spell['title']}</b></span>                    
                        <span class='np-font'>{spell['description']}</span>
                        
                        <span class='np-font'>Type:</span> <span class='np-font'>{spell['Type']}</span></div></div>">
        </div>
        """
        
class formatBuild:
    COMMENTS = []
    def searchPage(self, page: int, search=None, spells_list=[], slots=0, user_id=None, type_user=""):
        if search != None:
            BUILDS = main.search_name(search)
        elif len(spells_list) != 0:
            BUILDS = main.search_blind(slots, spells_list)
        elif user_id != None:
            if type_user == "LIKED":
                BUILDS = create.liked_builds(user_id)
            elif type_user == "CREATED":
                BUILDS = create.user_builds(user_id)
        else:
            BUILDS = create.get_builds()
        
        next_page = False

        if type(BUILDS) == list:        
            if page == 0:
                START_POINT = 0
            else:
                START_POINT = 10*page

            if START_POINT > len(BUILDS):
                return "No results.", next_page
            
            
            if len(BUILDS) > 10*page+10:
                END_POINT = 10*page+10
                next_page = True
            else:
                END_POINT = len(BUILDS)

            spell_form = []
            builds = BUILDS[START_POINT:END_POINT]

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
                comments = main.get_comments(bld['id'])

                for cmt in comments:
                    cmt['author'] = main.get_user(cmt['author-id'])

                self.COMMENTS = comments

                comment_tree = []
                for record in self.COMMENTS:
                    if record['parent-id'] == 0: # if this is the start of a tree
                        comment_tree.append(self.create_tree(record))

                bld['comments'] = comment_tree

                lista = []
                for cmt in comment_tree:
                    lista.append(cmt)
                    if len(cmt['children']) != 0: 
                        lista.extend(self.get_children(cmt['children']))

                bld['comments'] = lista
        else:
            return "No results.", next_page
        return builds, next_page

    def create_tree(self,parent):
        parent['children'] = []
        for record in self.COMMENTS:
            if record['parent-id'] == parent['id']:
                parent['children'].append(self.create_tree(record))
        return parent

    def get_children(self,child):
        childs = []
        for record in child:
            childs.append(record)
            if len(record['children']) != 0: 
                    childs.extend(self.get_children(record['children']))
        return childs

fmts = formatSpell()