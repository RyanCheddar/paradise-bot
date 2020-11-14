
async def transactionmanager():
    global transactionmanager_online
    transactionmanager_online = '1'
    print(transactionmanager_online)
    print("Transaction Manager online")
    while True:
        transactionmanager_online = '1'
        print(transactionmanager_online)
        await transactionmanager_core()
        await asyncio.sleep(60)


async def transactionmanager_core():
    Cursor.execute("SELECT * FROM Transactions WHERE Transaction='unban'")
    to_unban = Cursor.fetchall()
    print(to_unban)
    for check in to_unban:
        timer = check[1]
        time_now = datetime.datetime.now(datetime.timezone.utc)
        print(time_now)
        time_now = await unaware_timezone(time_now)
        print(timer, time_now)
        if timer <= time_now:
            print("checked timer")
            user_id = check[0]
            try:
                user = await client.fetch_user(int(user_id))
            except discord.errors.NotFound:
                print("user not found at the time of unban.")
            else:
                guild = client.get_guild(int(674474377286516736))
                print(guild)
                await guild.unban(user, reason="Automatic Unban.")
            Cursor.execute(
                f"DELETE FROM Transactions WHERE User_id={user_id} AND Transaction='unban'")
    Cursor.execute("SELECT * FROM Transactions WHERE Transaction='unmute'")
    to_unmute = Cursor.fetchall()
    print(to_unmute)
    for check in to_unmute:
        timer = check[1]
        time_now = datetime.datetime.now(datetime.timezone.utc)
        print(time_now)
        time_now = await unaware_timezone(time_now)
        print(timer, time_now)
        if timer <= time_now:
            print("checked timer")
            user_id = check[0]
            guild = client.get_guild(int(674474377286516736))
            #print (guild,guild.members)
            #print (type(guild),type(guild.members))
            try:
                user = await guild.fetch_member(int(user_id))
                print(user)
            except discord.errors.NotFound:
                print("user not found at the time of unmute.")
            else:
                role_check = discord.utils.get(guild.roles, name="Muted")
                if role_check in user.roles:
                    mute_role = get(guild.roles, name="Muted")
                    await user.remove_roles(mute_role)
                else:
                    print("The person was already unmuted at the time of unmute")
                Cursor.execute(
                    f"DELETE FROM Transactions WHERE User_id={user_id} AND Transaction='unmute'")
    Cursor.execute(
        "SELECT * FROM Transactions WHERE Transaction='unbanservice'")
    to_unban = Cursor.fetchall()
    print(to_unban)
    for check in to_unban:
        timer = check[1]
        time_now = datetime.datetime.now(datetime.timezone.utc)
        print(time_now)
        time_now = await unaware_timezone(time_now)
        print(timer, time_now)
        if timer <= time_now:
            print("checked timer")
            user_id = check[0]
            guild = client.get_guild(int(674474377286516736))
            #print (guild,guild.members)
            #print (type(guild),type(guild.members))
            try:
                user = await guild.fetch_member(int(user_id))
                print(user)
            except discord.errors.NotFound:
                print("user not found at the time of unmute.")
            else:
                role_remove = discord.utils.get(
                    guild.roles, name="Service Blacklisted")
                role_add = discord.utils.get(
                    guild.roles, name="Can see services")
                if role_remove in user.roles:
                    await user.add_roles(role_add)
                    await user.remove_roles(role_remove)
                else:
                    print("The person was already unbanned at the time of unmute")
                Cursor.execute(
                    f"DELETE FROM Transactions WHERE User_id={user_id} AND Transaction='unbanservice'")


async def start_transactionmanager(ctx):
    if ctx.author.guild_permissions.ban_members:
        global transactionmanager_online
        if transactionmanager_online == '0':
            print("Offline")
            await ctx.channel.send("Somehow The Transaction Manager was offline.... \nTurned it on.")
            await transactionmanager()
        else:
            msg = await ctx.channel.send("Transaction Manager seems to be online! \nConfirming its validation, please wait upto 80 seconds for the validation report.\nDo `p!forceupdate-transaction` incase you want to force refresh the transactions")
            transactionmanager_online = '0'
            count: int = 0
            while count < 80:
                if transactionmanager_online == '1':
                    await msg.edit(content="Transaction Manager is working fine......")
                    return
                await asyncio.sleep(1)
                count += 1
            # if transactionmanager_online == '0':
            await msg.edit(content="Seems like the Transaction Manager had crashed... turned it back on\n<@640773439115886642> Please look into why it had crashed")
            await transactionmanager()
            # else:
            #    await msg.edit(content="Transaction Manager is working fine......")
    else:
        await ctx.channel.send(embed=await Not_enough_perms())


async def transactionmanager_forceupdate(ctx):
    if ctx.author.guild_permissions.kick_members:
        msg = await ctx.channel.send("Force updating transactions.....")
        await transactionmanager_core()
        await msg.edit(content="Successfully Updated transactions!")
    else:
        await ctx.channel.send(embed=await Not_enough_perms())
