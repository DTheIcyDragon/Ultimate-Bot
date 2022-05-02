import os
import discord
from dotenv import load_dotenv

load_dotenv()

def log_channel(client: discord.Client):
    log = int(os.getenv("LOG"))
    channel = client.get_channel(log)
    return channel