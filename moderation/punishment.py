async def ban(message):
    if !member.guild_permissions.ban_members:
        await message.channel.send("Not enough perms")
        
    content_split = await split(content, 2)
    banned_id = await get_digit(content_split[1])
    
        try:
            banned_id = int(banned_id)
        except:
            embed = discord.Embed(title="Member Not Found", description="You need to include the Member after p!ban!\nCorrect syntax - `p!ban <member id or mention> (reason for ban)`", color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        
        try:
            banned = await client.fetch_user(banned_id)
        except discord.errors.NotFound:
            embed = discord.Embed(title="Member Not Found", description="You need to include the Member after p!ban!\nCorrect syntax - `p!ban <member id or mention> (reason for ban)`", color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        
        print("this is to be banned: ", banned_id, banned, message.guild)
        if banned == None:
            embed = discord.Embed(title="Member Not Found", description="You need to include the Member after p!ban!\nCorrect syntax - `p!ban <member id or mention> (reason for ban)`", color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
        else:
            try:
                reason = content_split[2]
            except IndexError:
                def check(message):
                    print("checking for reason")
                    # and message.content.startswith()!="p!say"
                    return message.channel == channel and message.author == member

                try:
                    embed = discord.Embed(
                        title="Banning member", description=f"Why do you want to ban <@{banned_id}>", color=16776960, timestamp=datetime.datetime.now(datetime.timezone.utc))
                    embed.set_footer(text="Paradise Bot")
                    await message.channel.send(embed=embed, delete_after=15)
                    print("checking for reason")
                    reason = await client.wait_for('message', timeout=15.0, check=check)
                    reason = reason.content
                    print(reason)
                except asyncio.TimeoutError:
                    await message.channel.send("Oh Well, I did not get the reason in time, too bad i can't ban without reason :(")
                    return
                
            prepare = f'''SELECT MAX(`case_id`) FROM PunishmentLogs'''
            Cursor.execute(prepare)
            case_id = Cursor.fetchall()
            print("Heres the case_id: ", case_id)
            case_id = (case_id[0][0])
            try:
                case_id = int(case_id)
            except:
                case_id = 0
            else:
                case_id += 1
                
            time_now = datetime.datetime.now(datetime.timezone.utc)
            time_now = await unaware_timezone(time_now)
            prepare = f'''INSERT INTO PunishmentLogs (`User_id`,`Duration`,`reason`,`Mod`,`action`,`time`,`case_id`)
               VALUES ('{banned_id}','0','{reason}','{str(member.id)}','ban','{time_now}','{case_id}')'''
            Cursor.execute(prepare)
            duration = "Doesn't Apply to bans and warns"
            embed = discord.Embed(title=f"Case #{case_id} has been registered!", color=16711680,
                                  description=f"**Moderator: **<@{int(member.id)}>\n**Action: **Permanent Ban\n**Duration :**{duration}\n**Reason: **{reason}", timestamp=datetime.datetime.now(datetime.timezone.utc))
            try:
                dm = await banned.create_dm()
            except:
                print("can't dm member")
            else:
                embed = discord.Embed(title="Banned in Paradise Network",
                                      description=f"You have been banned in Paradise network by <@{member.id}>\nReason of warn: {reason}\nDuration: Permanent", timestamp=datetime.datetime.now(datetime.timezone.utc), color=16711680)
                await dm.send(f"You have been banned in Paradise network by <@{member.id}>\nReason of warn: {reason}\nDuration: Permanent")
            embed.set_footer(text="Paradise Bot")
            embed.set_thumbnail(url=banned.avatar_url)
            await message.channel.send(embed=embed)
            await punish_log(embed=embed)
            await message.guild.ban(banned, reason=reason, delete_message_days=0)

    else:
        await channel.send(embed=await Not_enough_perms())

async def unban(message):
    try:
        await message.delete()
    except discord.NotFound:
        print("message not found D:")
    content = message.content
    member = message.author
    channel = message.channel
    print(member.id, type(member.id))
    if member.guild_permissions.ban_members:
        print("has perms")
        content_split = await split(content, 2)
        banned_id = await get_digit(content_split[1])
        try:
            banned_id = int(banned_id)
        except:
            embed = discord.Embed(title="Member Not Found", description="You need to include the Member after p!unban!\nCorrect syntax - `p!unban <member id or mention>`",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        
        try:
            banned = await client.fetch_user(banned_id)
        except discord.errors.NotFound:
            embed = discord.Embed(title="Member Not Found", description="You need to include the Member after p!unban!\nCorrect syntax - `p!unban <member id or mention>`",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        
        print("this is to be banned: ", banned_id, banned, message.guild)
        if banned == None:
            embed = discord.Embed(title="Member Not Found", description="You need to include the Member after p!unban!\nCorrect syntax - `p!unban <member id or mention>`",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title=f"Unbanned {banned}", color=16711680,
                                  description=f"**Moderator: **<@{int(member.id)}>\n**Action: **unban", timestamp=datetime.datetime.now(datetime.timezone.utc))
            await message.channel.send(embed=embed)
            await punish_log(embed=embed)
            await message.guild.unban(banned, reason=f"Unbanned by {member}")

    else:
        await channel.send(embed=await Not_enough_perms())


async def unmute(message):
    try:
        await message.delete()
    except discord.NotFound:
        print("message not found D:")
    content = message.content
    member = message.author
    channel = message.channel
    print(member.id, type(member.id))
    
    if member.guild_permissions.mute_members:
        print("has perms")
        content_split = await split(content, 2)
        banned_id = await get_digit(content_split[1])
        try:
            banned_id = int(banned_id)
        except:
            embed = discord.Embed(title="Member Not Found", description="You need to include the Member after p!unmute!\nCorrect syntax - `p!unmute <member id or mention>`",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        
        try:
            banned = await client.fetch_user(banned_id)
        except discord.errors.NotFound:
            embed = discord.Embed(title="Member Not Found", description="You need to include the Member after p!unmute!\nCorrect syntax - `p!unmute <member id or mention>`",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        
        print("this is to be banned: ", banned_id, banned, message.guild)
        if banned == None:
            embed = discord.Embed(title="Member Not Found", description="You need to include the Member after p!unmute!\nCorrect syntax - `p!unmute <member id or mention>`",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
        else:
            role_check = discord.utils.get(message.guild.roles, name="Muted")
            mute_role = get(message.guild.roles, name="Muted")
            embed = discord.Embed(title=f"Unmuted {banned}", color=16711680,
                                  description=f"**Moderator: **<@{int(member.id)}>\n**Action: **unmute", timestamp=datetime.datetime.now(datetime.timezone.utc))
            await message.channel.send(embed=embed)
            await punish_log(embed=embed)
            try:
                await banned.remove_roles(mute_role)
            except:
                print("class helper")
    else:
        await channel.send(embed=await Not_enough_perms())



async def unban_service(message):
    try:
        await message.delete()
    except discord.NotFound:
        print("message not found D:")
        
    content = message.content
    member = message.author
    channel = message.channel
    print(member.id, type(member.id))
    if member.guild_permissions.mute_members:
        print("has perms")
        content_split = await split(content, 2)
        banned_id = await get_digit(content_split[1])
        try:
            banned_id = int(banned_id)
        except:
            embed = discord.Embed(title="Member Not Found", description="You need to include the Member after p!service-unban!\nCorrect syntax - `p!service-unban <member id or mention>`",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        
        try:
            banned = await client.fetch_user(banned_id)
        except discord.errors.NotFound:
            embed = discord.Embed(title="Member Not Found", description="You need to include the Member after p!service-unban!\nCorrect syntax - `p!service-unban <member id or mention>`",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        
        print("this is to be banned: ", banned_id, banned, message.guild)
        if banned == None:
            embed = discord.Embed(title="Member Not Found", description="You need to include the Member after p!service-unban!\nCorrect syntax - `p!service-unban <member id or mention>`",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
        else:
            role_add = discord.utils.get(
                message.guild.roles, name="Service Blacklisted")
            role_remove = discord.utils.get(
                message.guild.roles, name="Can see services")
            embed = discord.Embed(title=f"Service Unbanned {banned}", color=16711680,
                                  description=f"**Moderator: **<@{int(member.id)}>\n**Action: **unmute", timestamp=datetime.datetime.now(datetime.timezone.utc))
            await message.channel.send(embed=embed)
            await punish_log(embed=embed)
            try:
                await banned.add_roles(role_add)
                await banned.remove_roles(role_remove)
            except:
                print("class helper")
    else:
        await channel.send(embed=await Not_enough_perms())



async def TempBan(message):
    member = message.author
    channel = message.channel
    content = message.content
    try:
        await message.delete()
    except discord.errors.NotFound:
        print("not found")
    if member.guild_permissions.kick_members:
        content_split = await split(content, 2)
        print(content_split)
        banned_id = content_split[1]
        banned_id = await get_digit(banned_id)
        try:
            banned_id = int(banned_id)
        except:
            embed = discord.Embed(
                title="Member Not Found", description="You need to include the Member after p!tempban!\nCorrect syntax - `p!tempban <member id or mention> (time) [reason for ban]`", timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        
        try:
            banned = await client.fetch_user(banned_id)
        except discord.errors.NotFound:
            embed = discord.Embed(title="Member Not Found", description="either the member id is wrong or the member disabled/deleted their account",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=16711680)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        
        possible_time = await split(content_split[2], 9999)
        print(possible_time)
        # del possible_time(5)
        sec = await convert_possible_time_to_sec(possible_time)
        print("sec was: ", sec)
        reason_worded = possible_time[sec[1]:]
        reason = ' '.join([str(elem) for elem in reason_worded])
        sec_human = possible_time[0:sec[1]]
        sec: str = sec[0]
        if str(sec) == "0":
            await message.channel.send(embed=await Invalid_Time_send())
            return
        sec_human = ' '.join([str(elem) for elem in sec_human])
        
        if reason == "":
            def check(message):
                print("checking for reason")
                return message.channel == channel and message.author == member
            try:
                embed = discord.Embed(
                    title="Banning member", description=f"Why do you want to ban <@{banned_id}> for {sec_human}", color=16711680, timestamp=datetime.datetime.now(datetime.timezone.utc))
                embed.set_footer(text="Paradise Bot")
                await message.channel.send(embed=embed, delete_after=15)
                print("checking for reason")
                reason = await client.wait_for('message', timeout=15.0, check=check)
                reason = reason.content
                print(reason)
            except asyncio.TimeoutError:
                await message.channel.send("Oh Well, I did not get the reason in time, too bad i can't ban without reason :(")
                return
            
        done: bool = False
        while done == False:
            try:
                Cursor.execute(
                    "SELECT User_id FROM Transactions WHERE Transaction='unban'")
            except mysql.connector.errors.DatabaseError:
                await asyncio.sleep(2)
                Cursor.execute(
                    "SELECT User_id FROM Transactions WHERE Transaction='unban'")
                done = True
            else:
                done = True
        members_on_cooldown = Cursor.fetchall()
        print(members_on_cooldown)
        members_on_cooldown = await read_member_id(members_on_cooldown)
        if str(banned_id) in members_on_cooldown:
            prepare = f"""DELETE FROM Transactions 
            WHERE User_id='{str(banned_id)}'
            AND Transaction= 'unban'"""
            Cursor.execute(prepare)
        time_in_future = await time_future(sec)
        Cursor.execute(f'''INSERT INTO Transactions (User_id,Duration,reason,Transaction,`Mod`)
        VALUES ('{banned_id}','{await unaware_timezone(time_in_future)}','{reason}','unban','{str(member.id)}')''')
        prepare = f'''SELECT MAX(`case_id`) FROM PunishmentLogs'''
        Cursor.execute(prepare)
        case_id = Cursor.fetchall()
        print("Heres the case_id: ", case_id)
        case_id = (case_id[0][0])
        try:
            case_id = int(case_id)
        except:
            case_id = 0
        else:
            case_id += 1
        time_now = datetime.datetime.now(datetime.timezone.utc)
        time_now = await unaware_timezone(time_now)
        prepare = f'''INSERT INTO PunishmentLogs (`User_id`,`Duration`,`reason`,`Mod`,`action`,`time`,`case_id`)
        VALUES ('{banned_id}','{sec}','{reason}','{str(member.id)}','tempban','{time_now}','{case_id}')'''
        Cursor.execute(prepare)
        duration = sec
        duration = await sec_to_time(int(duration))
        if duration == "":
            duration = "Doesn't Apply to bans and warns"
        embed = discord.Embed(title=f"Case #{case_id} has been registered!", color=16711680,
                              description=f"**Offender: **<@{banned_id}>\n**Moderator: **<@{int(member.id)}>\n**Action: **Ban\n**Duration: **{duration}\n**Reason: **{reason}", timestamp=datetime.datetime.now(datetime.timezone.utc))
        try:
            dm = await banned.create_dm()
        except:
            print("can't dm member")
        else:
            await dm.send(f"You have been banned in Paradise network by <@{member.id}>\nReason of ban: {reason}\nDuration: {duration}")
        embed.set_footer(text="Paradise Bot")
        embed.set_thumbnail(url=banned.avatar_url)
        await message.channel.send(embed=embed)
        await punish_log(embed=embed)
        await message.guild.ban(banned, reason=reason, delete_message_days=0)

    else:
        await channel.send(embed=await Not_enough_perms())


async def Tempmute(message):
    member = message.author
    channel = message.channel
    content = message.content
    try:
        await message.delete()
    except discord.errors.NotFound:
        print("not found")
    if member.guild_permissions.mute_members:
        content_split = await split(content, 2)
        print(content_split)
        muted_id = content_split[1]
        muted_id = await get_digit(muted_id)
        try:
            muted_id = int(muted_id)
        except:
            embed = discord.Embed(
                title="Member Not Found", description="You need to include the Member after p!mute!\nCorrect syntax - `p!mute <member id or mention> (time) [reason for mute]`", timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        print('muted-id: ', muted_id)
        try:
            muted = await message.guild.fetch_member(muted_id)
        except discord.errors.NotFound:
            embed = discord.Embed(
                title="Member Not Found", description="Either the member id is wrong or the member is not in this server....\nCorrent syntax - `p!mute <member id or member mention> (time) [reason for mute]`", timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            print('muted-id: ', muted_id)
            return
        if muted == None:
            print(muted_id, muted)
            embed = discord.Embed(
                title="Member Not Found", description="Either the member id is wrong or the member is not in this server....\nCorrent syntax - `p!mute <member id or member mention> (time) [reason for mute]`", timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        try:
            possible_time = await split(content_split[2], 9999)
        except IndexError:
            await message.channel.send(embed=await Invalid_Time_send())
            return
        print(possible_time)
        # del possible_time(5)
        sec = await convert_possible_time_to_sec(possible_time)
        print("sec was: ", sec)
        reason_worded = possible_time[sec[1]:]
        reason = ' '.join([str(elem) for elem in reason_worded])
        sec_human = possible_time[0:sec[1]]
        sec: str = sec[0]
        if str(sec) == "0":
            await message.channel.send(embed=await Invalid_Time_send())
            return
        sec_human = ' '.join([str(elem) for elem in sec_human])
        if reason == "":
            def check(message):
                print("checking for reason")
                return message.channel == channel and message.author == member
            try:
                embed = discord.Embed(
                    title="Muting member", description=f"Why do you want to mute <@{muted_id}> for {sec_human}", color=16776960, timestamp=datetime.datetime.now(datetime.timezone.utc))
                embed.set_footer(text="Paradise Bot")
                await message.channel.send(embed=embed, delete_after=15)
                print("checking for reason")
                reason = await client.wait_for('message', timeout=15.0, check=check)
                reason = reason.content
                print(reason)
            except asyncio.TimeoutError:
                await message.channel.send("Oh Well, I did not get the reason in time, too bad i can't mute without reason :(")
                return
            
        await message.channel.send(f"Heres the time in calc in (sec): {sec} \n Reason: {reason}")
        done: bool = False
        while done == False:
            try:
                Cursor.execute(
                    "SELECT User_id FROM Transactions WHERE Transaction='unmute'")
            except mysql.connector.errors.DatabaseError:
                await asyncio.sleep(2)
                Cursor.execute(
                    "SELECT User_id FROM Transactions WHERE Transaction='unmute'")
                done = True
            else:
                done = True
        members_on_cooldown = Cursor.fetchall()
        print(members_on_cooldown)
        members_on_cooldown = await read_member_id(members_on_cooldown)
        
        if str(muted_id) in members_on_cooldown:
            prepare = f"""DELETE FROM Transactions 
            WHERE User_id='{str(muted_id)}'
            AND Transaction= 'unmute'"""
            Cursor.execute(prepare)
            
        mute_role = get(member.guild.roles, name="Muted")
        await muted.add_roles(mute_role)
        time_in_future = await time_future(sec)
        prepare = f'''INSERT INTO Transactions (User_id,Duration,reason,Transaction,`Mod`)
        VALUES ('{muted_id}','{await unaware_timezone(time_in_future)}','{reason}','unmute','{str(member.id)}')'''
        Cursor.execute(prepare)
        time_now = datetime.datetime.now(datetime.timezone.utc)
        time_now = await unaware_timezone(time_now)
        prepare = f'''SELECT MAX(`case_id`) FROM PunishmentLogs'''
        Cursor.execute(prepare)
        case_id = Cursor.fetchall()
        print("Heres the case_id: ", case_id)
        case_id = (case_id[0][0])
        try:
            case_id = int(case_id)
        except:
            case_id = 0
        else:
            case_id += 1
            
        prepare = f'''INSERT INTO PunishmentLogs (`User_id`,`Duration`,`reason`,`Mod`,`action`,`time`,`case_id`)
        VALUES ('{muted_id}','{sec}','{reason}','{str(member.id)}','tempmute','{time_now}','{case_id}')'''
        duration = sec
        duration = await sec_to_time(int(duration))
        if duration == "":
            duration = "Doesn't Apply to bans and warns"
        embed = discord.Embed(title=f"Case #{case_id} has been registered!", color=16711680,
                              description=f"**Offender: **<@{muted_id}>\n**Moderator: **<@{int(member.id)}>\n**Action: **Mute\n**Duration: **{duration}\n**Reason: **{reason}", timestamp=datetime.datetime.now(datetime.timezone.utc))
        try:
            dm = await muted.create_dm()
        except:
            print("can't send dm")
        else:
            await dm.send(f"You have been muted in Paradise network by <@{member.id}>\nReason of mute: {reason}\nDuration: {duration}")
        embed.set_footer(text="Paradise Bot")
        embed.set_thumbnail(url=muted.avatar_url)
        await punish_log(embed=embed)
        await message.channel.send(embed=embed)
        Cursor.execute(prepare)
    else:
        await channel.send(embed=await Not_enough_perms())


async def logs_user(message):
    member = message.author
    channel = message.channel
    content = message.content
    try:
        await message.delete()
    except discord.errors.NotFound:
        print("not found")
    if member.guild_permissions.mute_members:
        content_split = await split(content, 2)
        print(content_split)
        try:
            log_id = content_split[1]
        except IndexError:
            embed = discord.Embed(title="Incorrect syntax...", description="The correct syntax is `p!punishments <member id or mention> (`**`optional-`**`page number)`",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        
        log_id = await get_digit(log_id)
        try:
            log_id = int(log_id)
        except:
            embed = discord.Embed(title="Incorrect syntax...", description="The correct syntax is `p!punishments <member id or mention> (`**`optional-`**`page number)`",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        
        print('log-id: ', log_id)
        try:
            page_no = await get_digit(content_split[2])
            if page_no == '':
                page_no = 1
            page_no = int(page_no)-1
        except IndexError:
            page_no: int = 0
        if page_no == '':
            page_no: int = 0
        try:
            log_user = await client.fetch_user(log_id)
            print("the user i found: ", log_user)
        except discord.errors.NotFound:
            embed = discord.Embed(title="Member Not Found", description="The member id is wrong",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        if log_user == None:
            embed = discord.Embed(title="Member Not Found", description="The member id is wrong....",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        
        prepare = f'''SELECT * FROM PunishmentLogs WHERE `User_id`='{log_id}'
        ORDER BY case_id DESC'''
        Cursor.execute(prepare)
        cases = Cursor.fetchall()
        for i in cases:
            print(i)
        if len(cases) < 1:
            await channel.send("The Person has no punishment in logs")
            return
        pages: list = []
        page_carry: list = []
        for item in enumerate(cases):
            count = item[0]
            count = int(count)
            page_carry.append(count)
            if count % 10 == 9 % 10:
                pages.append(page_carry)
                page_carry = ['class helper']
                page_carry.clear()
        if len(page_carry) > 0:
            pages.append(page_carry)
        print(page_carry)
        print("\n", pages)
        print("\n \n")
        try:
            page = pages[page_no]
        except IndexError:
            page = pages[0]
            page_no = 0
        embed = discord.Embed(title=f"{log_user} ({int(log_id)})", timestamp=datetime.datetime.now(
            datetime.timezone.utc), color=26861)
        embed.set_footer(
            text=f"Paradise Bot  Page Number {int(page_no)+1} out of {len(pages)}")
        embed.set_thumbnail(url=log_user.avatar_url)
        for page_number in page:
            page_number = int(page_number)
            case = cases[page_number]
            embed.add_field(
                name=f"Case #{case[6]} - {case[4]}", value=case[2], inline=False)
        await message.channel.send(embed=embed)
    else:
        await channel.send(embed=await Not_enough_perms())

async def case(message):
    member = message.author
    channel = message.channel
    content = message.content
    try:
        await message.delete()
    except discord.errors.NotFound:
        print("not found")
    if member.guild_permissions.mute_members:
        content_split = await split(content, 2)
        try:
            item_id = content_split[1]
        except IndexError:
            embed = discord.Embed(title="Invalid syntax!", description="The correct syntax is `p!case {case number}`", timestamp=datetime.datetime.now(
                datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await channel.send(embed=embed)
            return
        
        item_id = await get_digit(item_id)
        try:
            item_id = int(item_id)
        except:
            embed = discord.Embed(title="Invalid syntax!", description="The correct syntax is `p!case {case number}`", timestamp=datetime.datetime.now(
                datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await channel.send(embed=embed)
            return
        
        prepare = f'''Select * From PunishmentLogs WHERE `case_id`='{item_id}' '''
        Cursor.execute(prepare)
        Case = Cursor.fetchall()
        try:
            Case = Case[0]
        except IndexError:
            embed = discord.Embed(title="No Case found!", description="No such case found in the database, please check the case id.\nThe case might have been removed by other staff members",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await channel.send(embed=embed)
            return
        
        log_user = await client.fetch_user(int(Case[3]))
        print("log user-: ", log_user, "\nId: ", int(Case[3]))
        offender = await client.fetch_user(int(Case[0]))
        print("Offender user-: ", offender, "\nId: ", int(Case[0]))
        duration = Case[1]
        duration = await sec_to_time(int(duration))
        if duration == "":
            duration = "Doesn't Apply to bans and warns"
        embed = discord.Embed(title=f"{offender} ({int(Case[3])})", timestamp=Case[5], color=26861,
                              description=f"**Offender: **<@{offender.id}>\n**Moderator: **<@{log_user.id}>\n**Action: **{Case[4]}\n**Duration: **{duration}\n**Reason: **{Case[2]}")
        embed.set_footer(text=f"Paradise Bot  - Case #{Case[6]}")
        embed.set_thumbnail(url=offender.avatar_url)
        await channel.send(embed=embed)
    else:
        await channel.send(embed=await Not_enough_perms())


async def remove_case(message):
    member = message.author
    channel = message.channel
    content = message.content
    try:
        await message.delete()
    except discord.errors.NotFound:
        print("not found")
    if member.guild_permissions.ban_members:
        content_split = await split(content, 2)
        try:
            item_id = content_split[1]
        except IndexError:
            embed = discord.Embed(title="Invalid syntax!", description="The correct syntax is `p!removecase {case id}`", timestamp=datetime.datetime.now(
                datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await channel.send(embed=embed)
            return
        
        item_id = await get_digit(item_id)
        try:
            item_id = int(item_id)
        except:
            embed = discord.Embed(title="Invalid syntax!", description="The correct syntax is `p!removecase {case id}`", timestamp=datetime.datetime.now(
                datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await channel.send(embed=embed)
            return
        
        prepare = f'''Select * From PunishmentLogs WHERE `case_id`='{item_id}' '''
        Cursor.execute(prepare)
        Case = Cursor.fetchall()
        try:
            Case = Case[0]
        except IndexError:
            embed = discord.Embed(title="No Case found!", description="No such case found in the database, please check the case id.\nThe case might have been removed by other staff members",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await channel.send(embed=embed)
            return
        
        prepare = f'''DELETE FROM PunishmentLogs WHERE `case_id`='{item_id}' '''
        Cursor.execute(prepare)
        embed = discord.Embed(title=f"Case - #{int(Case[6])}", description=f"Case#{int(Case[6])} has been sucessfully deleted!\nModerator - <@{member.id}>",
                              timestamp=datetime.datetime.now(datetime.timezone.utc), color=16711680)
        embed.set_footer(
            text=f"Paradise Bot  - Case #{Case[6]}", icon_url=member.avatar_url)
        await channel.send(embed=embed)
        await punish_log(embed=embed)
    else:
        await channel.send(embed=await Not_enough_perms())
async def change_reason(message):
    member = message.author
    channel = message.channel
    content = message.content
    try:
        await message.delete()
    except discord.errors.NotFound:
        print("not found")
    if member.guild_permissions.kick_members:
        content_split = await split(content, 2)
        try:
            item_id = content_split[1]
        except IndexError:
            embed = discord.Embed(title="Invalid syntax!", description="The correct syntax is `p!reason {case id} [new reason]`", timestamp=datetime.datetime.now(
                datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await channel.send(embed=embed)
            return
        
        item_id = await get_digit(item_id)
        try:
            item_id = int(item_id)
        except:
            embed = discord.Embed(title="Invalid syntax!", description="The correct syntax is `p!reason {case id} [new reason]`", timestamp=datetime.datetime.now(
                datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await channel.send(embed=embed)
            return
        
        prepare = f'''Select * From PunishmentLogs WHERE `case_id`='{item_id}' '''
        Cursor.execute(prepare)
        Case = Cursor.fetchall()

        def check(message):
            print("checking for reason")
            return message.channel == channel and message.author == member
        try:
            Case = Case[0]
        except IndexError:
            embed = discord.Embed(title="No Case found!", description="No such case found in the database, please check the case id.\nThe case might have been removed by other staff members",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await channel.send(embed=embed)
            return
        
        try:
            reason = content_split[2]
        except IndexError:
            try:
                embed = discord.Embed(
                    title="Changing reason", description=f"What is the new reason for Case #{item_id}", color=65280, timestamp=datetime.datetime.now(datetime.timezone.utc))
                embed.set_footer(text="Paradise Bot")
                await message.channel.send(embed=embed, delete_after=15)
                print("checking for reason")
                reason = await client.wait_for('message', timeout=15.0, check=check)
                reason = reason.content
                print(reason)
            except asyncio.TimeoutError:
                await message.channel.send("Oh Well, I did not get the reason in time, too bad i can't mute without reason :(")
                return
            
        if reason == '':
            try:
                embed = discord.Embed(
                    title="Changing reason", description=f"What is the new reason for Case #{item_id}", color=65280, timestamp=datetime.datetime.now(datetime.timezone.utc))
                embed.set_footer(text="Paradise Bot")
                await message.channel.send(embed=embed, delete_after=15)
                print("checking for reason")
                reason = await client.wait_for('message', timeout=15.0, check=check)
                reason = reason.content
                print(reason)
            except asyncio.TimeoutError:
                await message.channel.send("Oh Well, I did not get the reason in time, too bad i can't mute without reason :(")
                return
            
        prepare = f'''DELETE FROM PunishmentLogs WHERE `case_id`='{item_id}' '''
        Cursor.execute(prepare)
        prepare = f'''INSERT INTO PunishmentLogs (`User_id`,`Duration`,`reason`,`Mod`,`action`,`time`,`case_id`)
            VALUES ('{Case[0]}','{Case[1]}','{reason}','{Case[3]}','{Case[4]}','{Case[5]}','{Case[6]}')'''
        Cursor.execute(prepare)
        embed = discord.Embed(title=f"Case - #{int(Case[6])}", description=f"**Case #{int(Case[6])}** Reason has been sucessfully updated!\n**Old reason: **{Case[2]}\n**New reason: **{reason}\nModerator: <@{member.id}>",
                              timestamp=datetime.datetime.now(datetime.timezone.utc), color=16711680)
        embed.set_footer(
            text=f"Paradise Bot  - Case #{Case[6]}", icon_url=member.avatar_url)
        await channel.send(embed=embed)
        await punish_log(embed=embed)
    else:
        await channel.send(embed=await Not_enough_perms())


async def warn(message):
    try:
        await message.delete()
    except discord.NotFound:
        print("message not found D:")
    content = message.content
    member = message.author
    channel = message.channel
    print(member.id, type(member.id))
    if member.guild_permissions.manage_messages:
        print("has perms")
        content_split = await split(content, 2)
        try:
            warned_id = content_split[1]
        except IndexError:
            embed = discord.Embed(
                title="Invalid syntax", description="You need to include the Member after p!warn!\nCorrect syntax - `p!warn <member id or mention> [reason for warn]`", timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        
        warned_id = await get_digit(warned_id)
        try:
            warned_id = int(warned_id)
        except:
            embed = discord.Embed(
                title="Invalid syntax", description="You need to include the Member after p!warn!\nCorrect syntax - `p!warn <member id or mention> [reason for warn]`", timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        
        try:
            warned = await client.fetch_user(warned_id)
        except discord.errors.NotFound:
            embed = discord.Embed(title="Member Not Found", description="Either the member id is wrong or the member is not in this server\nCorrect syntax - `p!warn <member id or mention> [reason for warn]`",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        
        print("this is to be banned: ", warned_id, warned, message.guild)
        if warned == None:
            embed = discord.Embed(title="Member Not Found", description="Either the member id is wrong or the member is not in this server\nCorrect syntax - `p!warn <member id or mention> [reason for warn]`",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        else:
            def check(message):
                print("checking for reason")
                return message.channel == channel and message.author == member
            try:
                reason = content_split[2]
            except IndexError:
                try:
                    embed = discord.Embed(
                        title="Warning member", description=f"Why do you want to warn <@{warned_id}>", color=16711680, timestamp=datetime.datetime.now(datetime.timezone.utc))
                    embed.set_footer(text="Paradise Bot")
                    await message.channel.send(embed=embed, delete_after=15)
                    print("checking for reason")
                    reason = await client.wait_for('message', timeout=15.0, check=check)
                    reason = reason.content
                    print(reason)
                except asyncio.TimeoutError:
                    await message.channel.send("Oh Well, I did not get the reason in time, too bad i can't warn without reason :(", delete_after=5)
                    return
                
            if reason == '':
                try:
                    embed = discord.Embed(
                        title="Warning member", description=f"Why do you want to warn <@{warned_id}>", color=16711680, timestamp=datetime.datetime.now(datetime.timezone.utc))
                    embed.set_footer(text="Paradise Bot")
                    await message.channel.send(embed=embed, delete_after=15)
                    print("checking for reason")
                    reason = await client.wait_for('message', timeout=15.0, check=check)
                    reason = reason.content
                    print(reason)
                except asyncio.TimeoutError:
                    await message.channel.send("Oh Well, I did not get the reason in time, too bad i can't warn without reason :(")
                    return
                
            prepare = f'''SELECT MAX(`case_id`) FROM PunishmentLogs'''
            Cursor.execute(prepare)
            case_id = Cursor.fetchall()
            print("Heres the case_id: ", case_id)
            case_id = (case_id[0][0])
            try:
                case_id = int(case_id)
            except:
                case_id = 0
            else:
                case_id += 1
            time_now = datetime.datetime.now(datetime.timezone.utc)
            time_now = await unaware_timezone(time_now)

            embed = discord.Embed(title=f"Case #{case_id} has been registered!", color=16711680,
                                  description=f"**Offender: **<@{warned_id}>\n**Moderator: **<@{int(member.id)}>\n**Action: **Warn\n**Reason: **{reason}", timestamp=datetime.datetime.now(datetime.timezone.utc))
            try:
                dm = await warned.create_dm()
            except:
                print("can't dm member")
            else:
                await dm.send(f"You have been warned in Paradise network by <@{member.id}>\nReason of warn: {reason}")
            embed.set_footer(text="Paradise Bot")
            embed.set_thumbnail(url=warned.avatar_url)
            await message.channel.send(embed=embed)
            await punish_log(embed=embed)
            prepare = f'''INSERT INTO PunishmentLogs (`User_id`,`Duration`,`reason`,`Mod`,`action`,`time`,`case_id`)
               VALUES ('{warned_id}','0','{reason}','{str(member.id)}','warn','{time_now}','{case_id}')'''

            Cursor.execute(prepare)
    else:
        await channel.send(embed=await Not_enough_perms())


async def temp_service_ban(message):
    member = message.author
    channel = message.channel
    content = message.content
    try:
        await message.delete()
    except discord.errors.NotFound:
        print("not found")
    if member.guild_permissions.kick_members:
        content_split = await split(content, 2)
        print(content_split)
        try:
            banned_id = content_split[1]
        except IndexError:
            embed = discord.Embed(
                title="Invalid syntax", description="You need to include the Member after p!serviceban!\nCorrect syntax - `p!serviceban <member id or mention> (time) [reason for warn]`", timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        
        banned_id = await get_digit(banned_id)
        try:
            banned_id = int(banned_id)
        except:
            embed = discord.Embed(
                title="Member Not Found", description="You need to include the Member after p!serviceban!\nCorrect syntax - `p!serviceban <member id or mention> (time) [reason for warn]`", timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        
        print('banned-id: ', banned_id)
        try:
            banned = await message.guild.fetch_member(banned_id)
        except discord.errors.NotFound:
            embed = discord.Embed(title="Member Not Found", description="Either the member id is wrong or the member is not in this server\nCorrect syntax - `p!serviceban <member id or mention> (time) [reason for warn]`",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            print('muted-id: ', banned_id)
            return
        
        if banned == None:
            print(banned_id, banned)
            embed = discord.Embed(title="Member Not Found", description="Either the member id is wrong or the member is not in this server\nCorrect syntax - `p!serviceban <member id or mention> (time) [reason for warn]`",
                                  timestamp=datetime.datetime.now(datetime.timezone.utc), color=65280)
            embed.set_footer(text="Paradise Bot")
            await message.channel.send(embed=embed)
            return
        
        try:
            possible_time = await split(content_split[2], 9999)
        except IndexError:
            await message.channel.send(embed=await Invalid_Time_send())
            return
        
        print(possible_time)
        # del possible_time(5)
        sec = await convert_possible_time_to_sec(possible_time)
        print("sec was: ", sec)
        reason_worded = possible_time[sec[1]:]
        reason = ' '.join([str(elem) for elem in reason_worded])
        sec_human = possible_time[0:sec[1]]
        sec: str = sec[0]
        if str(sec) == "0":
            await message.channel.send(embed=await Invalid_Time_send())
            return
        
        sec_human = ' '.join([str(elem) for elem in sec_human])
        if reason == "":
            def check(message):
                print("checking for reason")
                return message.channel == channel and message.author == member
            try:
                embed = discord.Embed(title="Service Banning member",
                                      description=f"Why do you want to service Ban <@{banned_id}> for {sec_human}", color=16711680, timestamp=datetime.datetime.now(datetime.timezone.utc))
                embed.set_footer(text="Paradise Bot")
                await message.channel.send(embed=embed, delete_after=15)
                print("checking for reason")
                reason = await client.wait_for('message', timeout=15.0, check=check)
                reason = reason.content
                print(reason)
            except asyncio.TimeoutError:
                await message.channel.send("Oh Well, I did not get the reason in time, too bad i can't service ban without reason :(")
                return
            
        await message.channel.send(f"Heres the time in calc in (sec): {sec} \n Reason: {reason}")
        done: bool = False
        while done == False:
            try:
                Cursor.execute(
                    "SELECT User_id FROM Transactions WHERE Transaction='unbanservice'")
            except mysql.connector.errors.DatabaseError:
                await asyncio.sleep(2)
                Cursor.execute(
                    "SELECT User_id FROM Transactions WHERE Transaction='unbanservice'")
                done = True
            else:
                done = True
        members_on_cooldown = Cursor.fetchall()
        print(members_on_cooldown)
        members_on_cooldown = await read_member_id(members_on_cooldown)
        
        if str(banned_id) in members_on_cooldown:
            prepare = f"""DELETE FROM Transactions 
            WHERE User_id='{str(banned_id)}'
            AND Transaction= 'unbanservice'"""
            Cursor.execute(prepare)
        role_add = discord.utils.get(
            message.guild.roles, name="Service Blacklisted")
        role_remove = discord.utils.get(
            message.guild.roles, name="Can see services")
        await banned.add_roles(role_add)
        await banned.remove_roles(role_remove)
        time_in_future = await time_future(sec)
        prepare = f'''INSERT INTO Transactions (User_id,Duration,reason,Transaction,`Mod`)
        VALUES ('{banned_id}','{await unaware_timezone(time_in_future)}','{reason}','unbanservice','{str(member.id)}')'''
        Cursor.execute(prepare)
        time_now = datetime.datetime.now(datetime.timezone.utc)
        time_now = await unaware_timezone(time_now)
        prepare = f'''SELECT MAX(`case_id`) FROM PunishmentLogs'''
        Cursor.execute(prepare)
        case_id = Cursor.fetchall()
        print("Heres the case_id: ", case_id)
        case_id = (case_id[0][0])
        
        try:
            case_id = int(case_id)
        except:
            case_id = 0
        else:
            case_id += 1
        prepare = f'''INSERT INTO PunishmentLogs (`User_id`,`Duration`,`reason`,`Mod`,`action`,`time`,`case_id`)
        VALUES ('{banned_id}','{sec}','{reason}','{str(member.id)}','service-ban','{time_now}','{case_id}')'''
        duration = sec
        duration = await sec_to_time(int(duration))
        if duration == "":
            duration = "Doesn't Apply to bans and warns"
        embed = discord.Embed(title=f"Case #{case_id} has been registered!", color=16711680,
                              description=f"**Offender: **<@{banned_id}>\n**Moderator: **<@{int(member.id)}>\n**Action: **Service Ban\n**Duration: **{duration}\n**Reason: **{reason}", timestamp=datetime.datetime.now(datetime.timezone.utc))
        
        try:
            dm = await banned.create_dm()
        except:
            print("can't dm member")
        else:
            await dm.send(f"You have been service banned in Paradise network by <@{member.id}>\nReason of warn: {reason}\nDuration: {duration}")
        embed.set_footer(text="Paradise Bot")
        embed.set_thumbnail(url=banned.avatar_url)
        await message.channel.send(embed=embed)
        await punish_log(embed=embed)
        Cursor.execute(prepare)
    else:
        await channel.send(embed=await Not_enough_perms())

