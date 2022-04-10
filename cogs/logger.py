import datetime

from discord.ext import commands
from utils.design_helper import ConsoleColors
import logging

with open("data/bot.log", "w") as log:
    log.write("")

logging.getLogger("discord").setLevel(logging.CRITICAL) #Implemented this to prevent py-cord logging module from logging (Credits to Red#6291 from the py-cord discord
logging.basicConfig(filename="data/bot.log",
            filemode="a",
            datefmt="%d-%b-%y %H:%M:%S",
            format="%(levelname)s: %(asctime)s - %(message)s",
            level="INFO")

class DiscordEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"The client is ready!")
        print(f"{ConsoleColors.GREEN} Started at {datetime.datetime.now()}!")

    @commands.Cog.listener()
    async def on_disconnect(self):
        logging.critical(f"The client has been disconnected!")
        print(f"{ConsoleColors.RED} Disconnected! at {datetime.datetime.now()}!")

    @commands.Cog.listener()
    async def on_resumed(self):
        logging.warning("The client has reconnected!")
        print(f"{ConsoleColors.YELLOW} Reconnected! at {datetime.datetime.now()}!")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        logging.info(f"{self.client.user.name} joined {guild.name}.")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        logging.info(f"{self.client.user.name} left {guild.name}.")

def setup(client):
    client.add_cog(DiscordEvents(client))