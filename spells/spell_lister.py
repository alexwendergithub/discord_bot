import pandas as pd

spells = pd.read_json('.\spells.json')

def search_spell(spell_name):
    try:
        query_search = "name == ," + spell_name + "'"
        spell = a.query(query_search)
        if spell.size > 0:
            return spell
        else:
            return "Not Found"
    except:
        return "Error"