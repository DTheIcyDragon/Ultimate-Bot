import discord
from discord.ext import commands
from utils.design_helper import ConsoleColors
import logging

logging.basicConfig(filename="data/bot.log",
                    filemode="w",
                    datefmt="%d-%b-%y %H:%M:%S",
                    format="%(levelname)s: %(asctime)s - %(message)s",
                    level="INFO")

class DiscordEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_disconnect(self):
        logging.critical(f"The client has been disconnected!")
        print(f"{ConsoleColors.RED} Disconnected")

    @commands.Cog.listener()
    async def on_resumed(self):
        logging.warning("The client has reconnected!")
        print(f"{ConsoleColors.YELLOW} Reconnected")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        pass


def setup(client):
    client.add_cog(DiscordEvents(client))