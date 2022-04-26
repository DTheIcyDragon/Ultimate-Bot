import os

import discord
from discord.ext import commands


class FeedbackModal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        title = self.title
        if title == "Application":
            self.add_item(discord.ui.InputText(style=discord.InputTextStyle.short,
                                               label="What do you want to apply for?",
                                               placeholder="e.g. Moderator",
                                               max_length=255))
            self.add_item(discord.ui.InputText(style=discord.InputTextStyle.long,
                                               label="Why do you want that?",
                                               placeholder="e.g. Because I think I am a good Moderator"))
        if title == "Bug":
            self.add_item(discord.ui.InputText(style=discord.InputTextStyle.short,
                                               label="Where is the bug?",
                                               placeholder="e.g. The bot while using the ping command",
                                               max_length=255))
            self.add_item(discord.ui.InputText(style=discord.InputTextStyle.long,
                                               label="How can we reproduce it?",
                                               placeholder="e.g. Just run the ban command without having the right for it."))
        if title == "Feature":
            self.add_item(discord.ui.InputText(style=discord.InputTextStyle.short,
                                               label="What feature you want to suggest.",
                                               placeholder="e.g. Daily feed of reddit memes.",
                                               max_length=255))
            self.add_item(discord.ui.InputText(style=discord.InputTextStyle.long,
                                               label="Explain your feature.",
                                               placeholder="e.g. Just let it feed through the bot into the memes channel."))
        if title == "Help":
            self.add_item(discord.ui.InputText(style=discord.InputTextStyle.short,
                                               label="How can we assist you?",
                                               placeholder="e.g. How do I report someone?",
                                               max_length=255))
            self.add_item(discord.ui.InputText(style=discord.InputTextStyle.long,
                                               label="Details",
                                               placeholder="e.g. How am I able to do that."))
        if title == "Other":
            self.add_item(discord.ui.InputText(style=discord.InputTextStyle.short,
                                               label="Other",
                                               placeholder="...",
                                               max_length=255))
            self.add_item(discord.ui.InputText(style=discord.InputTextStyle.long,
                                               label="More space to explain",
                                               placeholder="Just write more here if you need to."))

    async def callback(self, interaction: discord.Interaction):
        client = interaction.client
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        channel = client.get_channel(int(os.getenv("MODABSTIMMUNGEN")))
        
        em = discord.Embed(title = self.children[0].value,
                           description=self.children[1].value,
                           color = discord.Color.purple())
        em.set_author(name = member.name, icon_url = member.display_avatar)
        em.set_footer(text = member.id)
        message = await channel.send(embed = em)
        await interaction.response.send_message(embed = discord.Embed(title=f"Thanks for submitting your feedback.",
                                                color = discord.Color.purple()).set_footer(text="Your id was submitted for your identification to inform you about the process."))
        await message.add_reaction("🟢")
        await message.add_reaction("🟡")
        await message.add_reaction("🔴")

class ModalsCog(commands.Cog):
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


def setup(client):
    client.add_cog(ModalsCog(client))