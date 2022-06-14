import asyncio
import os
from dotenv import load_dotenv
import discord

load_dotenv()

class VerificationButtons(discord.ui.View):
    def __init__(self, message: discord.Interaction = None):
        self.message = message
        super().__init__(timeout = 300)

    async def on_timeout(self) -> None:
        self.disable_all_items()
        em = discord.Embed(
            title = "Bitte nutze den Command erneut, die Zeit ist abgelaufen.",
            color = discord.Color.dark_blue()
        )
        await self.message.edit_original_message(embed = em, view = self)


    @discord.ui.button(
            style = discord.ButtonStyle.red,
            label = "Ablehnen",
            disabled = False,
            emoji = "<:redTick:962801636152078356>"
        )
    async def red_callback(self, button: discord.Button, interaction: discord.Interaction):
        em = discord.Embed(title = "Ist okay, du kannst es noch immer später machen.",
                           color = discord.Color.dark_red())
        self.disable_all_items()
        await self.message.delete_original_message()
        await interaction.response.send_message(embed = em, view = self)
        self.stop()

    @discord.ui.button(
            style = discord.ButtonStyle.green,
            label = "Annehmen",
            disabled = False,
            emoji = "<:greenTick:962801636189798440>"
        )

    async def green_callback(self, button: discord.Button, interaction: discord.Interaction):
        role = interaction.guild.get_role(int(os.getenv("VERIFIED")))
        user = interaction.user
        if not role in user.roles:
            em = discord.Embed(title = "Verifizierung Erfolgreich!",
                               description = "Bitte warte eine Sekunde.",
                               color = discord.Color.green())
            self.disable_all_items()
            await self.message.delete_original_message()
            await interaction.response.send_message(embed = em, view = self)
            self.stop()
            await asyncio.sleep(1.2)
            await user.add_roles(role, reason = f"Verification for {user.name}")
            await asyncio.sleep(5)
            await interaction.channel.delete(reason = f"Verification for {user.name} successful.")
        else:
            em = discord.Embed(title = "Du bist bereits verifiziert!",
                               color = discord.Color.dark_red())
            self.disable_all_items()
            await self.message.delete_original_message()
            await interaction.response.send_message(embed = em, view = self)
            self.stop()
            