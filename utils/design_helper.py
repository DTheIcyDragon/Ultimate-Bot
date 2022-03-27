import discord

class ConsoleColors:
    PURPLE = '\033[95m'  # purple
    BLUE = '\033[94m'  # blue
    GREEN = '\033[92m'  # green
    YELLOW = '\033[93m'  # light_yellow
    RED = '\033[91m'  # light_red
    NORMAL = '\033[0m'  # "Normal" color
    BOLD = '\033[1m'  # Bold
    UNDERLINED = '\033[4m'  # Underline
    
    
def TestEmbed():
    test_embed = discord.Embed(title="Test",
                               description="*It* **obviously** ***works!***",
                               color = discord.Color.from_rgb(255,255,255))
    return test_embed