
async def BadName(member, message):
    name = str(member.name).upper()
    if await check_blocked_word(name) == True:
        await member.edit(nick=member.name)
        await message.delete()
        try:
            await member.send("We have removed your nickname in Paradise Network as your name was offensive. Attempts to bypass this system will result in severe punishment!")
        except discord.HTTPException:
            return


async def check_url(content):
    urls = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+',
                      content.replace(",", ".").replace(" .", ".").lower())
    print(urls)
    for x in urls:
        if any(ele in x.upper().replace("\n", "").replace("-", "").replace(" ", "").replace(".", "").replace('"', "").replace(",", "").replace("REGIONAL_INDICATOR_", "").replace(":", "").replace("/", "").replace("_", "").replace("*", "").replace("HIIPS", "").replace("HIIP", "").replace("WWW", "") for ele in ipgrab):
            return True
        else:
            return False


async def check_blocked_word(content):
    if any(ele in content.upper().replace("\n", "").replace("t", "i").replace("-", "").replace(" ", "").replace(".", "").replace('"', "").replace(",", "").replace("REGIONAL_INDICATOR_", "").replace(":", "").replace("_", "").replace("*", "") for ele in blocked_word) == True:
        return True
    else:
        return False

async def staff_ping_check(ctx):
    channel = ctx.channel
    channel = ctx.channel
    member = ctx.author
    print("checking for staff pings in msg")
    if "<@&714456813612826675>" in ctx.content:
        print("Omg let me ping all staff members")
        embed = discord.Embed(title="Emergency Ping", description="Are you sure you want to ping ALL staff members?",
                              color=0x76bb40, timestamp=datetime.datetime.now(datetime.timezone.utc))
        embed.add_field(name="Information",
                        value="**PING ALL STAFF FOR:**\nServer Raids, Spammer in chat, Anything that requires urgent attention.\n\n**PING COUNCIL FOR:**\nRogue Staff, Major Bug in Paradise Bot or Bank (e.g. Dupe Glitch), Other Admin Matters.\n\n**DO NOT PING FOR:**\nUnimportant issues, Non-Urgent Matters, Matters that are actively being handled, To annoy staff.\n\n**Abuse of this ping feature will result in permanent mute with no appeal process.**\n",
                        inline=False)
        embed.add_field(name="Still need to ping? Also if this is not urgent then you maybe consider pinging **individual staff member**",
                        value="Press :white_check_mark: to confirm this ping or press :negative_squared_cross_mark: to cancel.\n\n**DO NOT PRESS CHECKMARK IF YOU DO NOT INTEND TO PING. THIS ACTION CANNOT BE UNDONE.**\n\n(To prevent abuse, the checkmark will only appear 5 seconds later.)",
                        inline=False)
        embed.set_footer(text="Paradise Bot | Emergency Handling")
        a = await channel.send(content=member.mention + " STAFF EMERGENCY PING", embed=embed)
        try:
            await a.add_reaction("❎")
            await a.add_reaction("⬅️")
            await a.add_reaction("◀️")
            await asyncio.sleep(5)
            await a.add_reaction("✅")
        except discord.errors.NotFound:
            print("discord.errors.Notfound")

    if "<@&714457002411294760>" in ctx.content:
        embed = discord.Embed(title="Emergency Ping",
                              description="Are you sure you want to ping COUNCIL staff members?", color=0x76bb40, timestamp=datetime.datetime.now(datetime.timezone.utc))
        embed.add_field(name="Information",
                        value="**PING ALL STAFF FOR:**\nServer Raids, Spammer in chat, Anything that requires urgent attention.\n\n**PING COUNCIL FOR:**\nRogue Staff, Major Bug in Paradise Bot or Bank (e.g. Dupe Glitch), Other Admin Matters.\n\n**DO NOT PING FOR:**\nUnimportant issues, Non-Urgent Matters, Matters that are actively being handled, To annoy staff.\n\n**Abuse of this ping feature will result in permanent mute with no appeal process.**\n",
                        inline=False)
        embed.add_field(name="Still need to ping?",
                        value="Press :white_check_mark: to confirm this ping or press :negative_squared_cross_mark: to cancel.\n\n**DO NOT PRESS CHECKMARK IF YOU DO NOT INTEND TO PING. THIS ACTION CANNOT BE UNDONE.**\n\n(To prevent abuse, the checkmark will only appear 5 seconds later.)",
                        inline=False)
        embed.set_footer(text="Paradise Bot | Emergency Handling")
        a = await channel.send(content=member.mention + " COUNCIL EMERGENCY PING", embed=embed)
        try:
            await a.add_reaction("❎")
            await a.add_reaction("⬅️")
            await a.add_reaction("◀️")
            await asyncio.sleep(5)
            await a.add_reaction("✅")
        except discord.errors.NotFound:
            print("discord.errors.Notfound")
