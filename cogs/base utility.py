import json
import os
import platform

import discord
import psutil as psutil
from discord.ext import commands

from utils.console_colors import ConsoleColors
from main import starttime, get_prefix

class BaseUtils(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.slash_command(name = "ping", description = "Show's the latency of the bot.")
    async def ping(self, ctx: discord.ApplicationContext):
        ping = self.client.latency * 1000
        em = discord.Embed(title="PONG 🏓",
                           description=f"`Ping`: {round(ping)}ms",
                           color=discord.Color.nitro_pink())
        await ctx.respond(embed = em)

    @commands.slash_command(name = "prefix", description = "Changes the prefix of the bot.")
    async def prefix(self,
                     ctx: discord.ApplicationContext,
                     prefix: discord.Option(str,
                                            description = "The new Prefix of the bot.")
                     ):
        
        with open("data/prefixes.json", "r") as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open("data/prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)
        await ctx.respond(embed=discord.Embed(title="Prefix",
                                            description=f"Mein Prefix ist jetzt `{prefix}`.",
                                            color=discord.Color.nitro_pink()))

    @commands.slash_command(name = "botstats",
                            description = "Show stats about the bot")
    async def botstats(self, ctx: discord.ApplicationContext):
        em = discord.Embed(title="Stats", color=discord.Color.nitro_pink())
        em.add_field(name = "Bot Info",
                     value=f"""
                                Eingeloggt als {self.client.user.mention}
                                **Prefix:** {get_prefix(client = self.client, message = ctx)}
                            """,
                     inline=False)
        em.add_field(name = f"Statistiken",
                     value=f"""
                                **Latenz**
                                {round(self.client.latency * 1000)}ms
                                **Laufzeit**
                                Exakt:<t:{starttime()}:f>
                                Relativ: <t:{starttime()}:R>
                            """,
                     inline=False)
        em.add_field(name="Anderes",
                     value=f"""
                                Pycord Version: {discord.__version__}
                                Python Version: {platform.python_version()}
                                System: {platform.system()} {platform.release()} {os.name}
                            """,
                     inline=False)
        em.add_field(name = "Hardware",
                    value = f"""
                                CPU Nutzung: {psutil.cpu_percent()}%
                                RAM Nutzung: {psutil.virtual_memory()[2]}
                            """,
                    inline=False)

        await ctx.respond(embed = em)

def setup(client):
    client.add_cog(BaseUtils(client))
