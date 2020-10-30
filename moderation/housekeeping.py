async def clear(message):
    if message.author.guild_permissions.manage_messages != True:
        embed=discord.Embed(title='No Permission', description="Required permission: MANAGE_MESSAGES", color=0xe22400)
        await message.channel.send(content=message.author.mention, delete_after=5, embed=embed)
        return

    if message.content.split(None, 1)[1].isdigit() == False or len(message) != 2:
        embed=discord.Embed(title='Wrong Command Syntax', description="Correct syntax: `p!clear [NUMBER]`", color=0xe22400)
        await message.channel.send(content=message.author.mention, delete_after=5, embed=embed)
        return

    amount = int(message.content.split()[1])
    embed=discord.Embed(title=f'Are you sure you want to clear {message.content.split(None, 1)[1]} messages?', description="Please do `p!confirm` to confirm this action.", color=0xe22400)
    embed.set_footer(text="Paradise Bot")
    msg = await message.channel.send(content=message.author.mention, delete_after=20, embed=embed)
    def check(m):
        return m.content == 'p!confirm' and m.channel == channel and m.author == message.author
    
    try:
        msg = await client.wait_for('message', timeout=15.0, check=check)
    except asyncio.TimeoutError:
        await abcdefg.edit(content='I did not receive confirmation in time. Oh well.', delete_after=5)
        await message.delete(delay=5)
    
    else:
        await channel.purge(limit=int(message.content.split(None, 1)[1]) + int('3'))
        await message.channel.send(content='Successfully deleted ' + message.content.split(None, 1)[1] + ' messages!', delete_after=5)
        await log(f"{message.author.name} ({message.author.mention}) deleted {amount} messages in {message.channel.mention}.")
        return

async def say(message):
    print("Say function in Housekeeping module Called")
    return

async def edit(message):
    print("Edit function in Housekeeping module Called")
    return

async def react(message):
    print("React function in Housekeeping module Called")
    return