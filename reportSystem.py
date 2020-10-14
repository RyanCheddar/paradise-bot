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
        try:
            reportcontent = message.content.split(None, 1)[1]
            reportchannel = client.get_channel(765525235042222080)
            reporter = message.author
            successMsg = discord.Embed(color=0x00ff1a)
            successMsg.add_field(name="Successfull", value="Report submitted!", inline=False)
            successMsg.set_footer(text=str(reporter))
            await message.channel.send(embed=successMsg)
            reportFinal = discord.Embed(title="Report by " + str(reporter), description=str(reportcontent), timestamp=datetime.datetime.now(datetime.timezone.utc), inline=False, color=0xff0000)
            await reportchannel.send(embed=reportFinal)
        except IndexError:
            errorMsg = discord.Embed(name="Incorrect syntax", value="Usage: p!report [report]", inline=False, color=0xff0000)
            await message.channel.send(embed=errorMsg)


# CHANGED: prettier
# TODO: MORE PRETTIER
