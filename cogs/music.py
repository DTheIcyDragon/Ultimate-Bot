import discord
from discord.ext import commands

# Defenitionen
import settings


class MyMusic(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.lavalink_nodes = [
            # No SSL/HTTPS
            {"host": "losingtime.dpaste.org", "port": 2124, "password": "SleepingOnTrains"},
            {"host": "lava.link", "port": 80, "password": "dismusic"},
            {"host": "lavalink.islantay.tk", "port": 8880, "password": "waifufufufu"},
            
            # SSL
            {"host": "lavalink.devz.cloud", "port": 443, "password": "mathiscool", "https": True},
            {"host": "lavalink2.devz.cloud", "port": 443, "password": "mathiscool", "https": True},
            {"host": "disbotlistlavalink.ml", "port": 443, "password": "LAVA", "https": True},
            {"host": "lavalink.scpcl.site", "port": 443, "password": "lvserver", "https": True},
            {"host": "lavalink.mariliun.ml", "port": 443, "password": "lavaliun", "https": True},
            {"host": "lavalinkinc.ml", "port": 443, "password": "incognito", "https": True},
            {"host": "node1.lavalink.trgop.gq", "port": 443, "password": "onionispro", "https": True},
            {"host": "node3.lavalink.trgop.gq", "port": 443, "password": "onionop", "https": True},
            {"host": "node5.lavalink.trgop.gq", "port": 443, "password": "htandsm", "https": True},
            {"host": "www.lavalinknodepublic.ml", "port": 443, "password": "mrextinctcodes", "https": True},
            {"host": "www.lavalinknodepublic2.ml", "port": 443, "password": "mrextinctcodes", "https": True},
            {"host": "lavalink.cobaltonline.net", "port": 443, "password": "cobaltlavanode23@", "https": True},
        
        ]
        print(f"{settings.console_colors.BLUE}Loaded music{settings.console_colors.RESET}")
        self.client.spotify_credentials = {
            'client_id': settings.SPOTIFY_ID,
            'client_secret': settings.SPOTIFY_SECRET
        }


def setup(client):
    client.add_cog(MyMusic(client))
    client.load_extension("dismusic")


def teardown(client):
    client.unload_extension("dismusic")
    client.remove_cog(MyMusic(client))
