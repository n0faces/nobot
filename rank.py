import discord
from discord.ext import commands
import asyncio
from itertools import cycle
import json
import os
import datetime
import time
import requests
import random
from discord import Game
from discord.ext.commands import Bot
import aiohttp
from discord.ext import commands as c
from discord import Game, Server, Member, Embed
from helpers import is_owner, get_logger
with open("json/config.json") as cfg:
    config = json.load(cfg)
#-----------------config--------------------

TOKEN        = config["TOKEN"]
prefix       = config["command_prefix"]
log_file     = config["log_file"]
log = get_logger(log_file)

#-------------------------------------------

description="""
noface bot commands
"""
#bot command prefix
bot = c.Bot(c.when_mentioned_or(prefix), pm_help=False, description=description)
os.chdir(r'/home/charles/Desktop/nobot/json')
bot.remove_command('help') # remove that help command
@bot.event
async def on_ready():
    print('-------------------------')
    print(' level bot has connected ')
    print('-------------------------')
#-------------------------------------------------------------------------------
# new event



#-------------------------------------------------------------------------------

#Ranks
@bot.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)

@bot.event
async def on_message(message):
    with open('users.json', 'r') as f:
        users = json.load(f)
    await bot.process_commands(message)
    await update_data(users, message.author)
    await add_experience(users, message.author, 5)
    await level_up(users, message.author, message.channel)

    with open('users.json', 'w') as f:
        json.dump(users, f)

async def update_data(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]['experience'] = 0
        users[user.id]['level'] = 1

async def add_experience(users, user, exp):
    users[user.id]['experience'] += exp

async def level_up(users, user,channel):
    experience = users[user.id]['experience']
    lvl_start = users[user.id]['level']
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
        await bot.send_message(channel, '{} has leveled up to level {}'.format(user.mention, lvl_end))
        users[user.id]['level'] = lvl_end





#id
@bot.command(pass_context=True)
async def id(ctx, user: discord.Member = None):
    """says your/mentions account id"""
    user = user or ctx.message.author
    with open('users.json') as f:
        data = json.load(f)

    if data.get(user.id) is not None:
        await bot.say('`User id is {}`'.format(user.id))
    else:
        await bot.say(f'I can not seem to grab your id')

#-------------------------------------------------------------------------------

#XP/Level
@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.channel)
async def xp(ctx, user: discord.Member = None):
    """says your/mentions XP count """
    user = user or ctx.message.author
    with open('users.json') as f:
        data = json.load(f)

    if data.get(user.id) is not None:
        await bot.say(f'`XP count is at {data[user.id]["experience"]}.`')
    else:
        await bot.say(f'`I cannot see {user.mention} in my list of users.`')

#--------------------------------------

@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.channel)
async def level(ctx, user: discord.Member = None):
    """says your/mentions level """
    user = user or ctx.message.author
    with open('users.json') as f:
        data = json.load(f)

    if data.get(user.id) is not None:
        await bot.say(f'`User level is {data[user.id]["level"]}.`')
    else:
        await bot.say(f'`I cannot see {user.mention} in my list of users.`')



bot.run(TOKEN)
