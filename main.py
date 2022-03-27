import discord
from discord.ext import commands, tasks

import utils.design_helper
from utils import *

import os
import json
from dotenv import load_dotenv
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
#definitions
def get_prefix(client, message):
    with open("data/prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]


#main_bot
client = commands.Bot(command_prefix=get_prefix,
                      case_insensitive=True,
                      strip_after_prefix=True,
                      help_command=SupremeHelpCommand(),
                      intents = discord.Intents.all())





@client.command(name = "test", help = "A command to test the bots functionality")
async def test(ctx):
    await ctx.reply(embed = utils.design_helper.TestEmbed())

if __name__ == '__main__':
    client.run(os.getenv('TOKEN'))