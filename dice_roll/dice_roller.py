import random

def rolling(dices):
    try:
        result = 0
        result_text = ""
        dices = dices.split("+")
        for dice in dices:
            dice = dice.split("d")
            print(dice)
            print(len(dice))
            if len(dice)>1:
                if result_text != "":
                    result_text = result_text + "+ "
                result_text_aux = "["
                for x in range(int(dice[0])):
                    print("dice"+str(dice[1]))
                    roll = random.randint(1,int(dice[1]))
                    result = result + roll
                    print("partial result: "+str(result))
                    if roll == int(dice[1]) or roll == 1:
                        print("MIN/MAX VALUE")
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
        print("final result:"+str(result))
        print(result_text)
        return result_text
    except:
        return "Error"