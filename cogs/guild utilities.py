import discord
from discord.ext import commands
from dotenv import load_dotenv

import os

from utils.modals import FeedbackModal

load_dotenv()

class GuildUtilsCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    AUTOCOMPLETE = ["Application",
                    "Bug",
                    "Feature",
                    "Help",
                    "Other"]

    @commands.slash_command(name = "feedback",
                            description = "Share any feedback related to us.",
                            guild_ids=[884435317057286214, 798302722431909888])
    async def feedback(self,
                       ctx: discord.ApplicationContext,
                       form: discord.Option(str,
                                            "Pick a kind of feedback.",
                                            autocomplete=discord.utils.basic_autocomplete(AUTOCOMPLETE))):

        await ctx.send_modal(FeedbackModal(title = form))



    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id == int(os.getenv("MODABSTIMMUNGEN")):
            message = self.client.get_message(int(payload.message_id))
            print(message)
            msg_embed = message.embeds
            print(msg_embed.to_dict())
            if payload.emoji == "🟢":
                pass
                embed = discord.Embed(title = "HI")
                # TODO: get the embed.to_dict done


def setup(client):
    client.add_cog(GuildUtilsCog(client))