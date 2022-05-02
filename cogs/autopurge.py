import discord
import os
from discord.ext import commands, tasks
from dotenv import load_dotenv
from asyncio import sleep
load_dotenv()

class Autopurge(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.clear.start()

    @tasks.loop(hours=24)
    async def clear(self):
        await self.client.wait_until_ready()
        channel = self.client.get_channel(int(os.getenv("COMMANDSCHANNEL")))
        messages = await channel.history(limit=3).flatten()
        if len(messages) != 0:

            purge = await channel.purge(limit=999,
                                        oldest_first=True,
                                        bulk=True,
                                        reason=f"Bulk purge in {channel.name}")
            em = discord.Embed(title = "Purge",
                               description = f"I cleared {len(purge)} Messages",
                               color = discord.Color.darker_gray())
            await sleep(0.8)
            await channel.send(embed = em)
        else:
            pass


def setup(client):
    client.add_cog(Autopurge(client))