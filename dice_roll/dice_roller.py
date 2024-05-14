import random

def rolling(dices):
    result = 0
    dices = dices.split("+")
    for dice in dices:
        dice = dice.split("d")
        print(dice)
        print(len(dice))
        if len(dice)>1:
            for x in range(int(dice[0])):
                print(int(dice[1]))
                result = result + random.randint(1,int(dice[1]))
                print(result)
        else:
            result = result + int(dice[0])
    print("final result:"+str(result))
    return result