import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

def log_channel(client: discord.Client):
    log = int(os.getenv("LOG"))
    channel = client.get_channel(log)
    return channel

def is_owner():
    def predicate(ctx):
        guild = ctx.guild
        role = guild.get_role(int(os.getenv("OWNERROLE")))
        return role in ctx.author.roles
    return commands.check(predicate)

def is_admin():
    def predicate(ctx):
        guild = ctx.guild
        role = guild.get_role(int(os.getenv("ADMINROLE")))
        return role in ctx.author.roles
    return commands.check(predicate)


def is_team():
    def predicate(ctx):
        guild = ctx.guild
        role = guild.get_role(int(os.getenv("TEAMROLE")))
        return role in ctx.author.roles
    return commands.check(predicate)

def is_verified():
    def predicate(ctx):
        guild = ctx.guild
        role = guild.get_role(int(os.getenv("VERIFIED")))
        return role in ctx.author.roles
    return commands.check(predicate)
