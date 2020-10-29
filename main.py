import asyncio
import discord
from discord.ext import commands
#from discord.utils import get
import pickle
#import pandas as pd
import datetime
import re
from threading import Thread
import time
import json
from discord.utils import get

ipgrab = ["GRABIFYLINK", "LEANCODINGCO", "SIOPIFY", "FREEGIFICARDSCO", "CURIOUSCAICLUB", "CAISNIHINGSFUN", "JOINMYSIIE",
          "CAISNIHINGSCOM", "IPLOGGERORG", "BLASZECOM", "WEBRESOLVERNL", "CURLV", "SHORIESI", "BIIURLIO", "RURLCO",
          "IPLOGGERCOM", "IPLOGGERRU", "2NOCO", "YIPSU"]
blocked_word = ['NIGGA', 'NIGGER', "NIGG", "REGIN", "IMAGPX", "REGGIN", "FAGGOT", "RETARD"]
secretcode = ['p!autodelete']

path_event_cooldown="event-ping-cooldown.txt"
path_specialist_cooldown="specialist-ping-cooldown.txt"
path_youtube_cooldown="youtube-ping-cooldown.txt"
#event_ping_cooldown:list=['640773439115886642,9']
#specialist_ping_cooldown:list=['640773439115886642,9']
#youtube_ping_cooldown:list=['640773439115886642,9']
#cooldowns={'event:':event_ping_cooldown,'specialist':specialist_ping_cooldown,'youtube:':youtube_ping_cooldown}
#with open('cooldowns.json', 'w') as f:
#  json.dump(cooldowns, f)

with open('cooldowns.json', 'rb') as f:
    cooldowns = json.load(f)
    print ("cooldowns: ",cooldowns)
event_ping_cooldown=cooldowns['event:']
specialist_ping_cooldown=cooldowns['specialist']
youtube_ping_cooldown=cooldowns['youtube:']

def pass_cooldown(item:list,cool,path_info):
    member_id=str(item[0:18])
    cooldown=int(str(item[19:]))
    print (member_id)
    print (cooldown)
    while cooldown > 0:
        print("inside the while")
        to_be_append = str(str(member_id) + ',' + str(cooldown))
        to_be_append = str(to_be_append)
        print(to_be_append)
        print("added/updated the cooldown")
        print(cool)
        cooldowns = {'event:': event_ping_cooldown,'specialist': specialist_ping_cooldown,'youtube:': youtube_ping_cooldown}
        with open('cooldowns.json', 'w') as f:
            print("opened file path")
            json.dump(cooldowns, f)
        print("path is:", cool)
        print(event_ping_cooldown)
        print("saved to database")
        time.sleep(10)  # 1 hour long sleep
        cool.remove(to_be_append)
        cooldown -= 1
        to_be_append = str(str(member_id) + ',' + str(cooldown))
        to_be_append = str(to_be_append)
        cool.append(to_be_append)
    cool.remove(to_be_append)
    with open(path_info, 'wb') as f:
        print("opened file path")
        pickle.dump(cool, f)
    print("cooldown over: ", cool)
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

for i in event_ping_cooldown:
    Thread(target=pass_cooldown, args=[i, event_ping_cooldown, path_event_cooldown]).start()
    print(i)
#def pass_specialist_cooldown():
for i in specialist_ping_cooldown:
    Thread(target=pass_cooldown, args=[i, specialist_ping_cooldown, path_specialist_cooldown]).start()
    print(i)
for i in youtube_ping_cooldown:
    Thread(target=pass_cooldown, args=[i, youtube_ping_cooldown, path_youtube_cooldown]).start()
    print(i)
#Thread(target =pass_event_cooldown).start()
#Thread(target =pass_specialist_cooldown).start()
print ("started cooldowns")

#staff_roles=['Owner','Ripanovia','Admin','Developer','Sr. Mod','Partnership Coordinator','Staff Council ⚒️','Mod','Helper']
#bot = commands.Bot(command_prefix='?')
bot=discord.Client()
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
        return "none"


async def get_digit(input):
    to_be_return:str=""
    for i in input:
        i=str(i)
        if i in "1234567890":
            to_be_return=to_be_return+i
    return to_be_return


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
async def on_raw_reaction_add(payload):
    emoji = str(payload.emoji)
    if payload.event_type == 'REACTION_ADD':
        member = bot.get_user(payload.user_id)
        if member == None:
            return
        if member.bot == True:
            return
        try:
            message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        except discord.errors.NotFound:
            return
    else:
        return
    print ("let me check")
    if (emoji == "❎") and (len(message.mentions) == 1) and ("EMERGENCY PING" in message.content) and (
            message.author.id == bot.user.id) and (member == message.mentions[0] or message.guild.get_role(bot.user.id) in message.guild.get_member(member.id).roles):
        await message.delete()
        return

    if (emoji == "✅") and (len(message.mentions) == 1) and ("STAFF EMERGENCY PING" in message.content) and (
            message.author.id == bot.user.id) and (member == message.mentions[0]):
        await message.channel.send("<@&757747024060743691>" + " ALL STAFF PING REQUESTED BY " + member.mention)
        await message.delete()
        return

    if (emoji == "✅") and (len(message.mentions) == 1) and ("COUNCIL EMERGENCY PING" in message.content) and (
            message.author.id == bot.user.id) and (member == message.mentions[0]):
        await message.channel.send("<@&757747024060743691>" + " COUNCIL PING REQUESTED BY " + member.mention)
        await message.delete()
        return


async def temp(ctx):
    member=ctx.author
    channel=ctx.channel
    if member.guild_permissions.manage_messages:
        print ("has perms")
        try:
            print(ctx.content.split(None, 1)[1])
        except IndexError:
            await ctx.channel.send('The syntax is wrong, you are missing an arguement \n The correct syntax is `p!clear [number]`',delete_after=5)
            return
        if ctx.content.split(None, 1)[1].isdigit() == True:
            number = ctx.content.split(None, 1)[1]
        else:
            await channel.send('The syntax is wrong, you are missing an arguement \n The correct syntax is `p!clear [number]`',delete_after=5)
            return
        print ("making embed")
        embed = discord.Embed(title=f'Are you sure you want to clear {number} messages?',description="Please do `p!confirm` to confirm this action.", color=0xe22400,timestamp=datetime.datetime.now(datetime.timezone.utc))
        print ("setting footer")
        embed.set_footer(text="Paradise Bot")
        print ("sending embed")
        clear = await channel.send(content=member.mention, delete_after=20, embed=embed)
        print ("embed sent")
        def check(ctx):
            print ("checking for p!confirm def")
            return ctx.content == 'p!confirm' and ctx.channel == channel and ctx.author == member
        try:
            print ("checking for p!confirm")
            msg = await bot.wait_for('message', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            print ("timeout")
            await clear.edit(content='I did not receive confirmation in time. Oh well.')
            await asyncio.sleep(5)
            await clear.delete()
        else:
            await channel.purge(limit=int(number) + int('3'))
            msg= await channel.send(f'Successfully deleted {number} messages!',delete_after=5)
            log_msg=f'{member} deleted {number} messages in <#{str(channel.id)}>'
            print (log_msg)
            await log(log_msg)
    else:
        await channel.send("You do you not have the perms to do this",delete_after=5)

async def youtube(ctx):
    print ("checking perms")
    await ctx.delete()

    if len(ctx.content)!=14:
        await ctx.channel.send('The syntax is wrong, you are missing an arguement \n The correct syntax is `p!youtube-ping`',delete_after=5)
        return
    member=ctx.author
    channel=ctx.channel
    youtuber_check=["Youtuber","Twitch Streamer"]
    has_perms: bool = False
    for role in youtuber_check:
        print ("inside the for loop to check for roles")
        role_check = discord.utils.get(ctx.guild.roles, name=role)
        print ("This is the role i found: ",role_check)
        if role_check in member.roles:
            has_perms = True
    if has_perms == False:
        await channel.send("You do you not have the perms to do this")
        return
    if has_perms == True:
        member_id=member.id
        member_id=str(member_id)
        on_cooldown:bool=False
        for a in enumerate(youtube_ping_cooldown):
            print("a: ", a)
            i = a[1]
            print("i: ", i)
            print(i[0:18])
            if str(i[0:18]) == member_id:
                on_cooldown = True
                cooldown_number = a[0]
        if on_cooldown == True:
            print("cooldown_number:", cooldown_number)
            cooldown_value = youtube_ping_cooldown[int(cooldown_number)]
            print("cooldown value: ", cooldown_value)
            cooldown_value = str(cooldown_value)
            cooldown_timer = cooldown_value[19:]
            print("cooldown timer: ", cooldown_timer)
            cooldown_timer = int(cooldown_timer)
            await channel.send(f"You are on cooldown for {cooldown_timer} hours", delete_after=10)
            return
        else:

            event_confirm_em = discord.Embed(title=f'Are you sure you want to ping?',description=f"Please do `p!confirm` to confirm that you want to ping <@&{760270486877241384}>", color=int('6579455'),timestamp=datetime.datetime.now(datetime.timezone.utc))
            event_confirm_em.set_footer(text="Paradise Bot")
            event_confirm = await channel.send(content=member.mention, delete_after=20, embed=event_confirm_em)
            def check(ctx):
                return ctx.content == 'p!confirm' and ctx.channel == channel and ctx.author == member
            try:
                msg = await bot.wait_for('message', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                await event_confirm.edit(content='I did not receive confirmation in time. Oh well.')
                await asyncio.sleep(5)
                await event_confirm.delete()
                return

            else:
                await msg.delete()
                await event_confirm.delete()
                await channel.send(f"<@&{759718231089872927}> You have been pinged by {member}")
                cooldown = 2
                cooldown = int(cooldown)
                print("starting cooldown counter")
                print (member.id)
                member_id=member.id
                member_id=str(member_id)
                while cooldown > 0:
                    print ("inside the while")
                    to_be_append=str(str(member_id)+','+str(cooldown))
                    to_be_append=str(to_be_append)
                    print (to_be_append)
                    youtube_ping_cooldown.append(to_be_append)
                    print ("added/updated the cooldown")
                    print (youtube_ping_cooldown)
                    cooldowns = {'event:': event_ping_cooldown, 'specialist': specialist_ping_cooldown,
                                 'youtube:': youtube_ping_cooldown}
                    with open('cooldowns.json', 'w') as f:
                        print("opened file path")
                        json.dump(cooldowns, f)
                    print("path is:",'cooldowns.json')
                    print(youtube_ping_cooldown)
                    print ("saved to database")
                    await asyncio.sleep(10)  # 1 hour long sleep
                    cooldown -= 1
                    youtube_ping_cooldown.remove(to_be_append)
                #event_ping_cooldown.remove(to_be_append)
                with open(path_youtube_cooldown, 'wb') as f:
                    print("opened file path")
                    pickle.dump(youtube_ping_cooldown, f)
                print ("cooldown over: ",youtube_ping_cooldown)

    else:
            event_manager_no=discord.Embed(title="You don't have the perms",description=f"You need the <@&{683868128664485889}> or <@&{679852120257855563}> role.",color=int('6579455'),timestamp=datetime.datetime.now(datetime.timezone.utc))
            await channel.send(content=f"Sorry <@{member.id}> but you can't", delete_after=15,embed=event_manager_no)





async def specialist(ctx):
    member=ctx.author
    channel=ctx.channel
    member_id=member.id
    member_id=str(member_id)
    await ctx.delete()
    if len(ctx.content)!=17:
        await ctx.channel.send('The syntax is wrong, you are missing an arguement \n The correct syntax is `p!ping-specialist`',delete_after=5)
        return
    on_cooldown:bool=False
    for a in enumerate(specialist_ping_cooldown):
        print ("a: ",a)
        i=a[1]
        print ("i: ",i)
        print (i[0:18])
        if str(i[0:18])==member_id:
            on_cooldown=True
            cooldown_number=a[0]
    if on_cooldown==True:
        print ("cooldown_number:",cooldown_number)
        cooldown_value=specialist_ping_cooldown[int(cooldown_number)]
        print ("cooldown value: ",cooldown_value)
        cooldown_value=str(cooldown_value)
        cooldown_timer=cooldown_value[19:]
        print ("cooldown timer: ",cooldown_timer)
        cooldown_timer=int(cooldown_timer)
        await channel.send(f"You are on cooldown for {cooldown_timer} hours",delete_after=10)
        return
    else:
        event_confirm_em = discord.Embed(title=f'Are you sure you want to ping?',description=f"Please do `p!confirm` to confirm that you want to ping <@&{705423459219537931}>", color=int('6579455'),timestamp=datetime.datetime.now(datetime.timezone.utc))
        event_confirm_em.set_footer(text="Paradise Bot")
        event_confirm = await channel.send(content=member.mention, delete_after=20, embed=event_confirm_em)
        def check(ctx):
            return ctx.content == 'p!confirm' and ctx.channel == channel and ctx.author == member
        try:
            msg = await bot.wait_for('message', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await event_confirm.edit(content='I did not receive confirmation in time. Oh well.',delete_after=5)
            return
        else:
            await event_confirm.delete()
            await msg.delete()
            await channel.send(f"<@&{759873679969484812}> You have been pinged by {member}")
            cooldown = 2
            cooldown = int(cooldown)
            print("starting cooldown counter")
            print (member.id)
            member_id=member.id
            member_id=str(member_id)
            while cooldown > 0:
                print ("inside the while")
                to_be_append=str(str(member_id)+','+str(cooldown))
                to_be_append=str(to_be_append)
                print (to_be_append)
                specialist_ping_cooldown.append(to_be_append)
                print ("added/updated the cooldown")
                print (specialist_ping_cooldown)
                cooldowns = {'event:': event_ping_cooldown, 'specialist': specialist_ping_cooldown,
                             'youtube:': youtube_ping_cooldown}
                with open('cooldowns.json', 'w') as f:
                    print("opened file path")
                    json.dump(cooldowns, f)
                print("path is:", 'cooldowns.json')
                print("path is:", path_specialist_cooldown)
                print(specialist_ping_cooldown)
                print ("saved to database")
                await asyncio.sleep(10)  # 1 hour long sleep
                cooldown -= 1
                specialist_ping_cooldown.remove(to_be_append)
            #event_ping_cooldown.remove(to_be_append)
            cooldowns = {'event:': event_ping_cooldown, 'specialist': specialist_ping_cooldown,
                         'youtube:': youtube_ping_cooldown}
            with open('cooldowns.json', 'w') as f:
                print("opened file path")
                json.dump(cooldowns, f)
            print ("cooldown over: ",specialist_ping_cooldown)


async def event(ctx):
    member=ctx.author
    channel=ctx.channel
    await ctx.delete()
    if len(ctx.content) != 12:
        await ctx.channel.send('The syntax is wrong, you are missing an arguement \n The correct syntax is `p!event-ping`',
            delete_after=5)
        return
    event_manager="Event Manager"
    role_check = discord.utils.get(ctx.guild.roles, name=event_manager)
    member_id=member.id
    member_id=str(member_id)
    on_cooldown:bool=False
    if role_check in member.roles:
        for a in enumerate(event_ping_cooldown):
            print("a: ", a)
            i = a[1]
            print("i: ", i)
            print(i[0:18])
            if str(i[0:18]) == member_id:
                on_cooldown = True
                cooldown_number = a[0]
        if on_cooldown == True:
            print("cooldown_number:", cooldown_number)
            cooldown_value = event_ping_cooldown[int(cooldown_number)]
            print("cooldown value: ", cooldown_value)
            cooldown_value = str(cooldown_value)
            cooldown_timer = cooldown_value[19:]
            print("cooldown timer: ", cooldown_timer)
            cooldown_timer = int(cooldown_timer)
            await channel.send(f"You are on cooldown for {cooldown_timer} hours", delete_after=10)
            return
        else:

            event_confirm_em = discord.Embed(title=f'Are you sure you want to ping?',description=f"Please do `p!confirm` to confirm that you want to ping <@&{735961962034364434}>", color=int('6579455'),timestamp=datetime.datetime.now(datetime.timezone.utc))
            event_confirm_em.set_footer(text="Paradise Bot")
            event_confirm = await channel.send(content=member.mention, delete_after=20, embed=event_confirm_em)
            def check(ctx):
                return ctx.content == 'p!confirm' and ctx.channel == channel and ctx.author == member
            try:
                msg = await bot.wait_for('message', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                await event_confirm.edit(content='I did not receive confirmation in time. Oh well.',delete_after=5)
                return
            else:
                await msg.delete()
                await event_confirm.delete()
                await channel.send(f"<@&{761970867210289184}> You have been pinged by {member}")
                cooldown = 2
                cooldown = int(cooldown)
                print("starting cooldown counter")
                print (member.id)
                member_id=member.id
                member_id=str(member_id)
                while cooldown > 0:
                    print ("inside the while")
                    to_be_append=str(str(member_id)+','+str(cooldown))
                    to_be_append=str(to_be_append)
                    print (to_be_append)
                    event_ping_cooldown.append(to_be_append)
                    print ("added/updated the cooldown")
                    print (event_ping_cooldown)
                    cooldowns = {'event:': event_ping_cooldown, 'specialist': specialist_ping_cooldown,
                                 'youtube:': youtube_ping_cooldown}
                    with open('cooldowns.json', 'w') as f:
                        print("opened file path")
                        json.dump(cooldowns, f)
                    print("path is:", 'cooldowns.json')
                    print("path is:", path_event_cooldown)
                    print(event_ping_cooldown)
                    print ("saved to database")
                    await asyncio.sleep(10)  # 1 hour long sleep
                    cooldown -= 1
                    event_ping_cooldown.remove(to_be_append)
                #event_ping_cooldown.remove(to_be_append)
                cooldowns = {'event:': event_ping_cooldown, 'specialist': specialist_ping_cooldown,
                             'youtube:': youtube_ping_cooldown}
                with open('cooldowns.json', 'w') as f:
                    print("opened file path")
                    json.dump(cooldowns, f)
                print ("cooldown over: ",event_ping_cooldown)

    else:
            event_manager_no=discord.Embed(title="You can't",description=f"You don't have the <@&{735958571052826656}> role.",color=int('6579455'),timestamp=datetime.datetime.now(datetime.timezone.utc))
            await channel.send(content=f"Sorry <@{member.id}> but you can't", delete_after=15,embed=event_manager_no)
async def say(ctx):
    try:
        await ctx.delete()
    except discord.NotFound:
        print ("ctx not found D:")
    content=ctx.content
    member=ctx.author
    channel=ctx.channel
    if member.guild_permissions.administrator:
           print ("has perms")
           content_split=await split(content,2)
           if content_split=="none":
               embed=discord.Embed(title="Channel Not Found",description="You need to include the channel after p!say!",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
               embed.set_footer(text="Paradise Bot")
               await ctx.channel.send(embed=embed,delete_after=5)
               return
           channel_id=await get_digit(content_split[1])
           channel_id=int(channel_id)
           channel=bot.get_channel(channel_id)
           if channel==None:
               embed=discord.Embed(title="Channel Not Found",description="You need to include the channel after p!say!",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
               embed.set_footer(text="Paradise Bot")
               await ctx.channel.send(embed=embed,delete_after=5)
           else:
               try:
                   text=content_split[2]
               except IndexError:
                   def check(ctx):
                       print("checking for text")
                       return ctx.channel == channel and ctx.author == member #and ctx.content.startswith()!="p!say"

                   try:
                       embed=discord.Embed(title="Sending Message",description=f"What do you want me to say in <#{channel_id}>?",color=16711680,timestamp=datetime.datetime.now(datetime.timezone.utc))
                       embed.set_footer(text="Paradise Bot")
                       await ctx.channel.send(embed=embed,delete_after=15)
                       print("checking for p!confirm")
                       msg = await bot.wait_for('message', timeout=15.0, check=check)
                       print (msg)
                   except asyncio.TimeoutError:
                       await ctx.channel.send("Oh Well, I did not get the message in time, too bad :(",delete_after=5)
                   else:
                       await channel.send(msg.content)
               else:
                await channel.send(text)
    else:
        await channel.send("You do you not have the perms to do this",delete_after=5)


async def edit(ctx):
    try:
        await ctx.delete()
    except discord.NotFound:
        print ("ctx not found D:")
    content=ctx.content
    member=ctx.author
    channel=ctx.channel

    if member.guild_permissions.administrator:
           print ("has perms")
           content_split=await split(content,2)
           if content_split=="none":
               embed=discord.Embed(title="Message Id Not Found",description="You need to include the Message Id after p!edit!",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
               embed.set_footer(text="Paradise Bot")
               await ctx.channel.send(embed=embed,delete_after=5)
               return
           print ("split content: ",content_split)
           msg_id = await get_digit(content_split[1])
           print("msg_id: ",msg_id)
           msg_id = int(msg_id)
           if msg_id==None:
               embed=discord.Embed(title="Message Id Not Found",description="You need to include the Message Id after p!edit!",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
               embed.set_footer(text="Paradise Bot")
               await ctx.channel.send(embed=embed,delete_after=5)
           else:
               try:
                   msg_ctx = await ctx.channel.fetch_message(id=msg_id)
               except discord.NotFound:
                   embed = discord.Embed(title="Message Not Found",
                                         description="Either that message is not in this channel or it does not exist.",
                                         color=16711680, timestamp=datetime.datetime.now(datetime.timezone.utc))
                   embed.set_footer(text="Paradise Bot")
                   await ctx.channel.send(embed=embed, delete_after=10)
                   return
               if msg_ctx.author.id!=bot.user.id:
                   embed = discord.Embed(title="No Permissions", description="That message's not by me!",color=16711680,timestamp=datetime.datetime.now(datetime.timezone.utc))
                   embed.set_footer(text="Paradise Bot")
                   await ctx.channel.send(embed=embed,delete_after=5)
                   return
               else:
                    try:
                        text=content_split[2]
                    except IndexError:
                        def check(ctx):
                            print("checking for text")
                            return ctx.channel == channel and ctx.author == member #and ctx.content.startswith()!="p!say"
                        try:
                            embed=discord.Embed(title="Edit Message",description=f"What do you want me to say in that message ?",color=16711680,timestamp=datetime.datetime.now(datetime.timezone.utc))
                            embed.set_footer(text="Paradise Bot")
                            await ctx.channel.send(embed=embed,delete_after=15)
                            print("checking for p!confirm")
                            msg = await bot.wait_for('message', timeout=15.0, check=check)
                            print (msg)
                            text=msg.content
                            text=str(text)
                        except asyncio.TimeoutError:
                            await ctx.channel.send("Oh Well, I did not get the message in time, too bad :(",delete_after=5)
                            return
                        else:
                            msg_ctx = await ctx.channel.fetch_message(id=msg_id)

                    await msg_ctx.edit(content=text)
    else:
        await channel.send("You do you not have the perms to do this",delete_after=5)


async def react(ctx):
    channel=ctx.channel
    content=ctx.content
    member=ctx.author
    if member.guild_permissions.administrator:
           print ("has perms")
           content_split=await split(content,2)
           if content_split=="none":
               embed=discord.Embed(title="Message Id Not Found",description="You need to include the Message Id after p!react!",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
               embed.set_footer(text="Paradise Bot")
               await ctx.channel.send(embed=embed,delete_after=5)
               return
           print ("split content: ",content_split)
           msg_id = await get_digit(content_split[1])
           print("msg_id: ",msg_id)
           msg_id = int(msg_id)
           if msg_id==None:
               embed=discord.Embed(title="Message Id Not Found",description="You need to include the Message Id after p!edit!",timestamp=datetime.datetime.now(datetime.timezone.utc),color=16711680)
               embed.set_footer(text="Paradise Bot")
               await ctx.channel.send(embed=embed,delete_after=5)
           else:
               try:
                   msg_ctx = await ctx.channel.fetch_message(id=msg_id)
               except discord.NotFound:
                   embed = discord.Embed(title="Message Not Found",description="Either that message is not in this channel or it does not exist.",color=16711680, timestamp=datetime.datetime.now(datetime.timezone.utc))
                   embed.set_footer(text="Paradise Bot")
                   await ctx.channel.send(embed=embed, delete_after=10)
                   return
               else:
                   embed = discord.Embed(title="Message Reacting",
                                         description="React to this message with what you want to add to the message.",
                                         color=0xe22400)
                   embed.set_footer(text="Paradise Bot")
                   message = await ctx.channel.send(content=ctx.author.mention, embed=embed)
                   while True:
                       def check(reaction, user):
                           return reaction.message.id == message.id and user == ctx.author

                       try:
                           reaction, user = await bot.wait_for('reaction_add', timeout=15.0, check=check)
                       except asyncio.exceptions.TimeoutError:
                           await message.delete()
                           #await ctx.delete()
                           return
                       else:
                           await msg_ctx.add_reaction(reaction.emoji)


@bot.event
async def on_member_update(before,after):
    #print (after)
    nickname=str(after.nick)
    #print ("nickname: ",nickname)
    if any(ele in nickname.replace("\n", "").replace("t", "i").replace("-", "").replace(" ", "").replace(".", "").replace('"', "").replace(",", "").replace("REGIONAL_INDICATOR_", "").replace(":", "").replace("_","").replace("*", "") for ele in blocked_word) == True:
        await after.send('Please refrain from using derogartory language in your Nicknames. Attempts to circumvent this filter will result in severe punishment!')
        await log('Bad language was detected in ' + after.name + '\'s nickname, it has been deleted and PM has been sent.')
        await after.edit(nick=before.nick)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('The syntax is wrong, you are missing an arguement')

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
        commands={
            'p!clear':temp,
            'p!youtube-ping':youtube,
            'p!ping-specialist':specialist,
            'p!event-ping':event,
            'p!confirm':confirm,
            'p!say':say,
            'p!edit':edit,
            'p!react':react
        }
        content_str=str(split_content[0])

        print ("the command i found:",commands.get(content_str))
        if commands.get(content_str)!=None:
            await commands[content_str](ctx)
        else:
            await ctx.channel.send(f"Unknown Command `{content_str}`")
    #if ctx.content.startswith('p!clear'):
    #    await temp(ctx)
    #    return
    #if ctx.content.startswith('p!youtube-ping'):
    #    await youtube(ctx)
    #    return
    #if ctx.content.startswith('p!ping-specialist'):
    #    await specialist(ctx)
    #    return
    #if ctx.content.startswith('p!event-ping'):
    #    await event(ctx)
    #    return




    #await bot.process_commands(ctx)



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
        return
async def log(text):
    print("getting log channel")
    devlog = bot.get_channel(int("683331960705515570"))
    print("sending logs")
    await devlog.send(text)
    print("log sent")

async def confirm(ctx):
    channel=ctx.channel

@bot.event
async def on_ready():
    print ("ready")
    #guild=bot.get_guild(int("674474377286516736"))
    #print (guild)
    #channel=bot.get_channel(int("683331849195487232"))
    #await channel.send("<@649604306596528138> \n Roses are red, \n Voilets are blue \n If you say this shit again, \n I will ban you")
    #add_role = get(guild.roles, name="Hot Pink")
    #print (add_role)
    #user_id=bot.user.id
    #user=guild.get_member(user_id)
    #print (user,type(user))
    #await user.add_roles(add_role)
bot.run('NzYxOTcwNDc3NTMwNzQyNzg0.X3iWTg.ot6JKf2tUDKK7nNDHiTfSLoGskE')
#bot.run('Njc5NjQ3NzY2MjgwMDExODMz.Xk0ZTg.BAB6C81qczhqDJI28ytTME4qx0w')
#client.run('NzYxOTcwNDc3NTMwNzQyNzg0.X3iWTg.OzC7N5qC5jeH25mpz4XErcT5-CQ')
