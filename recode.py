import asyncio
import discord
from discord.ext import commands
import datetime
import re
from threading import Thread
import time
from discord.utils import get
import discord.errors
bot = discord.Client()
import mysql.connector
import os
Database = mysql.connector.connect(
  host="localhost",
  user="root",
  password="login",
  autocommit=True
)
from time import strftime
strftime("%Y-%m-%d %H:%M:%S")
from threading import Thread
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
Cursor=Database.cursor()
Cursor.execute("USE ParadiseBot")
ipgrab = ["GRABIFYLINK", "LEANCODINGCO", "SIOPIFY", "FREEGIFICARDSCO", "CURIOUSCAICLUB", "CAISNIHINGSFUN", "JOINMYSIIE",
          "CAISNIHINGSCOM", "IPLOGGERORG", "BLASZECOM", "WEBRESOLVERNL", "CURLV", "SHORIESI", "BIIURLIO", "RURLCO",
          "IPLOGGERCOM", "IPLOGGERRU", "2NOCO", "YIPSU"]
blocked_word = ['NIGGA', 'NIGGER', "NIGG", "REGIN", "IMAGPX", "REGGIN", "FAGGOT", "RETARD", "CUNT","OOOL"]
secretcode = ['p!autodelete']
time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
Invalid_Time = discord.Embed(title="Invalid Time format",description="'s' for seconds\n'm' for minutes\n'h for hours'\n 'd' for days\n 'w' for weeks",color=0x00ff00)
Invalid_Time.add_field(name="Please use this format", value="This is not case sensitive",inline=False)
transactionmanager_online='0'

async def read_member_id(members):
    members_list:list=[]
    for member in members:
        members_list.append(str(member[0]))
    return members_list
async def unaware_timezone(time_now):
    sec=time_now.second
    minute=time_now.minute
    hour=time_now.hour
    day=time_now.day
    month=time_now.month
    year=time_now.year
    #print ("======================")
    #print (time_now)
    #print (year,month,day,hour,minute,sec)
    return datetime.datetime(year=year,month=month,day=day,hour=hour,minute=minute,second=sec)
async def time_future(duration):
    time_now=datetime.datetime.now(datetime.timezone.utc)
    duration=int(duration)
    minute=hour=day=0
    while duration>=60:
        minute+=1
        duration-=60
        print ("G")
    print ("hallo")
    while minute>=60:
        hour+=1
        minute-=60
    while hour>=24:
        day+=1
        hour-=24
    future_time=time_now + datetime.timedelta(minutes=minute,days=day,seconds=duration,hours=hour)
    from datetime import timezone
    timestamp = future_time.replace(tzinfo=timezone.utc)
    return future_time


async def transactionmanager():
    transactionmanager_online='1'
    print (transactionmanager_online)
    print ("Transaction Manager online")
    while True:
        transactionmanager_online='1'
        print (transactionmanager_online)
        await transactionmanager_core()
        await asyncio.sleep(60)

async def transactionmanager_core():
    Cursor.execute("SELECT * FROM Transactions WHERE Transaction='unban'")
    to_unban=Cursor.fetchall()
    print (to_unban)
    for check in to_unban:
        timer=check[1]
        time_now=datetime.datetime.now(datetime.timezone.utc)
        print (time_now)
        time_now=await unaware_timezone(time_now)
        print(timer,time_now)            
        if timer<=time_now:
            print ("checked timer")
            user_id=check[0]
            try:
                user=await bot.fetch_user(int(user_id))
            except discord.errors.NotFound:
                print ("user not found at the time of unban.")
            else:
                guild=bot.get_guild(int(674474377286516736))
                print (guild)
                await guild.unban(user,reason="Automatic Unban.")
            Cursor.execute(f"DELETE FROM Transactions WHERE User_id={user_id} AND Transaction='unban'")
    Cursor.execute("SELECT * FROM Transactions WHERE Transaction='unmute'")
    to_unmute=Cursor.fetchall()
    print (to_unmute)
    for check in to_unmute:
        timer=check[1]
        time_now=datetime.datetime.now(datetime.timezone.utc)
        print (time_now)
        time_now=await unaware_timezone(time_now)
        print(timer,time_now)            
        if timer<=time_now:
            print ("checked timer")
            user_id=check[0]
            guild=bot.get_guild(int(674474377286516736))
            #print (guild,guild.members)
            #print (type(guild),type(guild.members))
            try:
                user=await guild.fetch_member(int(user_id))
                print (user)
            except discord.errors.NotFound:
                print ("user not found at the time of unmute.")
            else:
                role_check = discord.utils.get(guild.roles, name="Muted")
                if role_check in user.roles:
                    mute_role = get(guild.roles, name="Muted")
                    await user.remove_roles(mute_role)
                else:
                    print("The person was already unmuted at the time of unmute")           
                Cursor.execute(f"DELETE FROM Transactions WHERE User_id={user_id} AND Transaction='unmute'")
    Cursor.execute("SELECT * FROM Transactions WHERE Transaction='unbanservice'")
    to_unban=Cursor.fetchall()
    print (to_unban)
    for check in to_unban:
        timer=check[1]
        time_now=datetime.datetime.now(datetime.timezone.utc)
        print (time_now)
        time_now=await unaware_timezone(time_now)
        print(timer,time_now)            
        if timer<=time_now:
            print ("checked timer")
            user_id=check[0]
            guild=bot.get_guild(int(674474377286516736))
            #print (guild,guild.members)
            #print (type(guild),type(guild.members))
            try:
                user=await guild.fetch_member(int(user_id))
                print (user)
            except discord.errors.NotFound:
                print ("user not found at the time of unmute.")
            else:
                role_remove = discord.utils.get(guild.roles, name="Service Blacklisted")
                role_add = discord.utils.get(guild.roles, name="Can see services")
                if role_remove in user.roles:
                    await user.add_roles(role_add)
                    await user.remove_roles(role_remove)
                else:
                    print("The person was already unbanned at the time of unmute")           
                Cursor.execute(f"DELETE FROM Transactions WHERE User_id={user_id} AND Transaction='unbanservice'")




async def split(content,number):
    content_list:list=[]
    content_str:str=""
    returned:bool=False
    number=int(number)
    number-=1
    content=str(content)
    content=content+" "
    print ("content recieved: ",content)
    for b in enumerate(range(len(content))):
        i=b[1]
        print (i)
        if content[i]==" ":
            content_list.append(content_str)
            print ("apppeded to list")
            content_str=""
        else:
            content_str=content_str+content[i]
        if len(content_list)-1==number:
            print ("limit found")
            print (content_list)
            try:
                optional_arg=content[i + 1:]
                content_list.append(optional_arg)
                if str(content_list[-1])=="":
                    content_list.remove(optional_arg)
            except IndexError:
                print ("No optional arguement found")
            return content_list
            returned=True
    print (content_list)
    if returned==False:
        return content_list
async def ban(ctx):
    try:
        await ctx.delete()
    except discord.NotFound:
        print ("ctx not found D:")
    content=ctx.content
    member=ctx.author
    channel=ctx.channel
    print (member.id,type(member.id))
    if member.guild_permissions.ban_members:
           print ("has perms")
           content_split=await split(content,2)
           try:
               test=content_split[2]
           except IndexError:
               embed=discord.Embed(title="Invalid Syntax!",description="Correct syntax is `p!ban <member id or mention> reason`",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
               embed.set_footer(text="Paradise Bot")
               await ctx.channel.send(embed=embed,delete_after=5)
               return
           banned_id=await get_digit(content_split[1])
           banned_id=int(banned_id)
           try:
               banned=await bot.fetch_user(banned_id)
           except discord.errors.NotFound:
               embed=discord.Embed(title="Member Not Found",description="either the member id is wrong or the member is not in this server",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
               embed.set_footer(text="Paradise Bot")
               await ctx.channel.send(embed=embed,delete_after=5)
               return
           print ("this is to be banned: ",banned_id,banned,ctx.guild)
           if banned==None:
               embed=discord.Embed(title="Member Not Found",description="You need to include the Member after p!ban!",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
               embed.set_footer(text="Paradise Bot")
               await ctx.channel.send(embed=embed,delete_after=5)
           else:
               try:
                   reason=content_split[2]
               except IndexError:
                   def check(ctx):
                       print("checking for reason")
                       return ctx.channel == channel and ctx.author == member #and ctx.content.startswith()!="p!say"

                   try:
                       embed=discord.Embed(title="Banning member",description=f"Why do you want to ban <@{banned_id}>",color=16711680,timestamp=datetime.datetime.now(datetime.timezone.utc))
                       embed.set_footer(text="Paradise Bot")
                       await ctx.channel.send(embed=embed,delete_after=15)
                       print("checking for reason")
                       reason = await bot.wait_for('message', timeout=15.0, check=check)
                       reason=reason.content
                       print (reason)
                   except asyncio.TimeoutError:
                       await ctx.channel.send("Oh Well, I did not get the reason in time, too bad i can't ban without reason :(",delete_after=5)
                       return
               prepare=f'''SELECT MAX(`case_id`) FROM PunishmentLogs'''
               Cursor.execute(prepare)
               case_id=Cursor.fetchall()
               print("Heres the case_id: ",case_id)
               case_id=(case_id[0][0])
               try:
                   case_id=int(case_id)
               except:
                   case_id=0
               else:
                   case_id+=1
               time_now=datetime.datetime.now(datetime.timezone.utc)
               time_now=await unaware_timezone(time_now)
               prepare=f'''INSERT INTO PunishmentLogs (`User_id`,`Duration`,`reason`,`Mod`,`action`,`time`,`case_id`)
               VALUES ('{banned_id}','0','{reason}','{str(member.id)}','ban','{time_now}','{case_id}')'''
               await ctx.channel.send(prepare)
               Cursor.execute(prepare)
               duration="Doesn't Apply to bans and warns"
               embed=discord.Embed(title=f"Case #{case_id} has been registered!",color=16711680,description=f"**Moderator: **<@{int(member.id)}>\n**Action: **Permanent Ban\n**Duration :**{duration}\n**Reason: **{reason}",timestamp=datetime.datetime.now(datetime.timezone.utc))
               dm=await banned.create_dm()
               await dm.send(f"You have been banned in Paradise network by <@{member.id}>\nReason of warn: {reason}\nDuration: Permanent")
               embed.set_footer(text="Paradise Bot")
               embed.set_thumbnail(url=banned.avatar_url)
               await ctx.channel.send(embed=embed)
               await ctx.guild.ban(banned,reason=reason,delete_message_days=0)

    else:  
        await channel.send("You do you not have the perms to do this",delete_after=5)
async def convert_possible_time_to_sec(possible_time):
    seconds=["s","sec","secs","seconds","second"]
    minutes=["m","min","mins","minute","minutes"]
    sec:int=0
    counter=0
    time_trial_counter=0
    time_data_started:bool=False
    for item in possible_time:
        item=str(item)
        if time_data_started==True:
           time_trial_counter+=1
           print ("heres the counters: ",counter,time_trial_counter)
           if int(counter)!=time_trial_counter:
               data=[sec,int(possible_time.index(item))-1]
               return data
        for i in seconds:
            print (i,item)
            if str(item).endswith(str(i)):
                second=item[:-int(len(i))]
                try:
                    second=int(second)
                except:
                    print("can't convert string to int")
                else:
                    sec+=second
                    time_data_started=True
                    counter+=1
        for i in minutes:
            print (i,item)
            if str(item).endswith(str(i)):
                second=item[:-int(len(i))]
                try:
                    second=int(second)
                except:
                    print("can't convert string to int")
                second=second*60
                sec+=second
                time_data_started=True
                counter+=1
    data=[sec,int(len(possible_time)-1)]
    return data

async def start_transactionmanager(ctx):
    if transactionmanager_online=='0':
        print ("Offline")
        await ctx.channel.send("Somehow The transaction manager was offline.... \nTurned it on.",delete_after=10)
        await transactionmanager()
    else:
        msg = await ctx.channel.send("Transaction manager seems to be online! \nConfirming its validation, please wait 90 seconds for the validation report.\nDo `p!forceupdate` incase you want to force refresh the transactions",delete_after=10)
        transactionmanager_online='0'
        await asyncio.sleep(90)
        if transactionmanager_online=='0':
            msg.edit(content="Seems like the transaction manager had crashed... turned it back on\n<@&674479154745573377> Please look into why it had crashed")
            await transactionmanager()

async def transactionmanager_forceupdate(ctx):
    msg = await ctx.channel.send("Force updating transactions.....")
    await transactionmanager_core()
    await msg.edit(content="Successfully Updated transactions!",delete_after=10)


async def TempBan(ctx):
    member=ctx.author
    channel=ctx.channel
    content=ctx.content
    try:
        await ctx.delete()
    except discord.errors.NotFound:
        print ("not found")
    if member.guild_permissions.ban_members:
        content_split=await split(content,2)
        print (content_split)
        banned_id=content_split[1]
        banned_id=await get_digit(banned_id)
        banned_id=int(banned_id)
        try:
           banned=await bot.fetch_user(banned_id)
        except discord.errors.NotFound:
           embed=discord.Embed(title="Member Not Found",description="either the member id is wrong or the member disabled/deleted their account",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
           embed.set_footer(text="Paradise Bot")
           await ctx.channel.send(embed=embed,delete_after=5)
           return
        possible_time=await split(content_split[2],9999)
        print (possible_time)
        #del possible_time(5)
        sec=await convert_possible_time_to_sec(possible_time)
        print ("sec was: ",sec)
        reason_worded=possible_time[sec[1]:]
        reason = ' '.join([str(elem) for elem in reason_worded])
        sec_human=possible_time[0:sec[1]]
        sec:str = sec[0]
        if str(sec)=="0":
            await ctx.channel.send(embed=Invalid_Time)
            return
        sec_human = ' '.join([str(elem) for elem in sec_human])
        if reason=="":
            def check(ctx):
                       print("checking for reason")
                       return ctx.channel == channel and ctx.author == member
            try:
                embed=discord.Embed(title="Banning member",description=f"Why do you want to ban <@{banned_id}> for {sec_human}",color=16711680,timestamp=datetime.datetime.now(datetime.timezone.utc))
                embed.set_footer(text="Paradise Bot")
                await ctx.channel.send(embed=embed,delete_after=15)
                print("checking for reason")
                reason = await bot.wait_for('message', timeout=15.0, check=check)
                reason=reason.content
                print (reason)
            except asyncio.TimeoutError:
                await ctx.channel.send("Oh Well, I did not get the reason in time, too bad i can't ban without reason :(",delete_after=5)
        await ctx.channel.send(f"Heres the time in calc in (sec): {sec} \n Reason: {reason}")
        done:bool=False
        while done==False:
            try:
                Cursor.execute("SELECT User_id FROM Transactions WHERE Transaction='unban'")
            except mysql.connector.errors.DatabaseError:
                await asyncio.sleep(2)
                Cursor.execute("SELECT User_id FROM Transactions WHERE Transaction='unban'")
                done=True
            else:
                done=True
        members_on_cooldown = Cursor.fetchall()
        print (members_on_cooldown)
        members_on_cooldown=await read_member_id(members_on_cooldown)
        if str(banned_id) in members_on_cooldown:
            print ("hes on cooldown")
            Cursor.execute(f"""SELECT * FROM Transactions 
            WHERE User_id='{str(banned_id)}'
            AND Transaction= 'unban'""")
            cooldown_info = Cursor.fetchall()
            cooldown_info=cooldown_info[0]
            print (cooldown_info)
            duration=cooldown_info[1]
            print("cooldown value: ", duration)
            duration = str(duration)
            reason=str(cooldown_info[2])
            await channel.send(f"That Person is banned until {duration} UTC \n Reason: {reason}", delete_after=10)
            return
        else:
            await ctx.guild.ban(banned,reason=reason,delete_message_days=0)
            time_in_future=await time_future(sec)
            await ctx.channel.send(f'''INSERT INTO Transactions (User_id,Duration,reason,Transaction,`Mod`)
            VALUES ({banned_id},{time_in_future},'{reason}','unban','{member.id}')''')     
            Cursor.execute(f'''INSERT INTO Transactions (User_id,Duration,reason,Transaction,`Mod`)
            VALUES ('{banned_id}','{await unaware_timezone(time_in_future)}','{reason}','unban','{str(member.id)}')''')
            prepare=f'''SELECT MAX(`case_id`) FROM PunishmentLogs'''
            Cursor.execute(prepare)
            case_id=Cursor.fetchall()
            print("Heres the case_id: ",case_id)
            case_id=(case_id[0][0])
            try:
                case_id=int(case_id)
            except:
                case_id=0
            else:
                case_id+=1
            time_now=datetime.datetime.now(datetime.timezone.utc)
            time_now=await unaware_timezone(time_now)
            prepare=f'''INSERT INTO PunishmentLogs (`User_id`,`Duration`,`reason`,`Mod`,`action`,`time`,`case_id`)
            VALUES ('{banned_id}','{sec}','{reason}','{str(member.id)}','tempban','{time_now}','{case_id}')'''
            await ctx.channel.send(prepare)
            Cursor.execute(prepare)
            duration=sec
            duration = await sec_to_time(int(duration))
            if duration=="":
                duration="Doesn't Apply to bans and warns"
            embed=discord.Embed(title=f"Case #{case_id} has been registered!",color=16711680,description=f"**Moderator: **<@{int(member.id)}>\n**Action: **Ban\n**Duration :**{duration}\n**Reason: **{reason}",timestamp=datetime.datetime.now(datetime.timezone.utc))
            dm=await banned.create_dm()
            await dm.send(f"You have been banned in Paradise network by <@{member.id}>\nReason of ban: {reason}\nDuration: {duration}")
            embed.set_footer(text="Paradise Bot")
            embed.set_thumbnail(url=banned.avatar_url)
            await ctx.channel.send(embed=embed)
    else:
        await channel.send("You do you not have the perms to do this",delete_after=5)


async def Tempmute(ctx):
    member=ctx.author
    channel=ctx.channel
    content=ctx.content
    try:
        await ctx.delete()
    except discord.errors.NotFound:
        print ("not found")
    if member.guild_permissions.mute_members:
        content_split=await split(content,2)
        print (content_split)
        muted_id=content_split[1]
        muted_id=await get_digit(muted_id)
        muted_id=int(muted_id)
        print ('muted-id: ',muted_id)
        try:
           muted=await ctx.guild.fetch_member(muted_id)
        except discord.errors.NotFound:
           embed=discord.Embed(title="Member Not Found",description="either the member id is wrong or the member is not in this server",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
           embed.set_footer(text="Paradise Bot")
           await ctx.channel.send(embed=embed,delete_after=5)
           print ('muted-id: ',muted_id)
           return
        if muted==None:
           print (muted_id,muted)
           embed=discord.Embed(title="Member Not Found",description="either the member id is wrong or the member is not in this server",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
           embed.set_footer(text="Paradise Bot")
           await ctx.channel.send(embed=embed,delete_after=5)
           return
        possible_time=await split(content_split[2],9999)
        print (possible_time)
        #del possible_time(5)
        sec=await convert_possible_time_to_sec(possible_time)
        print ("sec was: ",sec)
        reason_worded=possible_time[sec[1]:]
        reason = ' '.join([str(elem) for elem in reason_worded])
        sec_human=possible_time[0:sec[1]]
        sec:str = sec[0]
        if str(sec)=="0":
            await ctx.channel.send(embed=Invalid_Time)
            return
        sec_human = ' '.join([str(elem) for elem in sec_human])
        if reason=="":
            def check(ctx):
                       print("checking for reason")
                       return ctx.channel == channel and ctx.author == member
            try:
                embed=discord.Embed(title="Muting member",description=f"Why do you want to mute <@{muted_id}> for {sec_human}",color=16711680,timestamp=datetime.datetime.now(datetime.timezone.utc))
                embed.set_footer(text="Paradise Bot")
                await ctx.channel.send(embed=embed,delete_after=15)
                print("checking for reason")
                reason = await bot.wait_for('message', timeout=15.0, check=check)
                reason=reason.content
                print (reason)
            except asyncio.TimeoutError:
                await ctx.channel.send("Oh Well, I did not get the reason in time, too bad i can't mute without reason :(",delete_after=5)
        await ctx.channel.send(f"Heres the time in calc in (sec): {sec} \n Reason: {reason}")
        done:bool=False
        while done==False:
            try:
                Cursor.execute("SELECT User_id FROM Transactions WHERE Transaction='unmute'")
            except mysql.connector.errors.DatabaseError:
                await asyncio.sleep(2)
                Cursor.execute("SELECT User_id FROM Transactions WHERE Transaction='unmute'")
                done=True
            else:
                done=True
        members_on_cooldown = Cursor.fetchall()
        print (members_on_cooldown)
        members_on_cooldown=await read_member_id(members_on_cooldown)
        if str(muted_id) in members_on_cooldown:
            print ("hes on cooldown")
            Cursor.execute(f"""SELECT * FROM Transactions 
            WHERE User_id='{str(muted_id)}'
            AND Transaction= 'unmute'""")
            cooldown_info = Cursor.fetchall()
            cooldown_info=cooldown_info[0]
            print (cooldown_info)
            duration=cooldown_info[1]
            print("cooldown value: ", duration)
            duration = str(duration)
            reason=str(cooldown_info[2])
            await channel.send(f"That Person is muted until {duration} UTC \n Reason: {reason}", delete_after=10)
            return
        else:
            role_check = discord.utils.get(ctx.guild.roles, name="Muted")
            if role_check in muted.roles:
                await ctx.channel.send("That person is already muted, someone other bot/ admin have muted them.")
                return
            mute_role = get(member.guild.roles, name="Muted")
            await muted.add_roles(mute_role)
            time_in_future=await time_future(sec)
            prepare=f'''INSERT INTO Transactions (User_id,Duration,reason,Transaction,`Mod`)
            VALUES ('{muted_id}','{await unaware_timezone(time_in_future)}','{reason}','unmute','{str(member.id)}')'''
            #await ctx.channel.send(prepare)     
            Cursor.execute(prepare)
            time_now=datetime.datetime.now(datetime.timezone.utc)
            time_now=await unaware_timezone(time_now)
            prepare=f'''SELECT MAX(`case_id`) FROM PunishmentLogs'''
            Cursor.execute(prepare)
            case_id=Cursor.fetchall()
            print("Heres the case_id: ",case_id)
            case_id=(case_id[0][0])
            try:
                case_id=int(case_id)
            except:
                case_id=0
            else:
                case_id+=1
            prepare=f'''INSERT INTO PunishmentLogs (`User_id`,`Duration`,`reason`,`Mod`,`action`,`time`,`case_id`)
            VALUES ('{muted_id}','{sec}','{reason}','{str(member.id)}','tempmute','{time_now}','{case_id}')'''
            duration=sec
            duration = await sec_to_time(int(duration))
            if duration=="":
                duration="Doesn't Apply to bans and warns"
            embed=discord.Embed(title=f"Case #{case_id} has been registered!",color=16711680,description=f"**Moderator: **<@{int(member.id)}>\n**Action: **Mute\n**Duration :**{duration}\n**Reason: **{reason}",timestamp=datetime.datetime.now(datetime.timezone.utc))
            dm=await muted.create_dm()
            await dm.send(f"You have been muted in Paradise network by <@{member.id}>\nReason of mute: {reason}\nDuration: {duration}")
            embed.set_footer(text="Paradise Bot")
            embed.set_thumbnail(url=muted.avatar_url)
            await ctx.channel.send(embed=embed)
            await ctx.channel.send(prepare)
            Cursor.execute(prepare)
    else:
        await channel.send("You do you not have the perms to do this",delete_after=5)

async def logs_user(ctx):
    member=ctx.author
    channel=ctx.channel
    content=ctx.content
    try:
        await ctx.delete()
    except discord.errors.NotFound:
        print ("not found")
    if member.guild_permissions.kick_members:
        content_split=await split(content,2)
        print (content_split)
        log_id=content_split[1]
        log_id=await get_digit(log_id)
        log_id=int(log_id)
        print ('log-id: ',log_id)
        try:
            page_no=await get_digit(content_split[2])
            page_no=int(page_no)
        except IndexError:
            page_no:int=0
        if page_no=='':
            page_no:int=0
        try:
           log_user=await bot.fetch_user(log_id)
           print ("the user i found: ",log_user)
        except discord.errors.NotFound:
            embed=discord.Embed(title="Member Not Found",description="The member id is wrong",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
            embed.set_footer(text="Paradise Bot")
            await ctx.channel.send(embed=embed,delete_after=5)
            return
        if log_user==None:
            embed=discord.Embed(title="Member Not Found",description="The member id is wrong",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
            embed.set_footer(text="Paradise Bot")
            await ctx.channel.send(embed=embed,delete_after=5)
            return
        prepare=f'''SELECT * FROM PunishmentLogs WHERE `User_id`='{log_id}'
        ORDER BY case_id DESC'''
        Cursor.execute(prepare)
        cases=Cursor.fetchall()
        print(cases)
        if len(cases)<1:
            await channel.send("The Person has no punishment in logs")
            return
        pages:list=[]
        page_carry:list=[]
        for item in enumerate(cases):
            count=item[0]
            count=int(count)
            page_carry.append(count)
            if count%10==9%10:
                pages.append(page_carry)
                page_carry=['class helper']
                page_carry.clear()
        if len(page_carry)>0:
            pages.append(page_carry)
        print (page_carry)
        print ("\n",pages)
        print ("\n \n")
        try:
            page=pages[page_no]
        except IndexError:
            page=pages[0]
        embed=discord.Embed(title=f"{log_user} ({int(log_id)})",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
        embed.set_footer(text="Paradise Bot")
        embed.set_thumbnail(url=log_user.avatar_url)
        for page_number in page:
            page_number=int(page_number)
            case=cases[page_number]
            embed.add_field(name=f"Case #{case[6]} - {case[4]}", value=case[2], inline=False)
        await ctx.channel.send(embed=embed)
async def sec_to_time(sec):
    sec=int(sec)
    day = sec // (24 * 3600)
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    minutes = sec // 60
    sec %= 60
    seconds = sec
    time_human:str=""
    if day>0:
        time_human=time_human+f"{day} days"
    if hour>0:
        time_human=time_human+f"{hour} hours"
    if minutes>0:
        time_human=time_human+f"{minutes} mins"
    if seconds>0:
        time_human=time_human+f"{seconds} seconds"
    return time_human


async def case(ctx):
    member=ctx.author
    channel=ctx.channel
    content=ctx.content
    try:
        await ctx.delete()
    except discord.errors.NotFound:
        print ("not found")
    if member.guild_permissions.kick_members:
        content_split=await split(content,2)
        item_id=content_split[1]
        item_id=await get_digit(item_id)
        try:
            item_id=int(item_id)
        except:
            channel.send("Invalid item id")
            return
        prepare=f'''Select * From PunishmentLogs WHERE `case_id`='{item_id}' '''
        Cursor.execute(prepare)
        Case=Cursor.fetchall()
        try:
            Case=Case[0]
        except IndexError:
            await channel.send("No such case found!")
            return
        log_user=await bot.fetch_user(int(Case[3]))
        print ("log user-: ",log_user,"\nId: ",int(Case[3]))
        offender=await bot.fetch_user(int(Case[0]))
        print ("Offender user-: ",offender,"\nId: ",int(Case[0]))
        duration=Case[1]
        duration = await sec_to_time(int(duration))
        if duration=="":
            duration="Doesn't Apply to bans and warns"
        embed=discord.Embed(title=f"{offender} ({int(Case[3])})",timestamp=Case[5],color=16711680,description=f"**Moderator: **{log_user}\n**Action: **{Case[4]}\n**Duration: **{duration}\n**Reason: **{Case[2]}")
        embed.set_footer(text=f"Paradise Bot  - Case #{Case[6]}")
        embed.set_thumbnail(url=offender.avatar_url)
        await channel.send(embed=embed)
            
async def remove_case(ctx):
    member=ctx.author
    channel=ctx.channel
    content=ctx.content
    try:
        await ctx.delete()
    except discord.errors.NotFound:
        print ("not found")
    if member.guild_permissions.kick_members:
        content_split=await split(content,2)
        item_id=content_split[1]
        item_id=await get_digit(item_id)
        try:
            item_id=int(item_id)
        except:
            channel.send("Invalid item id")
            return
        prepare=f'''Select * From PunishmentLogs WHERE `case_id`='{item_id}' '''
        Cursor.execute(prepare)
        Case=Cursor.fetchall()
        try:
            Case=Case[0]
        except IndexError:
            await channel.send("No such case found!")
            return
        prepare=f'''DELETE FROM PunishmentLogs WHERE `case_id`='{item_id}' '''
        Cursor.execute(prepare)
        embed=discord.Embed(title=f"Case - #{int(Case[6])}",description=f"Case#{int(Case[6])} has been sucessfully deleted!",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
        embed.set_footer(text=f"Paradise Bot  - Case #{Case[6]}",icon_url=member.avatar_url)
        await channel.send(embed=embed)


async def change_reason(ctx):
    member=ctx.author
    channel=ctx.channel
    content=ctx.content
    try:
        await ctx.delete()
    except discord.errors.NotFound:
        print ("not found")
    if member.guild_permissions.kick_members:
        content_split=await split(content,2)
        item_id=content_split[1]
        item_id=await get_digit(item_id)
        try:
            item_id=int(item_id)
        except:
            channel.send("Invalid item id")
            return
        prepare=f'''Select * From PunishmentLogs WHERE `case_id`='{item_id}' '''
        Cursor.execute(prepare)
        Case=Cursor.fetchall()
        try:
            Case=Case[0]
        except IndexError:
            await channel.send("No such case found!")
            return
        try:
            reason=content_split[2]
        except IndexError:
            await channel.send("Please enter a valid reason to add")
            return
        if reason=='':
            await channel.send("Please enter a valid reason to add")
            return
        prepare=f'''DELETE FROM PunishmentLogs WHERE `case_id`='{item_id}' '''
        Cursor.execute(prepare)
        prepare=f'''INSERT INTO PunishmentLogs (`User_id`,`Duration`,`reason`,`Mod`,`action`,`time`,`case_id`)
            VALUES ('{Case[0]}','{Case[1]}','{reason}','{Case[3]}','{Case[4]}','{Case[5]}','{Case[6]}')'''
        await channel.send(prepare)
        Cursor.execute(prepare)
        embed=discord.Embed(title=f"Case - #{int(Case[6])}",description=f"**Case #{int(Case[6])}** Reason has been sucessfully updated!\n**Old reason: **{Case[2]}\n**New reason: **{reason}",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
        embed.set_footer(text=f"Paradise Bot  - Case #{Case[6]}",icon_url=member.avatar_url)
        await channel.send(embed=embed)


async def warn(ctx):
    try:
        await ctx.delete()
    except discord.NotFound:
        print ("ctx not found D:")
    content=ctx.content
    member=ctx.author
    channel=ctx.channel
    print (member.id,type(member.id))
    if member.guild_permissions.manage_messages:
           print ("has perms")
           content_split=await split(content,2)
           warned_id=await get_digit(content_split[1])
           warned_id=int(warned_id)
           try:
               warned=await bot.fetch_user(warned_id)
           except discord.errors.NotFound:
               embed=discord.Embed(title="Member Not Found",description="either the member id is wrong or the member is not in this server",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
               embed.set_footer(text="Paradise Bot")
               await ctx.channel.send(embed=embed,delete_after=5)
               return
           print ("this is to be banned: ",warned_id,warned,ctx.guild)
           if warned==None:
               embed=discord.Embed(title="Member Not Found",description="You need to include the Member after p!warn!",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
               embed.set_footer(text="Paradise Bot")
               await ctx.channel.send(embed=embed,delete_after=5)
           else:
               try:
                   reason=content_split[2]
               except IndexError:
                   def check(ctx):
                       print("checking for reason")
                       return ctx.channel == channel and ctx.author == member #and ctx.content.startswith()!="p!say"

                   try:
                       embed=discord.Embed(title="Warning member",description=f"Why do you want to warn <@{warned_id}>",color=16711680,timestamp=datetime.datetime.now(datetime.timezone.utc))
                       embed.set_footer(text="Paradise Bot")
                       await ctx.channel.send(embed=embed,delete_after=15)
                       print("checking for reason")
                       reason = await bot.wait_for('message', timeout=15.0, check=check)
                       reason=reason.content
                       print (reason)
                   except asyncio.TimeoutError:
                       await ctx.channel.send("Oh Well, I did not get the reason in time, too bad i can't warn without reason :(",delete_after=5)
                       return
               prepare=f'''SELECT MAX(`case_id`) FROM PunishmentLogs'''
               Cursor.execute(prepare)
               case_id=Cursor.fetchall()
               print("Heres the case_id: ",case_id)
               case_id=(case_id[0][0])
               try:
                   case_id=int(case_id)
               except:
                   case_id=0
               else:
                   case_id+=1
               time_now=datetime.datetime.now(datetime.timezone.utc)
               time_now=await unaware_timezone(time_now)
               
               embed=discord.Embed(title=f"Case #{case_id} has been registered!",color=16711680,description=f"**Moderator: **<@{int(member.id)}>\n**Action: **Warn\n**Reason: **{reason}",timestamp=datetime.datetime.now(datetime.timezone.utc))
               dm=await warned.create_dm()
               await dm.send(f"You have been warned in Paradise network by <@{member.id}>\nReason of warn: {reason}")
               embed.set_footer(text="Paradise Bot")
               embed.set_thumbnail(url=warned.avatar_url)
               await ctx.channel.send(embed=embed)
               prepare=f'''INSERT INTO PunishmentLogs (`User_id`,`Duration`,`reason`,`Mod`,`action`,`time`,`case_id`)
               VALUES ('{warned_id}','0','{reason}','{str(member.id)}','warn','{time_now}','{case_id}')'''
               await ctx.channel.send(prepare)
               Cursor.execute(prepare)
    else:
        await channel.send("You do you not have the perms to do this",delete_after=5)

async def temp_service_ban(ctx):
    member=ctx.author
    channel=ctx.channel
    content=ctx.content
    try:
        await ctx.delete()
    except discord.errors.NotFound:
        print ("not found")
    if member.guild_permissions.mute_members:
        content_split=await split(content,2)
        print (content_split)
        banned_id=content_split[1]
        banned_id=await get_digit(banned_id)
        banned_id=int(banned_id)
        print ('banned-id: ',banned_id)
        try:
           banned=await ctx.guild.fetch_member(banned_id)
        except discord.errors.NotFound:
           embed=discord.Embed(title="Member Not Found",description="either the member id is wrong or the member is not in this server",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
           embed.set_footer(text="Paradise Bot")
           await ctx.channel.send(embed=embed,delete_after=5)
           print ('muted-id: ',banned_id)
           return
        if banned==None:
           print (banned_id,banned)
           embed=discord.Embed(title="Member Not Found",description="either the member id is wrong or the member is not in this server",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
           embed.set_footer(text="Paradise Bot")
           await ctx.channel.send(embed=embed,delete_after=5)
           return
        possible_time=await split(content_split[2],9999)
        print (possible_time)
        #del possible_time(5)
        sec=await convert_possible_time_to_sec(possible_time)
        print ("sec was: ",sec)
        reason_worded=possible_time[sec[1]:]
        reason = ' '.join([str(elem) for elem in reason_worded])
        sec_human=possible_time[0:sec[1]]
        sec:str = sec[0]
        if str(sec)=="0":
            await ctx.channel.send(embed=Invalid_Time)
            return
        sec_human = ' '.join([str(elem) for elem in sec_human])
        if reason=="":
            def check(ctx):
                       print("checking for reason")
                       return ctx.channel == channel and ctx.author == member
            try:
                embed=discord.Embed(title="Service Banning member",description=f"Why do you want to service Ban <@{banned_id}> for {sec_human}",color=16711680,timestamp=datetime.datetime.now(datetime.timezone.utc))
                embed.set_footer(text="Paradise Bot")
                await ctx.channel.send(embed=embed,delete_after=15)
                print("checking for reason")
                reason = await bot.wait_for('message', timeout=15.0, check=check)
                reason=reason.content
                print (reason)
            except asyncio.TimeoutError:
                await ctx.channel.send("Oh Well, I did not get the reason in time, too bad i can't service ban without reason :(",delete_after=5)
        await ctx.channel.send(f"Heres the time in calc in (sec): {sec} \n Reason: {reason}")
        done:bool=False
        while done==False:
            try:
                Cursor.execute("SELECT User_id FROM Transactions WHERE Transaction='unbanservice'")
            except mysql.connector.errors.DatabaseError:
                await asyncio.sleep(2)
                Cursor.execute("SELECT User_id FROM Transactions WHERE Transaction='unbanservice'")
                done=True
            else:
                done=True
        members_on_cooldown = Cursor.fetchall()
        print (members_on_cooldown)
        members_on_cooldown=await read_member_id(members_on_cooldown)
        if str(banned_id) in members_on_cooldown:
            print ("hes on cooldown")
            Cursor.execute(f"""SELECT * FROM Transactions 
            WHERE User_id='{str(banned_id)}'
            AND Transaction= 'unbanservice'""")
            cooldown_info = Cursor.fetchall()
            cooldown_info=cooldown_info[0]
            print (cooldown_info)
            duration=cooldown_info[1]
            print("cooldown value: ", duration)
            duration = str(duration)
            reason=str(cooldown_info[2])
            await channel.send(f"That Person is muted until {duration} UTC \n Reason: {reason}", delete_after=10)
            return
        else:
            role_add = discord.utils.get(ctx.guild.roles, name="Service Blacklisted")
            role_remove = discord.utils.get(ctx.guild.roles, name="Can see services")
            if role_add in banned.roles:
                await ctx.channel.send("That person is already muted, someone other bot/ admin have muted them.")
                return
            await banned.add_roles(role_add)
            await banned.remove_roles(role_remove)
            time_in_future=await time_future(sec)
            prepare=f'''INSERT INTO Transactions (User_id,Duration,reason,Transaction,`Mod`)
            VALUES ('{banned_id}','{await unaware_timezone(time_in_future)}','{reason}','unbanservice','{str(member.id)}')'''
            #await ctx.channel.send(prepare)     
            Cursor.execute(prepare)
            time_now=datetime.datetime.now(datetime.timezone.utc)
            time_now=await unaware_timezone(time_now)
            prepare=f'''SELECT MAX(`case_id`) FROM PunishmentLogs'''
            Cursor.execute(prepare)
            case_id=Cursor.fetchall()
            print("Heres the case_id: ",case_id)
            case_id=(case_id[0][0])
            try:
                case_id=int(case_id)
            except:
                case_id=0
            else:
                case_id+=1
            prepare=f'''INSERT INTO PunishmentLogs (`User_id`,`Duration`,`reason`,`Mod`,`action`,`time`,`case_id`)
            VALUES ('{banned_id}','{sec}','{reason}','{str(member.id)}','service-ban','{time_now}','{case_id}')'''
            duration=sec
            duration = await sec_to_time(int(duration))
            if duration=="":
                duration="Doesn't Apply to bans and warns"
            embed=discord.Embed(title=f"Case #{case_id} has been registered!",color=16711680,description=f"**Moderator: **<@{int(member.id)}>\n**Service Ban: **Warn\n**Duration :**{duration}\n**Reason: **{reason}",timestamp=datetime.datetime.now(datetime.timezone.utc))
            dm=await banned.create_dm()
            await dm.send(f"You have been service banned in Paradise network by <@{member.id}>\nReason of warn: {reason}\nDuration: {duration}")
            embed.set_footer(text="Paradise Bot")
            embed.set_thumbnail(url=banned.avatar_url)
            await ctx.channel.send(embed=embed)
            await ctx.channel.send(prepare)
            Cursor.execute(prepare)
    else:
        await channel.send("You do you not have the perms to do this",delete_after=5)


async def check_url(content):
    urls = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+',content.replace(",", ".").replace(" .", ".").lower())
    print(urls)
    for x in urls:
        if any(ele in x.upper().replace("\n", "").replace("-", "").replace(" ", "").replace(".", "").replace('"',"").replace(",", "").replace("REGIONAL_INDICATOR_", "").replace(":", "").replace("/", "").replace("_", "").replace("*", "").replace("HIIPS", "").replace("HIIP", "").replace("WWW", "") for ele in ipgrab):
            return True
        else:
            return False
async def check_blocked_word(content):
    if any(ele in content.upper().replace("\n", "").replace("t", "i").replace("-", "").replace(" ", "").replace(".", "").replace('"', "").replace(",", "").replace("REGIONAL_INDICATOR_", "").replace(":", "").replace("_","").replace("*", "") for ele in blocked_word) == True:
        return True
    else:
        return False
async def get_digit(input):
    to_be_return:str=""
    for i in input:
        i=str(i)
        if i in "1234567890":
            to_be_return=to_be_return+i
    return to_be_return

async def log(text):
    print("getting log channel")
    devlog = bot.get_channel(int("683331960705515570"))
    print("sending logs")
    await devlog.send(text)
    print("log sent")

async def staff_ping_check(ctx):
    channel = ctx.channel
    channel = ctx.channel
    member = ctx.author
    print ("checking for staff pings in msg")
    if "<@&714456813612826675>" in ctx.content:
        print ("Omg let me ping all staff members")
        embed = discord.Embed(title="Emergency Ping", description="Are you sure you want to ping ALL staff members?",color=0x76bb40,timestamp=datetime.datetime.now(datetime.timezone.utc))
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
            print ("discord.errors.Notfound")

    if "<@&714457002411294760>" in ctx.content:
        embed = discord.Embed(title="Emergency Ping",
                              description="Are you sure you want to ping COUNCIL staff members?", color=0x76bb40,timestamp=datetime.datetime.now(datetime.timezone.utc))
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
            print ("discord.errors.Notfound")

@bot.event
async def on_message(ctx):
    member = ctx.author
    content = ctx.content
    if ctx.author.bot == True:
        return
    print ("author: ",ctx.author)
    print ("content: ",ctx.content)
    split_content=content.split(None, 1)
    if await check_url(content)==True:
        await ctx.delete()
        await ctx.channel.send(
            member.mention + "\n\n**[8] Respect Privacy** - <#683331763090620427>\n\nIP Grabbers, malicious or not are not allowed in Paradise Network. **Attempts to bypass this filter will result in a permanent ban.**")
        return
    if await check_blocked_word(content)==True:
        try:
            await ctx.delete()
        except: discord.NotFound
        await member.send('Please refrain from using derogartory language in your messages. Attempts to circumvent this filter will result in severe punishment!')
        await log('Bad language was detected in ' + member.name + '\'s edited message, message has been deleted and PM has been sent.')
    if any(ele in content for ele in secretcode) == True:
        await ctx.delete(delay=10)
    await staff_ping_check(ctx)
    if content.startswith('p!')==True:
        commands={"p!ban":ban,
        "p!tempban":TempBan,
        "p!start-transactionmanager":start_transactionmanager,
        "p!forceupdate-transaction":transactionmanager_forceupdate,
        "p!tempmute":Tempmute,
        "p!punishments":logs_user,
        "p!case":case,
        "p!removecase":remove_case,
        "p!reason":change_reason,
        "p!warn":warn,
        "p!serviceban":temp_service_ban
        }
        content_str=str(split_content[0])

        print ("the command i found:",commands.get(content_str))
        if commands.get(content_str)!=None:
            await commands[content_str](ctx)
        else:
            await ctx.channel.send(f"Unknown Command `{content_str}`")


@bot.event
async def on_ready():
    print("ready")
    await transactionmanager()      

@bot.event
async def on_message_edit(before, after):
    if after.author.bot == True:
        return
    print (after)
    member=after.author
    content=after.content
    print (member)
    print (content)
    if await check_url(content) == True:
        await after.delete()
        await after.channel.send(
            member.mention + "\n\n**[8] Respect Privacy** - <#683331763090620427>\n\nIP Grabbers, malicious or not are not allowed in Paradise Network. **Attempts to bypass this filter will result in a permanent ban.**")
        return
    if await check_blocked_word(content)==True:
        await after.delete()
        await after.author.send('Please refrain from using derogartory language in your messages. Attempts to circumvent this filter will result in severe punishment!')
        await log('Bad language was detected in ' + after.author.name + '\'s edited message, message has been deleted and PM has been sent.')
    if any(ele in after.content for ele in secretcode) == True:
        await after.delete(delay=10)

async def BadName(member, message):
    name = str(member.name).upper()
    if await check_blocked_word(name)==True:
        await member.edit(nick=member.name)
        await message.delete()
        try:
            await member.send("We have removed your nickname in Paradise Network as your name was offensive. Attempts to bypass this system will result in severe punishment!")
        except discord.HTTPException:
            return

print ("TOKEN IS: ",TOKEN)
bot.run(TOKEN)