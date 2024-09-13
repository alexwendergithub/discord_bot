import random

converter = {
    'FOR':"forca",
    "ATL":"atletismo",
    "BON":"bonus__de_proeficiencia"
}

# recebe o numero de faces do dado e quantos dele rolar. Retorna uma lista do resultado de cada rolagem
def multiRolls(num_dices,num_faces):
    result = []
    for i in range(num_dices):
        result.append(random.randint(1,num_faces))
    return result

#recebe a string do dice e retorna uma lista com uma lista dos dados e outra com a soma dos modificadores
def splitString(string):
    stringArr = string.split("+")
    mod = 0
    rollsArr = []

    for element in stringArr:
        if element.isdigit():
            mod += int(element)
        else:
            rollsArr.append(element)
    
    return rollsArr, mod

# recebe a string do dice e retorna uma lista com tuplas sendo o primeiro elemento da tupla o numero de dados
# e o segundo elemento o numero de faces do dado   
def processString(string):
    rollsArr, mod = splitString(string)

    processedRollsArr = []
    for roll in rollsArr:
        rollExpression = roll.split("d")
        num_dice = int(rollExpression[0])
        num_faces = int(rollExpression[1])
        processedRollsArr.append((num_dice, num_faces))              

    return processedRollsArr

#  recebe a string do dice e uma lista dos dices ja em forma de inteiros. 
#  faz a rolagem, soma todas as rolagens e por fim cria a string atraves de iteradocoes sobre a lista de resultados.
#  retorna uma string no formato "f`{totalSum+mod}` <- [result]XdY + ... + mod + ... + [result]AdB "
def mountString(string, processedDicesArr):
    try:
            stringArr = string.split("+")
            mod = splitString(string)[1]

            results = [multiRolls(dice[0], dice[1]) for dice in processedDicesArr]
            totalSum = sum(sum(row) for row in results)

            arrOfResults = []
            for DicesIndex, rollSet in enumerate(results):
                strOfResult = "["

                for rollSetIndex, roll in enumerate(rollSet):
                    if roll == 1 or roll == processedDicesArr[DicesIndex][1]:
                        strOfResult += f"**{roll}**"
                    else:
                        strOfResult += f"{roll}"

                    if rollSetIndex < len(rollSet) - 1:
                        strOfResult += ", "
    
                strOfResult += "]"
                arrOfResults.append(strOfResult)

            resultIndex = 0
            for stringArrIndex, parts in enumerate(stringArr):

                if 'd' in parts:
                    stringArr[stringArrIndex] = f"{arrOfResults[resultIndex]}{parts}"        
                    resultIndex += 1

            stringArr[0] = f"`{totalSum+mod}` <- " + stringArr[0]
            final = " + ".join(stringArr)
            print(final)
            return final
    except Exception as e:
        print(e)
        return "error"


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

