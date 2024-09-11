from typing import Optional

import pandas as pd
import discord
import token_bot
from discord import app_commands
import credentials
import db_handler

#MY_GUILD = discord.Object(id=1163857844865617991) 
#Rei caido
MY_GUILD = discord.Object(id=1215497910553419816)
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
    db = db_handler.db_Handler(db_name=credentials.db_name ,host=credentials.db_host,username=credentials.db_username,password=credentials.db_password)
    #db.read("discordCharacters",{"name":char_name})
    await interaction.response.send_message(f'{char_name}')

@client.tree.command()
@app_commands.describe()
async def create_char(interaction: discord.Interaction, char_json: str, usuario: Optional[discord.Member] = None):
    db = db_handler.db_Handler(db_name=credentials.db_name ,host=credentials.db_host,username=credentials.db_username,password=credentials.db_password)
    await interaction.response.send_message(f'{char_name}')

@client.tree.command()
@app_commands.describe()
async def roll(interaction:  discord.Interaction, dice_to_roll: str, usuario: Optional[discord.Member] = None):
    from dice_roll import dice_roller
    result = dice_roller.rolling(dice_to_roll)
    await interaction.response.send_message(f'{result}')

@client.tree.command()
@app_commands.describe()
async def spell(interaction:  discord.Interaction, spell: str):
    from spells import spell_lister
    result = spell_lister.search_spell(spell)
    print(result)
    cr_embed = discord.Embed(title=result["name"].iloc[0], description=result["desc"].iloc[0], colour=0xFFFFFF)
    cr_embed.add_field(name="Higher levels", value=result["higher_level"].iloc[0], inline = False)
    cr_embed.add_field(name="Range", value=result["range"].iloc[0], inline=True)
    cr_embed.add_field(name="Level", value=result["level"].iloc[0], inline=True)
    cr_embed.add_field(name="Duration", value=result["duration"].iloc[0], inline=True)
    cr_embed.add_field(name="Components", value=result["components"].iloc[0], inline=True)
    cr_embed.add_field(name="Concentration", value=result["concentration"].iloc[0], inline=True)
    await interaction.response.send_message(embeds=[cr_embed])

client.run(token_bot.token)