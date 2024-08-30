import discord
import random
def roll20PlusMod(mod):
    return random.randint(1,20)+mod

def roll_iniciative(idList, dexMod):
    idDict = {}
    for i in idList:
        idDict[i] = roll20PlusMod(dexMod)
        
    return dict(sorted(idDict.items(), key=lambda item: item[1], reverse=True))

def setEmbed(idDict):
    string = ""
    for i in idDict.keys():
        string += f"`{idDict[i]}` <- {i}\n"

    embed = discord.Embed(title="iniciativa",description=string,colour=0xFFFFFF)
    return embed
