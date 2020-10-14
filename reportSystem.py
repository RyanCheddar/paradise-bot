import discord
from discord.ext.commands import Bot
from discord.utils import get
import asyncio
import datetime

client = Bot('!')

@client.event
async def on_ready():
    print("bot ready")

@client.event
async def on_message(message):
    if message.content.startswith("p!report"):
        reportcontent = message.content.split(None, 1)[1]
        reportchannel = client.get_channel(765525235042222080)
        reporter = message.author
        successMsg = discord.Embed(color=0x00ff1a)
        successMsg.add_field(name="Successfull", value="Report sumitted!", inline=False)
        successMsg.set_footer(text=str(reporter))
        await message.channel.send(embed=successMsg)
        reportFinal = discord.Embed(title="Report by " + str(reporter), description=str(reportcontent), timestamp=datetime.datetime.now(datetime.timezone.utc), inline=False, color=0xff0000)
        await reportchannel.send(embed=reportFinal)

    if message.content == 'cheddar':
        await message.channel.send(":PogChamp~5:")


# CHANGED: prettier
# TODO: MORE PRETTIER
