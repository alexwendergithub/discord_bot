import random

converter = {
    'FOR':"forca",
    "ATL":"atletismo",
    "BON":"bonus__de_proeficiencia"
}

#function responsable for rolling dices it rolls any number of dices and add they results
#send a display message as a result
#return message format: RESULT <- [Dice rolls] (Number of rolls)d(Dice Type) + Constant + ...
def rolling(dices):
    try:
        result = 0
        result_text = ""
        dices = dices.split("+")
        for dice in dices:
            dice = dice.split("d")
            if len(dice)>1:
                if result_text != "":
                    result_text = result_text + "+ "
                result_text_aux = "["
                for x in range(int(dice[0])):
                    roll = random.randint(1,int(dice[1]))
                    result = result + roll
                    if roll == int(dice[1]) or roll == 1:
                        result_text_aux = result_text_aux + " **" + str(roll) + "**,"
                    else:
                        result_text_aux = result_text_aux + str(roll) + ","
                result_text_aux = result_text_aux[:-1] + "]"
                result_text = result_text + result_text_aux +dice[0] + "d" + dice[1]+ " "
            else:
                if result_text != "":
                    result_text = result_text + "+ "
                result = result + int(dice[0])
                result_text = result_text + dice[0] + " "
        result_text = "`" + str(result) + "`" + " <- " + result_text 
        print(result_text)
        return result_text
    except Exception as e:
        print(e)
        return "Error"

#rola uma estatistica de um personagem especifico, the characther json follows the char.json example
def get_stat_char(char,stat_acro):
    try:
        modifier = 0
        dice_to_roll = ""
        #converter acronimo para Nome
        stat_name = converter[stat_acro]
        #verificar nome da estatistica no personagem
        if stat_name in char.keys():
            stat = char[stat_name]
        elif stat_name in char["estatisticas"].keys():
            stat = char["estatisticas"][stat_name]
        elif stat_name in char["estatisticas_derivadas"].keys():
            stat = char["estatisticas_derivadas"][stat_name]
        elif stat_name in char["ataques"].keys():
            stat = char["ataques"][stat_name]
        else:
            return "Stat não encontrado:"+ stat_name

        #pegar dado base(se tiver)
        if "base_stat" in stat.keys():
            modifier = modifier + stat["base_stat"]
        #rolar o tipo de dado e adicionar ao dado base
        try:
            dice_to_roll = stat["dice_type"]
        except:
            return "falha ao encontrar tipo de dado para rolar"
        #adicionar modificadores se tiver
        if "modifiers" in stat.keys():
            modifier = modifier + getModifiers(char,stat["modifiers"])
        print(dice_to_roll)
        print(modifier)
        response = rolling(dice_to_roll + "+" + str(modifier))
    except Exception as e:
        print(e)
        return "Failed to roll dice" 

def getModifiers(char,modifiers):
    if type(modifiers) is str:
        if modifiers.isdigit():
            return int(modifiers)
    elif type(modifiers) is int:
        return modifiers
    aux = ""
    if "+" in modifiers:
        aux = modifiers.split("+")
        if not aux[0].isdigit():
            aux[0] = get_stat_char(char,aux[0])
        if not aux[1].isdigit():
            aux[1] = get_stat_char(char,aux[1])
        return aux[0]+aux[1]       
    elif "/" in modifiers:
        aux = modifiers.split("/")
        if not aux[0].isdigit():
            aux[0] = get_stat_char(char,aux[0])
        if not aux[1].isdigit():
            aux[1] = get_stat_char(char,aux[1])
        return aux[0]/aux[1]
    elif "*" in modifiers:
        aux = modifiers.split("*")
        if not aux[0].isdigit():
            aux[0] = get_stat_char(char,aux[0])
        if not aux[1].isdigit():
            aux[1] = get_stat_char(char,aux[1])
        return aux[0]*aux[1]
    else:
        return 0

