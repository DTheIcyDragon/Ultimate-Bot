import os

import discord
from discord.ext import commands
from utils.errors import *
from dotenv import load_dotenv

load_dotenv()

def log_channel(client: discord.Client):
    log = int(os.getenv("LOG"))
    channel = client.get_channel(log)
    return channel

def is_role(member: discord.Member, role: discord.Role) -> bool:
    for thing in member.roles:
        if thing.id == role.id:
            return True
    else:
        return False
    
def is_staff():
    async def predicate(ctx: discord.ApplicationContext):
        role = ctx.guild.get_role(int(os.getenv("TEAMROLE")))
        #permission = ctx.author.guild_permissions.manage_messages
        permission = False
        role = role in ctx.author.roles
        if role or permission:
            return True
        else:
            embed = discord.Embed(title = "Error",
                                  description = "You're not allowed to run this command.")
            raise NotTeam("You are not allowed to use this command")
    return commands.check(predicate)