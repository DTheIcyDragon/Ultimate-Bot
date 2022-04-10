import datetime
import time

import discord

class ConsoleColors:
    PURPLE = '\033[95m'     # purple
    BLUE = '\033[94m'       # blue
    GREEN = '\033[92m'      # green
    YELLOW = '\033[93m'     # light_yellow
    RED = '\033[91m'        # light_red
    NORMAL = '\033[0m'      # "Normal" color
    BOLD = '\033[1m'        # Bold
    UNDERLINED = '\033[4m'  # Underline


def TestEmbed():
    test_embed = discord.Embed(title="~***Mark***~ ***_down_*** title",
                               description="**This** *is* ***a*** ~Description~",
                               color = discord.Color.from_rgb(255,255,255))
    test_embed.set_author(name = "Das ist der Authorname", icon_url="https://cdn.discordapp.com/attachments/962327039053033472/962327055066861638/dragon.jpg")
    test_embed.set_footer(text="Footer text", icon_url="https://cdn.discordapp.com/avatars/861323291716354058/c7404f54fee88933771c8192c0f329a5.png?size=4096")
    test_embed.add_field(name="This is a field", value="with a value", inline=True)
    test_embed.add_field(name = "Inline", value="does this", inline=True)
    
    
    
    return test_embed

