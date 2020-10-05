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
ipgrab = ["GRABIFYLINK", "LEANCODINGCO", "SIOPIFY", "FREEGIFICARDSCO", "CURIOUSCAICLUB", "CAISNIHINGSFUN", "JOINMYSIIE",
          "CAISNIHINGSCOM", "IPLOGGERORG", "BLASZECOM", "WEBRESOLVERNL", "CURLV", "SHORIESI", "BIIURLIO", "RURLCO",
          "IPLOGGERCOM", "IPLOGGERRU", "2NOCO", "YIPSU","SKELDRBOI"]
blocked_word = ['NIGGA', 'NIGGER', "NIGG", "REGIN", "IMAGPX", "REGGIN", "FAGGOT", "RETARD", "CUNT","OOOL"]
secretcode = ['p!autodelete']
#url_short=["BITLY","REBRANDLY","TINYURL","YOURLSORG","GOOGL","ISGD","BITDO"]
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
#def pass_event_cooldown():
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

staff_roles=['Owner','Ripanovia','Admin','Developer','Sr. Mod','Partnership Coordinator','Staff Council ⚒️','Mod','Helper']
bot = commands.Bot(command_prefix='?')
@bot.command(name='clear',help='clears messages from a channel')
async def temp(ctx,number:int):
    member=ctx.author
    channel=ctx.channel
    has_perms:bool=False
    for role in staff_roles:
        role_check = discord.utils.get(ctx.guild.roles, name=role)
        if role_check in member.roles:
            has_perms=True
    if has_perms==False:
        await channel.send("You do you not have the perms to do this")
    if has_perms==True:
        print ("has perms")
        print ("making embed")
        embed = discord.Embed(title=f'Are you sure you want to clear {number} messages?',description="Please do `p!confirm` to confirm this action.", color=0xe22400,timestamp=datetime.datetime.now())
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
            log_msg=f'<@{member.id}> deleted {number} messages in <#{str(channel.id)}>'
            print (log_msg)
            await log(log_msg)

@bot.command(name='youtube-ping',help='pings the YouTube ping')
async def event(ctx):
    print ("checking perms")
    member=ctx.author
    channel=ctx.channel
    youtuber_check=["Youtuber","Twitch Streamer"]
    has_perms: bool = False
    for role in youtuber_check:
        print ("insise the for loop to check for roles")
        role_check = discord.utils.get(ctx.guild.roles, name=role)
        print ("This is the role i found: ",role_check)
        if role_check in member.roles:
            has_perms = True
    if has_perms == False:
        await channel.send("You do you not have the perms to do this")
    if has_perms == True:
        member_id=member.id
        member_id=str(member_id)
        on_cooldown:bool=False
        await ctx.message.delete()
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
        else:

            event_confirm_em = discord.Embed(title=f'Are you sure you want to ping?',description=f"Please do `p!confirm` to confirm that you want to ping <@&{760270486877241384}>", color=int('6579455'),timestamp=datetime.datetime.now())
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
            else:
                await msg.delete()
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
                    print("path is:", path_youtube_cooldown)
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
            event_manager_no=discord.Embed(title="You don't have the perms",description=f"You need the <@&{683868128664485889}> or <@&{679852120257855563}> role.",color=int('6579455'),timestamp=datetime.datetime.now())
            await channel.send(content=f"Sorry <@{member.id}> but you can't", delete_after=15,embed=event_manager_no)





@bot.command(name='ping-specialist',help='pings the available specialist ping (works only in tickets)')
async def specialist(ctx):
    member=ctx.author
    channel=ctx.channel
    member_id=member.id
    member_id=str(member_id)
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

    else:
        event_confirm_em = discord.Embed(title=f'Are you sure you want to ping?',description=f"Please do `p!confirm` to confirm that you want to ping <@&{705423459219537931}>", color=int('6579455'),timestamp=datetime.datetime.now())
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
        else:
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
                with open(path_specialist_cooldown, 'wb') as f:
                    print ("opened file path")
                    pickle.dump(specialist_ping_cooldown, f)
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


@bot.command(name='event-ping',help='pings the event ping')
async def event(ctx):
    member=ctx.author
    channel=ctx.channel
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
        else:

            event_confirm_em = discord.Embed(title=f'Are you sure you want to ping?',description=f"Please do `p!confirm` to confirm that you want to ping <@&{735961962034364434}>", color=int('6579455'),timestamp=datetime.datetime.now())
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
            else:
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
                    with open(path_event_cooldown, 'wb') as f:
                        print ("opened file path")
                        pickle.dump(event_ping_cooldown, f)
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
            event_manager_no=discord.Embed(title="You can't",description=f"You don't have the <@&{735958571052826656}> role.",color=int('6579455'),timestamp=datetime.datetime.now())
            await channel.send(content=f"Sorry <@{member.id}> but you can't", delete_after=15,embed=event_manager_no)






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




    await bot.process_commands(ctx)



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


bot.run('NzYxOTcwNDc3NTMwNzQyNzg0.X3iWTg.OzC7N5qC5jeH25mpz4XErcT5-CQ')
#client.run('NzYxOTcwNDc3NTMwNzQyNzg0.X3iWTg.OzC7N5qC5jeH25mpz4XErcT5-CQ')