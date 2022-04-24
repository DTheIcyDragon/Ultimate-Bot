import json
import os
import platform

import discord
import psutil as psutil
from discord.ext import commands

from utils.design_helper import ConsoleColors
from main import starttime, get_prefix

class BaseUtils(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(name = "Ping", help = "Show's the latency of the bot.")
    async def ping(self, ctx):
        ping = self.client.latency * 1000
        em = discord.Embed(title="PONG 🏓",
                           description=f"`My latency`: {round(ping)}ms",
                           color=discord.Color.nitro_pink())
        await ctx.reply(embed = em)

    @commands.command(name = "prefix", help = "Changes the prefix of the bot.")
    async def prefix(self, ctx, prefix):
        with open("data/prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open("data/prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)
        await ctx.reply(embed=discord.Embed(title="Prefix",
                                            description=f"My prefix is now `{prefix}`",
                                            color=discord.Color.nitro_pink()))

    @commands.command(name = "botstats", help = "Show stats about the bot")
    async def botstats(self, ctx):
        em = discord.Embed(title="Stats", color=discord.Color.nitro_pink())
        em.add_field(name = "Bot info",
                     value=f"""
                                Logged in as {self.client.user.mention}
                                **Prefix:** {get_prefix(client = self.client, message = ctx)}
                            """,
                     inline=False)
        em.add_field(name = f"Statistics",
                     value=f"""
                                **Latency**
                                {round(self.client.latency * 1000)}ms
                                **Uptime**
                                Exact:<t:{starttime()}:f>
                                Relative: <t:{starttime()}:R>
                            """,
                     inline=False)
        em.add_field(name="Other",
                     value=f"""
                                Pycord Version: {discord.__version__}
                                Python Version: {platform.python_version()}
                                System: {platform.system()} {platform.release()} {os.name}
                            """,
                     inline=False)
        em.add_field(name = "Hardware",
                    value = f"""
                                CPU Usage: {psutil.cpu_percent()}%
                                RAM Usage: {psutil.virtual_memory()[2]}
                            """,
                    inline=False)

        await ctx.reply(embed = em)

def setup(client):
    client.add_cog(BaseUtils(client))
