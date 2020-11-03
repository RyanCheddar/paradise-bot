async def report(message):
    if message.content.startswith("p!report"):
        try:
            reportcontent = message.content.split(None, 1)[1]
            reportchannel = client.get_channel(765525235042222080)
            reporter = message.author
            successMsg = discord.Embed(color=0x00ff1a)
            successMsg.add_field(name="Successfull", value="Report submitted!", inline=False)
            successMsg.set_footer(icon_url=message.author.avatar_url, text='\nRequested by:\n{0}'.format(message.author))
            await message.channel.send(embed=successMsg)
            reportFinal = discord.Embed(title="Report by " + str(reporter), description=str(reportcontent), timestamp=datetime.datetime.now(datetime.timezone.utc), inline=False, color=0xff0000)
            await reportchannel.send(embed=reportFinal)
        except IndexError:
            errorMsg = discord.Embed(title="Incorrect syntax", description="Usage: p!report [report]", inline=False, color=0xff0000)
            errorMsg.set_footer(icon_url=message.author.avatar_url, text='\nRequested by:\n{0}'.format(message.author))
            await message.channel.send(embed=errorMsg)

# CHANGED: MORE PRETTIER
# TODO: EVEN MORE PRETTIER
