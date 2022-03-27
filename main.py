import json
import os
import utils

import discord
import pyfiglet
from discord.ext import commands
from dotenv import load_dotenv

from utils.design_helper import *

load_dotenv()


#class
class SupremeHelpCommand(commands.HelpCommand):
    def get_command_signature(self, command):   #full credits to the pycord guide https://github.com/Pycord-Development/guide
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", color=discord.Color.dark_gold())
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            if command_signatures := [
                self.get_command_signature(c) for c in filtered
            ]:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command) , color=discord.Color.dark_gold())
        if command.help:
            embed.description = command.help
        if alias := command.aliases:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_help_embed(self, title, description, commands): # a helper function to add commands to an embed
        embed = discord.Embed(title=title, description=description or "No help found...", color=discord.Color.dark_gold())

        if filtered_commands := await self.filter_commands(commands):
            for command in filtered_commands:
                embed.add_field(name=self.get_command_signature(command), value=command.help or "No help found...")

        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        title = self.get_command_signature(group)
        await self.send_help_embed(title, group.help, group.commands)

    async def send_cog_help(self, cog):
        title = cog.qualified_name or "No"
        await self.send_help_embed(f'{title} Category', cog.description, cog.get_commands())


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

#definitions
def get_prefix(client, message):
    with open("data/prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]
def options_():
    modules = []
    
    for file in os.listdir("cogs"):
        if file.endswith(".py"):
            modules.append(discord.SelectOption(label=str(file.capitalize()[:-3])))
    
    return modules

#main_bot
client = commands.Bot(command_prefix=get_prefix,
                      case_insensitive=True,
                      strip_after_prefix=True,
                      help_command=SupremeHelpCommand(),
                      intents = discord.Intents.all())

@client.event
async def on_ready():
    print(f"""
{ConsoleColors.PURPLE}
{pyfiglet.figlet_format(client.user.name)}
Bot ID: {client.user.id}
Joined at the following guilds
""")
    async for guild in client.fetch_guilds(limit=100):
        print(ConsoleColors.BLUE, guild.name)

    with open("data/cogs.json", "r") as f:
        loads = json.load(f)
    loads = loads["cogs"]
    for key, value in loads.items():
        if value == "1":
            client.load_extension(f"cogs.{key}")

@client.command(name = "cogs", help = "Shows wich Cogs are loaded")
async def cogs_cmd(ctx):
    with open("data/cogs.json", "r") as f:
        loads = json.load(f)
    loads = loads["cogs"]
    embed = discord.Embed(title = "Cog Board",
                          description = "Shows wich Modules are loaded",
                          color = discord.Color.dark_red())
    for key, value in loads.items():
        embed.add_field(name = key.capitalize(), value = f'{"🟢" if value == "1" else "🔴"}')
    await ctx.reply(embed = embed, view = UniLoadView())
    

@client.command(name = "test", help = "A command to test the bots functionality")
async def test(ctx):
    await ctx.reply(embed = utils.design_helper.TestEmbed())

if __name__ == '__main__':
    client.run(os.getenv('TOKEN'))