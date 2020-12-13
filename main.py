import asyncio
import discord
import pickle
import datetime
import re
from threading import Thread
import time
import json
import os
import mysql.connector
from discord.ext import commands
import time
from discord.utils import get
import discord.errors



#Modules
import moderation
import premium
import rewards
import ticketing
import utilities

client = discord.Client()
token = ''


#Global variables
ipgrab = ["GRABIFYLINK", "LEANCODINGCO", "SIOPIFY", "FREEGIFICARDSCO", "CURIOUSCAICLUB", "CAISNIHINGSFUN", "JOINMYSIIE",
          "CAISNIHINGSCOM", "IPLOGGERORG", "BLASZECOM", "WEBRESOLVERNL", "CURLV", "SHORIESI", "BIIURLIO", "RURLCO",
          "IPLOGGERCOM", "IPLOGGERRU", "2NOCO", "YIPSU"]
blocked_word = ['NIGGA', 'NIGGER', "NIGG", "REGIN", "IMAGPX", "REGGIN", "FAGGOT", "RETARD"]
secretcode = ['p!autodelete']
time_convert = {"s": 1, "m": 60, "h": 3600, "d": 86400}



global transactionmanager_online
transactionmanager_online = '0'

async def log(action, description):
    embed=discord.Embed(title=action, description=description, color=0xe22400)
    embed.set_footer(text="Action Logging")
    await client.get_channel(683331960705515570).send(embed=embed)

@client.event
async def on_raw_reaction_add(payload):
    emoji = str(payload.emoji)
    if payload.event_type == 'REACTION_ADD':
        member = client.get_user(payload.user_id)
        if member == None:
            return
        if member.bot == True:
            return
        try:
            message = await client.get_channel(payload.channel_id).fetch_message(payload.message_id)
        except discord.errors.NotFound:
            return
    else:
        return

@client.event
async def on_member_update(before,after):
    await moderation.scanning.nickname(before, after)

@client.event
async def on_member_join(member):
    captcha = secrets.token_hex(nbytes=6)
    await member.send("your captcha is __~~***" + captcha + "***~~__")

    def check(m):
        return m.content == captcha
    try:
    msg = await client.wait_for('message', timeout=60.0, check=check)
    except asynio.timeout:
      await.send("sorry but fuck off")
      return
    await member.send("gg u passed captcha")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if msg_analysis(message):
        return

    commands={
        ['p!clear', 'p!purge'] : moderation.housekeeping.clear,
        ['p!youtube-ping', 'p!youtubeping'] : utilities.pings.youtube_ping,
        ['p!specialist-ping', 'p!specialistping'] : utilities.pings.specialist_ping,
        ['p!event-ping', 'p!eventping'] : utilities.pings.event_ping,
        ['p!say', 'p!send'] : moderation.housekeeping.say,
        ['p!edit'] : moderation.housekeeping.edit,
        ['p!react'] : moderation.housekeeping.react,
        ['p!report'] : moderation.reportsystem.report,
        ['p!verify'] : utilities.verify.verify,
        ["p!ban"]: ban,
        ["p!tempban"]: TempBan,
        ["p!start-transactionmanager","p!start","p!start-transactionsmanager"]: start_transactionmanager,
        ["p!forceupdate-transaction","p!forceupdate-transactions","p!force-transaction","p!forceupdate"]: transactionmanager_forceupdate,
        ["p!mute","p!tempmute"]: Tempmute,
        ["p!punishments","p!punishment","p!punish"]: logs_user,
        ["p!case","p!view-case","p!viewcase"]: case,
        ["p!removecase","p!remove","p!remove-case"]: remove_case,
        ["p!reason","p!view-reason","p!viewreason"]: change_reason,
        ["p!warn"]: warn,
        ["p!serviceban","p!servicesban","p!services-ban","p!service-ban"]: temp_service_ban,
        ["p!unmute"]: unmute,
        ["p!unban"]: unban,
        ["p!service-unban","p!servicesunban","p!serviceunban","p!services-unban"]: unban_service
        }
    
    if message.content.startswith('p!')==True:
        for x in commands:
            if message.content.split()[0].lower() in x:
                await commands[x](message)
                return


@client.event
async def on_message_edit(before, after):
    await moderation.scanning.messages(before, after)

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
    await transactionmanager()

client.run(token)
