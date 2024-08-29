import pandas as pd

spells = pd.read_json('.\spells\spells.json')

def search_spell(spell_name):
    try:
        query_search = "name == '" + spell_name + "'"
        spell = spells.query(query_search)
        print(spell)
        if spell.size > 0:
            return spell
        else:
            df = pd.DataFrame()
            df["name"] = spell_name + " not found"
            return df
    except Exception as e:
        print(e)
        return "Error"