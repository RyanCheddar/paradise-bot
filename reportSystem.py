import discord
from discord.ext.commands import Bot
from discord.utils import get
import asyncio


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
        successMsg=discord.Embed(color=0x00ff1a)
        successMsg.add_field(name="Successfull", value="Report sumitted!", inline=False)
        successMsg.set_footer(text=str(reporter))
        await message.channel.send(embed=successMsg)
        reportFinal=discord.Embed(color=0xff0000)
        reportFinal.add_field(name="Report by " + str(reporter), value=str(reportcontent), inline=False)
        await reportchannel.send(embed=reportFinal)

client.run('NzYxOTcwNDc3NTMwNzQyNzg0.X3iWTg.OzC7N5qC5jeH25mpz4XErcT5-CQ')
