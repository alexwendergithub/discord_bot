import random

converter = {
    'FOR':"forca",
    "ATL":"atletismo",
    "BON":"bonus__de_proeficiencia"
}

import random

def multiRolls(num_dices,num_faces):
    result = []
    for i in range(num_dices):
        result.append(random.randint(1,num_faces))
    return result

def splitString(string):
    stringArr = string.split("+")
    mod = 0
    rollsArr = []
    result = []

    for i in stringArr:
        if i.isdigit():
            mod += int(i)
        else:
            rollsArr.append(i)
    
    return [rollsArr,mod]
    
def processString(string):
    stringArr = splitString(string)
    mod = stringArr[1]
    rollsArr = stringArr[0]

    processedRollsArr = []
    for roll in rollsArr:
        rollExpression = roll.split("d")
        num_dice = int(rollExpression[0])
        num_faces = int(rollExpression[1])
        processedRollsArr.append((num_dice, num_faces))              
    
    result = []
    for whathever in processedRollsArr:
        result.append(multiRolls(whathever[0],whathever[1]))

    return processedRollsArr

def mountString(string, processedDicesArr):
    stringArr = string.split("+")
    mod = splitString(string)[1]

    results = []
    for dice in processedDicesArr:
        results.append(multiRolls(dice[0],dice[1]))

    totalSum = sum(sum(row) for row in results)

    arrOfResults = []
    for i in range(len(results)):
        strOfResult = "["
        for j in range(len(results[i])):
            if results[i][j] == 1 or results[i][j] == processedDicesArr[i][1]:
                strOfResult += f"**{results[i][j]}**"
            else:
                strOfResult += f"{results[i][j]}"
            
            if j < len(results[i]) - 1:
                strOfResult += ", "
        strOfResult += "]" 
        arrOfResults.append(strOfResult)

        k = 0
    for i in range(len(stringArr)):

        if 'd' in stringArr[i]:
            stringArr[i] = arrOfResults[k] + stringArr[i]        
            k += 1
    stringArr[0] = f"`{totalSum+mod}` <- " + stringArr[0]
    final = " + ".join(stringArr)
    return final

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
        return "Error" 

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

