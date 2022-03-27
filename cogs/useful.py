import discord
from discord.ext import commands


class Useful(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def show_emojis(self, ctx):
        await ctx.reply("".join([f"`{emoji.url}`\n" if emoji.url.endswith(".gif") else "" for emoji in ctx.guild.emojis]))

def setup(client):
    client.add_cog(Useful(client))