import asyncio
import discord
import pickle
import datetime
import re
from threading import Thread
import time
import json

client = discord.Client()

ipgrab = ["GRABIFYLINK", "LEANCODINGCO", "SIOPIFY", "FREEGIFICARDSCO", "CURIOUSCAICLUB", "CAISNIHINGSFUN", "JOINMYSIIE",
          "CAISNIHINGSCOM", "IPLOGGERORG", "BLASZECOM", "WEBRESOLVERNL", "CURLV", "SHORIESI", "BIIURLIO", "RURLCO",
          "IPLOGGERCOM", "IPLOGGERRU", "2NOCO", "YIPSU"]
blocked_word = ['NIGGA', 'NIGGER', "NIGG", "REGIN", "IMAGPX", "REGGIN", "FAGGOT", "RETARD"]
secretcode = ['p!autodelete']

@client.event
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


@client.event
async def on_member_update(before,after):
    nickname=str(after.nick)
    if any(ele in nickname.replace("\n", "").replace("t", "i").replace("-", "").replace(" ", "").replace(".", "").replace('"', "").replace(",", "").replace("REGIONAL_INDICATOR_", "").replace(":", "").replace("_","").replace("*", "") for ele in blocked_word) == True:
        await after.send('Please refrain from using derogartory language in your Nicknames. Attempts to circumvent this filter will result in severe punishment!')
        await log('Bad language was detected in ' + after.name + '\'s nickname, it has been deleted and PM has been sent.')
        await after.edit(nick=before.nick)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if msg_analysis(message):
        return

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
    
    if message.content.startswith('p!')==True:
        if message.content.split()[0] in commands:
            await commands[message.content.split()[0]](message)
            return


@client.event
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
    devlog = client.get_channel(int("683331960705515570"))
    await devlog.send(text)

@client.event
async def on_ready():
    print("====================")
    print("Paradise Bot Started")
    print("====================")
    activity = discord.Activity(name='Paradise Network', type=discord.ActivityType.watching)
    await client.change_presence(status=discord.Status.online, activity=activity)

bot.run('NzYxOTcwNDc3NTMwNzQyNzg0.X3iWTg.ot6JKf2tUDKK7nNDHiTfSLoGskE')
