from discord.ext import commands

client = commands.Bot()

@client.event                                                       #event decorator
async def on_message(message):
    """
    Always the lowest message in a channel
    (Could be improved later)
    """
    if message.author.bot:                                          #don't react to ourselves
        return
    if message.channel.id == 877562448679411742:                    #correct channel
        channel = client.get_channel(877562448679411742)            #get the channel
        history = await channel.history().flatten()                 #channel history in a list

        if history[0].author.id != 762627384338939915:
            await client.get_message(int(history[1].id)).delete()
            await channel.send("hi")

