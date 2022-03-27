import discord
from discord.ext import commands, tasks

import os



#class

#definitions
def get_prefix(client, message):
    pass #have to look into my older projects
#main_bot
client = commands.Bot(command_prefix=get_prefix)


if __name__ == '__main__':
    client.run(os.getenv('TOKEN'))