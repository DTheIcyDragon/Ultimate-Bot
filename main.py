import os
import time
import json
import datetime
import platform

from utils.console_colors import *

import discord
import pyfiglet
from discord.ext import commands
from discord.commands import permissions
from dotenv import load_dotenv

load_dotenv()

class LoadSelect(discord.ui.Select):
    def __init__(self):
        super().__init__(
            placeholder="Choose the cog to load",
            min_values=1,
            max_values=1,
            options=options_(),
        )

    async def callback(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(f"{interaction.user.mention} you are not allowed to do that")
        else:
            client.load_extension(f"cogs.{self.values[0].lower()}")

            with open("data/cogs.json", "r") as f:
                loads = json.load(f)

            loads["cogs"][self.values[0].lower()] = "1"

            with open("data/cogs.json", "w") as f:
                json.dump(loads, f, indent=4)

            await interaction.response.send_message(
                f"Loaded {self.values[0]}",
                delete_after=5
            )
class UnLoadSelect(discord.ui.Select):
    def __init__(self):
        options = options_()

        super().__init__(
            placeholder="Choose the cog to unload",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(f"{interaction.user.mention} you are not allowed to do that")
        else:
            client.unload_extension(f"cogs.{self.values[0].lower()}")

            with open("data/cogs.json", "r") as f:
                loads = json.load(f)

            loads["cogs"][self.values[0].lower()] = "0"

            with open("data/cogs.json", "w") as f:
                json.dump(loads, f, indent=4)

            await interaction.response.send_message(
                f"Unloaded {self.values[0]}",
                delete_after = 5
            )
class ReLoadSelect(discord.ui.Select):
    def __init__(self):
        options = options_()

        super().__init__(
            placeholder="Choose the cog to Reload",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(f"{interaction.user.mention} you are not allowed to do that")
            return
        else:
            client.unload_extension(f"cogs.{self.values[0].lower()}")
            client.load_extension(f"cogs.{self.values[0].lower()}")

        await interaction.response.send_message(
            f"Reloaded {self.values[0]}",
            delete_after=5
        )
class UniLoadView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(LoadSelect())
        self.add_item(UnLoadSelect())
        self.add_item(ReLoadSelect())

def get_prefix(client, message):
    with open("data/prefixes.json", "r") as f:
        prefixes = json.load(f)
        if isinstance(message.channel, discord.DMChannel):
            return "isnotaPrefixedChannel"
    return prefixes[str(message.guild.id)]
def options_():
    modules = []

    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            modules.append(discord.SelectOption(label=str(file.capitalize()[:-3])))

    return modules

started = time.time()

def starttime():
    return int(started)

client = commands.Bot(command_prefix=get_prefix,
                      case_insensitive=True,
                      strip_after_prefix=True,
                      intents = discord.Intents.all(),
                      debug_guilds = [int(os.getenv("DEBUGGUILD"))]
                        )

@client.event
async def on_ready():
    print(f"""
{ConsoleColors.PURPLE}
{pyfiglet.figlet_format(client.user.name)}
Logged in as {client.user.name} ({client.user.id})
Pycord Version {discord.__version__}
Python Version {platform.python_version()}
Running on: {platform.system()} {platform.release()} ({os.name})
Ready at: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Joined at the following guilds
""")
    async for guild in client.fetch_guilds(limit=100):
        print(ConsoleColors.BLUE, guild.name)

    with open("data/cogs.json", "r") as f:
        loads = json.load(f)
    loads = loads["cogs"]
    for key, value in loads.items():
        if value == "1":
            print(f"{ConsoleColors.GREEN}       Loaded {key}")

@client.slash_command(name = "cogs", description = "Shows wich Cogs are loaded\nLoad, Unload, Reload") #permissions are defined in the view
async def cogs_cmd(ctx):
    with open("data/cogs.json", "r") as f:
        loads = json.load(f)
    loads = loads["cogs"]
    embed = discord.Embed(title = "Cog Board",
                          description = "Shows wich Modules are loaded",
                          color = discord.Color.dark_red())
    for key, value in loads.items():
        embed.add_field(name = key.capitalize(), value = f'{"🟢" if value == "1" else "🔴"}')
    await ctx.respond(embed = embed, view = UniLoadView())


@client.slash_command(name = "test", description = "A command to test the bots functionality")
@permissions.is_owner()
async def test(ctx):
    test_embed = discord.Embed(title="~~***Mark***~~ ***__down__*** title",
                               description="**This** *is* ***a*** ~~Description~~",
                               color = discord.Color.from_rgb(255,255,255))
    test_embed.set_author(name = "Das ist der Authorname", icon_url="https://cdn.discordapp.com/attachments/962327039053033472/962327055066861638/dragon.jpg")
    test_embed.set_footer(text="Footer text", icon_url="https://cdn.discordapp.com/avatars/861323291716354058/c7404f54fee88933771c8192c0f329a5.png?size=4096")
    test_embed.add_field(name="This is a field", value="with a value", inline=True)
    test_embed.add_field(name = "Inline", value="does this", inline=True)
    await ctx.respond(embeds = [test_embed])

if __name__ == '__main__':
    
    with open("data/cogs.json", "r") as f:
        loads = json.load(f)
    loads = loads["cogs"]
    for key, value in loads.items():
        if value == "1":
            client.load_extension(f"cogs.{key}")

    client.run(os.getenv('TOKEN'))
    