import discord
from dice_roll import dice_roller

def filterMembers(memberList):
    filteredMemberList = [member.display_name for member in memberList if member is not None]
    return filteredMemberList

#update this function to receive a list of dex modifiers
def roll_iniciative(idList, dexMod):
    idDict = {}
    for i in idList:
         idDict[i] = dice_roller.multiRolls(1,20)[0]
    
    return dict(sorted(idDict.items(), key=lambda item: item[1], reverse=True))

def setEmbed(idDict):
    string = ""
    for i in idDict.keys():
        string += f"`{idDict[i]}` <- {i}\n"

    embed = discord.Embed(title="iniciativa",description=string,colour=0xFFFFFF)
    return embed
