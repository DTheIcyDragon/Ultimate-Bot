import json
import os
import time
import discord
from discord.ext import commands
from asyncio import sleep
from dotenv import load_dotenv

from utils import helper_functions, modals

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
        em.add_field(name=f"Discord Beigetreten", value=f"<t:{int(created_at)}:F>", inline=False)
        em.add_field(name="Server beigetreten", value=f"<t:{int(joined_at)}:F>")
        em.add_field(name=f"Bot", value=f"{'Ja' if member.bot else 'Nein'}", inline=False)
        em.set_thumbnail(url=member.display_avatar)

        if not ctx.channel.id == int(os.getenv("MODAREA")):
            await ctx.respond(embed = em)

        else:
            try:
                with open("data/moderation_user.json", "r") as f:
                    user = json.load(f)
                warnings = user[str(member.id)]["warning_details"]
                em.add_field(name = "Warunugen", value = "------------------", inline = False)
                for num, warning in warnings.items():
                    em.add_field(name = f"{num}. Verwarnung", value=f"{warning}", inline = False)
                    if len(em.fields) > 24:
                        break
            except KeyError:
                em.add_field(name = "Warnings", value="0")
            await ctx.respond(embed = em)


    @commands.slash_command(name = "warn",
                            description = "Warns a member")
    @helper_functions.is_team()
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
                with open("data/moderation_user.json", "w") as a:
                    json.dump(data, a, indent=4)
                with open("data/moderation_user.json", "r") as b:
                    data = json.load(b)
                data[user]["warning_details"] = {}
                with open("data/moderation_user.json", "w") as c:
                    json.dump(data, c, indent=4)
            infractions = data[user]["warning_details"]

            count = 0
            for key, _ in infractions.items():
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
    
    @commands.slash_command(name = "kick",
                            description = "Kicks a member")
    @helper_functions.is_team()
    async def kick(self,
                   ctx: discord.ApplicationContext,
                   member: discord.Option(str,
                                          "Please provide a member id to warn!",
                                          required = True)):
        
        member = ctx.guild.get_member(int(member))
        for role in member.roles:
            if role.permissions.manage_channels:
                
                break
        modal = modals.KickModal(title = member.name)
        await ctx.send_modal(modal)
       
#        await member.kick(reason = f"Kicked by {ctx.author}")

    @commands.slash_command(name = "clear",
                            description = "Clears an given amount of messages from the chat.")
    @commands.has_any_role()
    async def clear(self,
                    ctx: discord.ApplicationContext,
                    amount: discord.Option(int,
                                           "Provide a number of messages to clear.",
                                           required=True)):
        
        await ctx.respond("Purging...")
        await sleep(0.5)
        purge = await ctx.channel.purge(limit=amount,
                                reason=f"{ctx.author.name} bulk deleted messages in {ctx.channel.name}")

        em = discord.Embed(title="Purge results",
                           description=f"Purgend {len(purge)} from targeted {amount}.",
                           color=discord.Color.darker_gray())
        await sleep(0.8)
        await ctx.channel.send(embed=em, delete_after=7.5)
        
def setup(client):
    client.add_cog(ModerationCog(client))