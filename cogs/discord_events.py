import discord
from discord.ext import commands
from utils.design_helper import ConsoleColors

class Preset_Cog(commands.Cog):
    def __init__(self, client):
        self.client = client

        print(f"{ConsoleColors.GREEN} Loaded Music")
def setup(client):
    client.add_cog(Preset_Cog(client))