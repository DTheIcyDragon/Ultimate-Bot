import json
import os
import time
import discord
from discord.ext import commands
from discord.commands import permissions
from dotenv import load_dotenv

from utils import helper_functions

load_dotenv()

class ModerationCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.user_command(name = "Userinfo")
    async def userinfo(self, ctx, member: discord.Member):

        joined_at = member.joined_at
        joined_at.timestamp()
        joined_at = (time.mktime(joined_at.timetuple()))

        created_at = member.created_at
        created_at.timestamp()
        created_at = (time.mktime(created_at.timetuple()))

        em = discord.Embed(title=f"Userinfo for {member.display_name}",
                           color=discord.Color.magenta())
        em.add_field(name=f"Name", value=f"{member.name}", inline=False)
        em.add_field(name=f"ID", value=f"{member.id}", inline=False)
        em.add_field(name=f"Joined discord", value=f"<t:{int(created_at)}:F>", inline=False)
        em.add_field(name="Joined this server", value=f"<t:{int(joined_at)}:F>")
        em.add_field(name=f"Bot", value=f"{'Yes' if member.bot else 'No'}", inline=False)
        em.set_thumbnail(url=member.display_avatar)

        if not ctx.channel.id == int(os.getenv("MODAREA")):
            await ctx.respond(embed = em)

        else:
            try:
                with open("data/moderation_user.json", "r") as f:
                    user = json.load(f)
                warnings = user[str(member.id)]["warnings"]
                em.add_field(name = "Warnings", value=str(warnings))
            except KeyError:
                em.add_field(name = "Warnings", value="0")
            await ctx.respond(embed = em)
            
            
    @commands.slash_command(name = "warn",
                            description = "Warns an user for something")
    async def warn(self,
                   ctx: discord.ApplicationContext,
                   user: discord.Option(str,
                                        "Please provide a member id to warn!",
                                        required=True),
                   reason: discord.Option(str,
                                          "Please provide a context!",
                                          required=True)):

        member = ctx.guild.get_member(int(user))
        
        with open("data/moderation_user.json", "r") as f:
            data = json.load(f)
            
            try:
                data[user]
            except KeyError:
                data[user] = {}
                with open("data/moderation_user.json", "w") as f:
                    json.dump(data, f, indent=4)
                with open("data/moderation_user.json", "r") as f:
                    data = json.load(f)
                data[user]["warnings"] = "0"
                data[user]["warning_details"] = {}
                with open("data/moderation_user.json", "w") as f:
                    json.dump(data, f, indent=4)
            print("bist du hier?")
            warn_count = data[user]["warnings"]
            warn_count = int(warn_count) + 1
            data[user]["warnings"] = str(warn_count)
            
            infractions = data[user]["warning_details"]
            
            count = 0
            
            for key in infractions.items():
                count =+ 1
            
            key = int(count) + 1
            data[user]["warning_details"][str(key)] = reason
            
        with open("data/moderation_user.json", "w") as f:
            json.dump(data, f, indent=4)
        
        em = discord.Embed(title = "Warn",
                           description = f"Warned {member.mention}\nReason: {reason}",
                           color=discord.Color.yellow())
        await ctx.respond(embed = em)
        await helper_functions.log_channel(client = self.client).send(embed = em.add_field(name="Moderator", value=ctx.author.mention))

def setup(client):
    client.add_cog(ModerationCog(client))