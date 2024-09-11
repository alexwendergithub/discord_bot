from typing import Optional

import pandas as pd
import discord
import token_bot
from discord import app_commands

MY_GUILD = discord.Object(id=1163857844865617991) 
#Rei caido
#MY_GUILD = discord.Object(id=1215497910553419816)
intents = discord.Intents.default()
intents.message_content = True
class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)


intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')

@client.tree.command()
@app_commands.describe(
    char_name='Nome do personagem para se pegar informaçoes',
)
async def get_char(interaction: discord.Interaction, char_name: str):
    await interaction.response.send_message(f'{char_name}')

@client.tree.command()
@app_commands.describe()
async def create_char(interaction: discord.Interaction, char_json: str, usuario: Optional[discord.Member] = None):
    await interaction.response.send_message(f'{char_name}')

@client.tree.command()
@app_commands.describe()
async def roll_dice(interaction:  discord.Interaction, dice_to_roll: str, usuario: Optional[discord.Member] = None):
    from dice_roll.dice_roller import mountString, processString
    result = mountString(dice_to_roll,processString(dice_to_roll))
    await interaction.response.send_message(f'{result}')

@client.tree.command()
@app_commands.describe()
async def roll_iniciative(interaction: discord.Interaction, member1: discord.Member, member2: discord.Member, member3: Optional[discord.Member]= None, member4: Optional[discord.Member]= None, member5: Optional[discord.Member]= None, member6: Optional[discord.Member]= None, member7: Optional[discord.Member]= None, member8: Optional[discord.Member]= None, member9: Optional[discord.Member]= None, member10: Optional[discord.Member]= None):
    from iniciative_roll.iniciative_roll import filterMembers, roll_iniciative, setEmbed
    
    members = [member1, member2, member3, member4, member5, member6, member7, member8, member9, member10]
    
    filteredList = filterMembers(members)
    result = setEmbed(roll_iniciative(filteredList,1))
    await interaction.response.send_message(embed=result)

client.run(token_bot.token)