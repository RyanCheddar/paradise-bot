import asyncio
import discord
from discord.ext import commands
#from dotenv import load_dotenv
from discord.utils import get
#load_dotenv()
import pickle
import pandas as pd
import datetime
from discord import Embed
#TOKEN = os.getenv('DISCORD_TOKEN')
#with open('err.txt', 'a') as f:
    #f.read()
    #print (f.read())
#client = discord.Client()
from datetime import timedelta
import re
import random
time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}
ticket_num:list=["0","0","0","0","0","0","0","0"]
def Color():
    print ("Color 1")
    r=random.randint(50,200)
    print ("Color 2")
    g=random.randint(50,200)
    print ("Color 3")
    b=random.randint(50,200)
    print ("Color 4")
    return (r << 16) + (g << 8) + b
def convert_time_to_seconds(time):
    for i in time:
        if i not in "1234567890smhdw":
            return "None"
    else:
        try:
            return int(time[:-1]) * time_convert[time[-1]]
        except:
            return time
#ban_list = pd.read_csv("Service ban list1.txt",index_col=0)
#ban_list = ban_list.to_dict("split")
#ban_list = dict(zip(ban_list["index"], ban_list["data"]))
#print (type(ban_list))
#ban_list={}
#ban_list=pd.read_csv(r"C:\Users\home\PycharmProjects\DiscordBot\Service ban list.txt")
def breaker(text):
    #text=text.upper()
    text=list(str(text))
    broke=[]
    for i in range(len(text)):
        broke.append(text[i])
    return broke

bot = commands.Bot(command_prefix='?')
Invalid_Time = discord.Embed(title="Invalid Time format",description="'s' for seconds\n'm' for minutes\n'h for hours'\n 'd' for days\n 'w' for weeks",color=0x00ff00)
Invalid_Time.add_field(name="Please use this format", value="This is not case sensitive",inline=False)

#print ("ready")
@bot.command(name='services-ban',help='test command')
async def temp(ctx, muted: discord.Member,sec,reason):
    ROLE_need = "BOTS"
    role_check = discord.utils.get(ctx.guild.roles, name=ROLE_need)
    member = ctx.author
    sec_og = sec
    sec=convert_time_to_seconds(sec)

    if role_check in member.roles:
        member = ctx.author
        ROLE_put = "Service Blacklisted"
        ROLE_remove="Can see services"
        role_put = get(member.guild.roles, name=ROLE_put)
        role_remove=get(member.guild.roles, name=ROLE_remove)
        role_checker = discord.utils.get(ctx.guild.roles, name=ROLE_put)
        print (member.roles)
        if role_checker in muted.roles:
            await ctx.send(f"{muted} is alr blacklisted bruh, let me unblacklist them")
            await muted.remove_roles(role_put)
            await muted.add_roles(role_remove)
        else:
            if sec == "None":
                await ctx.send(embed=Invalid_Time)
            else:
                await muted.add_roles(role_put)
                await muted.remove_roles(role_remove)
                await ctx.send(f'ok i service banned {muted} for {sec_og}.')
                print ("1")
                dm=await muted.create_dm()
                Service_block_dm = discord.Embed(title="Service Blocked",description=f"You have been service blocked for {sec_og} or {sec} seconds by {member}")
                Service_block_dm.add_field(name="Reason", value=reason, inline=False)
                await dm.send(embed=Service_block_dm)
                print ("2")
                await asyncio.sleep(sec-1)
                await muted.remove_roles(role_put)
                await muted.add_roles(role_remove)
    else:
        await ctx.send(f"Bruh you don't have the {ROLE_need} role_put. Get Gud Lol")
@bot.command(name='service-ban',help='it bans the person from using services')
@commands.has_role('Admin')
async def service_ban(ctx):
    ROLE="BOTS"
    member=ctx.author
    role_put=get(member.guild.roles,name=ROLE)
    print (member.roles)
    role_check = discord.utils.get(ctx.guild.roles, name=ROLE)
    if role_check in member.roles:
        await ctx.send("you are alr blacklisted bruh, let me unblacklist you")
        await member.remove_roles(role_put)
    else:
        await member.add_roles(role_put)
        await ctx.send("blacklisted you")
        print(f"{member} was given {role_put}")
@bot.command(name='e',help='it practically does absolutely nothing')
async def e(message):
    response = "E is bad"
    await message.send(response)
    print (type(message))
    print(message.author.id)
    print (message.guild.created_at)
@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(message, number_of_dice:int, number_of_sides:int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await message.send(', '.join(dice))


@bot.command(name='create-channel', help='Simulates rolling dice.')
@commands.has_role('Admin')
async def create_channel(ctx, channel_name="1"):
    guild = ctx.guild
    print(f'Creating a new channel: {channel_name}')
    print (type(channel_name))
    print (guild)
    print (type(guild))
    chan=await guild.create_text_channel(channel_name)
    print ("done")
    chan.edit(category="TEST")
    print ("done")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send('The syntax is wrong, you are missing an arguement')
'''
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower() == 'e':
        response = "E is bad"
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        try:
            raise discord.DiscordException
        except DiscordException as e:
            response = 'Error occurred : ' + str(e)
            await message.channel.send(response)
'''
@bot.event
async def on_raw_reaction_add(payload):
    channel_nam=[]
    message_id=payload.message_id
    print(payload.emoji)
    print(str(payload.emoji))
    print (message_id)
    message_id=str(message_id)
    if str(payload.emoji) == "📩":
        ticket_numb:list=[]
        channel_num="0"
        path="transcripts\\"
        path=path+"ticket_number.csv"
        ticket_num = pd.read_csv(path, usecols=["0"])
        ticket_num = ticket_num.values.tolist()
        print (ticket_num)
        for i in ticket_num:
            ticket_numb.append(i[0])
        print (ticket_numb)
        print ("message found")
        if message_id == "760450375139852330":
            ticket_cat="Specialist-App"
            channel_num=ticket_numb[0]
            ticket_numb[0]=int(ticket_numb[0])+1
        elif message_id == "760450653196648470":
            ticket_cat="Enchant"
            channel_num=ticket_numb[1]
            ticket_numb[1]=int(ticket_numb[1])+1
        elif message_id == "760450888442839080":
            ticket_cat="Pet"
            channel_num=ticket_numb[2]
            ticket_numb[2]=int(ticket_numb[2])+1
        elif message_id == "760535433905569813":
            ticket_cat="Item"
            channel_num=ticket_numb[3]
            ticket_numb[3]=int(ticket_numb[3])+1
        elif message_id == "760535471255191582":
            ticket_cat="Construction"
            channel_num=ticket_numb[4]
            ticket_numb[4]=int(ticket_numb[4])+1
        elif message_id == "760535505116069928":
            ticket_cat="Essence"
            channel_num=ticket_numb[5]
            ticket_numb[5]=int(ticket_numb[5])+1
        elif message_id == "760542464640811040":
            ticket_cat="Rental"
            channel_num=ticket_numb[6]
            ticket_numb[6]=int(ticket_numb[6])+1
        elif message_id == "761624869250793534":
            ticket_cat="Dungeon"
            channel_num=ticket_numb[7]
            ticket_numb[7]=int(ticket_numb[7])+1
        else:
            ticket_cat="none"

        if ticket_cat=="none":
            print ("not a ticket")
        else:
            channel_num=str(channel_num)
            channel_name = ticket_cat+"-" + channel_num.zfill(3)
            print(channel_name)
            print(type(channel_name))
            channel_name = str(channel_name)
            print ("ticket registered")
            guild = bot.get_guild(payload.guild_id)
            category =  discord.utils.get(guild.categories, name="TEST")
            channel =  bot.get_channel(payload.channel_id)
            chan=await guild.create_text_channel(channel_name,category=category,sync_permissions=True)
            #chan.edit(sync_permissions=true)
            message = await channel.fetch_message(payload.message_id)
            user = bot.get_user(payload.user_id)
            await message.remove_reaction("📩",user)
            channel_num=int(channel_num)
            channel_num+=1
            ticket_num_csv = pd.DataFrame(ticket_numb)
            path = "C:\\Users\\home\\PycharmProjects\\DiscordBot\\transcripts\\"
            path = path + "ticket_number.csv"
            print("path is:", path)
            print(ticket_num_csv)
            ticket_num_csv.to_csv(path, index=False)
            user_id=user.id
            await chan.send(f"<@{str(user_id)}> someone will attend you shortly, if its an urgent thing then you can ping them.")
            command_em=discord.Embed(title="Here are some commands if you need", color=int("11447726"), description="`?close` - closes this ticket and also saves transcript \n `?open` - opens a closed ticket again")
            await chan.send(embed=command_em)
            await chan.set_permissions(user,send_messages=True,read_messages=True)

@bot.event
async def on_ready():
    print ("ready")
    #chan_d="760450174660509706"
    #msg_d=["760450653196648470","760450888442839080","760535471255191582","760535505116069928","760542464640811040","761624869250793534"]
    #channel=bot.get_channel(int(chan_d))
    #for d in msg_d:
    #    message = await channel.fetch_message(int(d))
    #    await message.add_reaction("📩")

def Reverse(lst):
    return [ele for ele in reversed(lst)]
@bot.command(name='close', help='closes the ticket')
async def close(ctx):
    chann=ctx.message.channel
    channel=ctx.channel
    print (channel)
    messages = await channel.history(limit=5).flatten()
    print ("1")
    print (messages)
    messages=Reverse(messages)
    print ("2")
    #channel = bot.get_channel(760903520332939274)
    channel_name=channel.name
    channel_name=str(channel_name)
    channel_numb=channel_name[-3:]
    print ("channel numb: ",int(channel_numb))
    if int(channel_numb)>-1:
        print ("opening colors")
        with open("users_ticket_log.txt", 'rb') as f:
            users = pickle.load(f)
        with open("colors_ticket_log.txt", 'rb') as f:
            colors = pickle.load(f)
        print ("colors opened")
        closed_name="closed-"+channel_name
        print (str(closed_name))
        print (type(closed_name))
        print (type(channel))
        print ("3")
        #users:list=["Dot_Squad#4627","lulu12457#5077"]
        print (type(users))
        #colors:list=["16743935","26348"]
        print (type(colors))
        content_log:list=[]
        time_log:list=[]
        user_log:list=[]
        avatar_log:list=[]
        for message in messages:
            msg_log: list = []
            print("3")
            user=message.author
            print ("4")
            user_str=str(user)
            print ("5")
            in_list:bool=False
            print ("6")
            print (user_str)
            for i in users:
                print ("7")
                if user_str==i:
                    print ("in_list=true")
                    in_list=True
                    color=colors[users.index(user_str)]
                    color = int(color)
                    #break
            if in_list==False:
                print("in_list=false")
                users.append(user_str)
                print("8")
                color=Color()
                color_was_in:bool=False
                while True:
                    for i in colors:
                        if color==i:
                            color=Color()
                            color_was_in=True
                    if color_was_in==False:
                        break
                print("9")
                color=str(color)
                print("10")
                colors.append(color)
                print("11")
                color=int(color)
                print("12")
            print("4")
            content=message.content
            print("5")
            avatar=user.avatar_url
            print("6")
            user=str(user)
            content=str(content)
            print (avatar)
            print (type(content))
            content_log.append(content)
            time_log.append(message.created_at)
            user_log.append(user_str)
            avatar_log.append(avatar)
            #msgs_logs.append(msg_log)
            '''
            msg_log=discord.Embed(title=content,color=color,timestamp=message.created_at)
            print("7")
            msg_log.set_footer(
                text=user_str,
                icon_url=avatar,
            )
            print("7.1")
            print("7.2")
            print("7.3")
            print("7.4")
            print("7.5")
            print("7.6")
    
            print("8")
            await channel.send(embed=msg_log)
            #msg_log=[]
            #msg_log.append(content)
            print ("sent successfully")
            '''
            #with open(channel_name, 'a') as f:
            #    pickle.dump(msg_log, f)
        msgs_logs={"content":content_log,"time":time_log,"user":user_log,"avatar":avatar_log}
        print ("log dumped")
        with open("users_ticket_log.txt", 'w') as f:
            pickle.dump(users, f)
        with open("colors_ticket_log.txt", 'wb') as f:
            pickle.dump(colors, f)
        print ("log starting")
        channel_name_og=channel_name
        channel_name=channel_name+".csv"
        print ("log filename made")
        print (type(msgs_logs))
        #key="❧"
        #msg_logs=key.join(msgs_logs)
        print(msgs_logs)
        print (channel_name)
        #np.savetxt(channel_name,
        #           msgs_logs,
        #           delimiter=key,
        #           fmt='% s')
        msgs_logs_csv=pd.DataFrame(msgs_logs)
        path="transcripts\\"
        path=path+channel_name
        print ("path is:",path)
        print (msgs_logs_csv)
        msgs_logs_csv.to_csv(path,index=False)
        print (channel_name)
        #msg=open(channel_name,'r')
        #print (msg.read())
        print (msgs_logs)
        #with open(channel_name, 'wb') as f:
        #    pickle.dump(msgs_logs, f)
        print ("log dumped")
        log_channel=bot.get_channel(int("761466149233098762"))
        description=f"do `?open-transcript {channel_name_og}` \n To open the transcript"
        print (description)
        log_em= discord.Embed(title=channel_name_og, color=int("16777215"),timestamp=ctx.message.created_at,description=description)
        print("7")
        print (avatar)
        print (user_str)
        log_em.set_footer(
            text=user_str,
            icon_url=avatar,
        )
        print ("uhh")
        msg=ctx.message
        #print (msg)
        print (msg.author.id)
        print (type(msg.author.id))
        #mention="<@"+str(msg.auther.id)+">"
        print (f"<@{str(msg.author.id)}>")
        description=f"Closed by <@{str(msg.author.id)}> \n The transcript has also been saved. \n Do `?open` to reopen this ticket."
        end_em=discord.Embed(title="Ticket Closed", color=int("16777215"),timestamp=ctx.message.created_at,description=description)
        await channel.send(embed=end_em)
        await log_channel.send(embed=log_em)
        await chann.edit(name=closed_name)






@bot.command(name='open', help='reopens the ticket')
async def close(ctx):
    channel=ctx.message.channel
    channel_name=channel.name
    channel_name=str(channel_name)
    print (channel_name[0:6])
    if channel_name[0:6]=="closed":
        channel_name=channel_name[7:]
        print ("opening the ticket. \n Note: changing the channel name might take a few mniutes as discord API limits exist.")
        await channel.edit(name=channel_name)
        print ("done")



@bot.command(name='open-transcript', help='opens a transcript')
async def open_trans(ctx, name):
    print ("opening")
    name=str(name)
    name_og=name
    name_og=name_og+".csv"
    #name_og="log.csv"
    name=name+"-transcript"
    guild = ctx.guild
    category = discord.utils.get(guild.categories, name="TRANSCRIPTS")
    channel = await guild.create_text_channel(name,sync_permissions=True,category=category)
    print(f'Creating a new channel: {name}')
    print("done")
    await channel.edit(category=category,sync_permissions=True)
    print("done")
    print (name_og)
    path="transcripts\\"
    path=path+name_og
    print ("path obtained: ",path)
    #print (type(msgs_logs))
    #print (msgs_logs)
    content_logs:list=[]
    time_logs:list=[]
    user_logs:list=[]
    avatar_logs:list=[]
    msgs_logs = pd.read_csv(path,usecols =["content"])
    content_logs=msgs_logs.values.tolist()
    msgs_logs = pd.read_csv(path,usecols =["time"])
    time_logs=msgs_logs.values.tolist()
    msgs_logs = pd.read_csv(path,usecols =["user"])
    user_logs=msgs_logs.values.tolist()
    msgs_logs = pd.read_csv(path,usecols =["avatar"])
    avatar_logs=msgs_logs.values.tolist()
    print ("for loop starts")
    with open("users_ticket_log.txt", 'rb') as f:
        users = pickle.load(f)
    with open("colors_ticket_log.txt", 'rb') as f:
        colors = pickle.load(f)

    for i in range(0,len(content_logs)):
        print (type(content_logs))
        print (content_logs[i])
        content=content_logs[i]
        msg_time=time_logs[i]
        user_str=user_logs[i]
        print (user_str)
        avatar=avatar_logs[i]
        print ("1")
        in_list: bool = False
        print ("2")
        color_was_in:bool=False
        print (str(user_logs[1]))
        print (user_logs[1])
        for d in user_logs:
            print("3")
            if str(user_str) == str(d):
                print("in_list=true")
                in_list = True
                print ("3.1")
                print (users[1])
                print (user_str[0])
                print (type(users[1]))
                print (type(user_str))
                print (users.index(user_str[0]))
                color = colors[users.index(user_str[0])]
                print ("3.2")
                color = int(color)
                print ("3.3")
                # break
        if in_list == False:
            print("in_list=false")
            users.append(user_str)
            print("4")
            color = Color()
            print("5")
        print ("saving colors")
        with open("users_ticket_log.txt", 'wb') as f:
            pickle.dump(users,f)
        with open("colors_ticket_log.txt", 'wb') as f:
            pickle.dump(users,f)
        print ("colors saved")
        while True:
            print ("while loop starts")
            for i in colors:
                if color == i:
                    print("color was in alr")
                    color = Color()
                    color_was_in = True
                    print("colors fixed")
            if color_was_in == False:
                print("color was not in")
                break
        print("6")
        print (content[0])
        print (color)
        print (type(msg_time[0]))
        print (msg_time[0])
        time_msg = datetime.datetime.strptime(msg_time[0], '%Y-%m-%d %H:%M:%S.%f')
        print (type(time_msg))
        print (time_msg)
        msg_log_em = discord.Embed(title=content[0], color=color,timestamp=time_msg)
        print("7")
        print (avatar)
        print (user_str)
        msg_log_em.set_footer(
            text=user_str[0],
            icon_url=avatar[0],
        )
        with open("users_ticket_log.txt", 'wb') as f:
            pickle.dump(users, f)
        with open("colors_ticket_log.txt", 'wb') as f:
            pickle.dump(colors, f)
        print("8")
        await channel.send(embed=msg_log_em)
        # msg_log=[]
        # msg_log.append(content)
        print("sent successfully")

@bot.command(name='delete', help='reopens the ticket')
async def delete_tick(ctx):
    channel=ctx.channel
    channel_name = channel.name
    channel_name = str(channel_name)
    channel_numb = channel_name[-3:]
    print("channel numb: ", int(channel_numb))
    if int(channel_numb) > -1:
        with open("users_ticket_log.txt", 'rb') as f:
            users = pickle.load(f)
        with open("colors_ticket_log.txt", 'rb') as f:
            colors = pickle.load(f)
        channel=ctx.channel
        channel_name=channel.name
        messages = await channel.history(limit=5).flatten()
        print ("1")
        print (messages)
        messages=Reverse(messages)
        print("colors opened")
        print("3")
        # users:list=["Dot_Squad#4627","lulu12457#5077"]
        print(type(users))
        # colors:list=["16743935","26348"]
        print(type(colors))
        content_log: list = []
        time_log: list = []
        user_log: list = []
        avatar_log: list = []
        for message in messages:
            msg_log: list = []
            print("3")
            user = message.author
            print("4")
            user_str = str(user)
            print("5")
            in_list: bool = False
            print("6")
            print(user_str)
            for i in users:
                print("7")
                if user_str == i:
                    print("in_list=true")
                    in_list = True
                    color = colors[users.index(user_str)]
                    color = int(color)
                    # break
            if in_list == False:
                print("in_list=false")
                users.append(user_str)
                print("8")
                color = Color()
                color_was_in: bool = False
                while True:
                    for i in colors:
                        if color == i:
                            color = Color()
                            color_was_in = True
                    if color_was_in == False:
                        break
                print("9")
                color = str(color)
                print("10")
                colors.append(color)
                print("11")
                color = int(color)
                print("12")
            print("4")
            content = message.content
            print("5")
            avatar = user.avatar_url
            print("6")
            user = str(user)
            content = str(content)
            print(avatar)
            print(type(content))
            content_log.append(content)
            time_log.append(message.created_at)
            user_log.append(user_str)
            avatar_log.append(avatar)
            # msgs_logs.append(msg_log)
            '''
            msg_log=discord.Embed(title=content,color=color,timestamp=message.created_at)
            print("7")
            msg_log.set_footer(
                text=user_str,
                icon_url=avatar,
            )
            print("7.1")
            print("7.2")
            print("7.3")
            print("7.4")
            print("7.5")
            print("7.6")
    
            print("8")
            await channel.send(embed=msg_log)
            #msg_log=[]
            #msg_log.append(content)
            print ("sent successfully")
            '''
            # with open(channel_name, 'a') as f:
            #    pickle.dump(msg_log, f)
        msgs_logs = {"content": content_log, "time": time_log, "user": user_log, "avatar": avatar_log}
        print("log dumped")
        with open("users_ticket_log.txt", 'wb') as f:
            pickle.dump(users, f)
        with open("colors_ticket_log.txt", 'wb') as f:
            pickle.dump(colors, f)
        print("log starting")
        channel_name_og = channel_name
        channel_name = channel_name + ".csv"
        print("log filename made")
        print(type(msgs_logs))
        # key="❧"
        # msg_logs=key.join(msgs_logs)
        print(msgs_logs)
        print(channel_name)
        # np.savetxt(channel_name,
        #           msgs_logs,
        #           delimiter=key,
        #           fmt='% s')
        msgs_logs_csv = pd.DataFrame(msgs_logs)
        path = "C:\\Users\\home\\PycharmProjects\\DiscordBot\\transcripts\\"
        path = path + channel_name
        print("path is:", path)
        print(msgs_logs_csv)
        msgs_logs_csv.to_csv(path, index=False)
        print(channel_name)
        # msg=open(channel_name,'r')
        # print (msg.read())
        print(msgs_logs)
        # with open(channel_name, 'wb') as f:
        #    pickle.dump(msgs_logs, f)
        print("log dumped")
        log_channel = bot.get_channel(int("761466149233098762"))
        description = f"do `?open-transcript {channel_name_og}` \n To open the transcript. \n This ticket has been deleted"
        print(description)
        log_em = discord.Embed(title=channel_name_og, color=int("16711680"), timestamp=ctx.message.created_at,
                               description=description)
        print("7")
        print(avatar)
        print(user_str)
        log_em.set_footer(
            text=user_str,
            icon_url=avatar,
        )
        print("uhh")
        msg = ctx.message
        # print (msg)
        print(msg.author.id)
        print(type(msg.author.id))
        # mention="<@"+str(msg.auther.id)+">"
        print(f"<@{str(msg.author.id)}>")
        await channel.send("This channel will be deleted in 5 seconds")
        await log_channel.send(embed=log_em)
        await asyncio.sleep(5)
        await channel.delete()
        #await bot.delete(channel)

#bot.run('NzYxODgwMTkzNTE3NjE3MTc0.X3hCOQ.n5t8yDy5iuQlTguQEpXQHdGF1IA')
bot.run('NzM1NzExNTc0NjI2NDAyMzU2.XxkOzA.PMAmMVwN1TINchuLy74_0Kb33Kw')