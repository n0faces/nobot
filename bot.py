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

@bot.event
async def on_ready():
    print('--------------------------')
    print(' noface bot has connected ')
    print('--------------------------')

#-------------------------------------------------------------------------------

#Status Cycle
status = ['with my charles demons', 'with Discord.py', 'my floppy drive...', 'with 4heds 4hed', 'with Syntax errors', 'with my wires ;)',]

async def change_status():
    await bot.wait_until_ready()
    msgs = cycle(status)

    while not bot.is_closed:
        current_status = next(msgs)
        await bot.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(15)

# Connection status



#-------------------------------------------------------------------------------

#AUTO ROLE
@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name='users')
    await bot.add_roles(member, role)

# COMMANDS BELOW
#-------------------------------------------------------------------------------

# Ping Pong Connection Test


@bot.command(pass_context=True)
async def ping(ctx):
    """tests bot connection"""
    embed = discord.Embed(title="Pong! :ping_pong:")
    await bot.say(embed=embed)

@bot.command(pass_context=True)
@commands.has_role("staff")
async def users(ctx):
    """amount of users on server"""
    amount = len(ctx.message.server.members)
    await bot.say('There are `' + str(amount) + '` users')


@bot.command(pass_context=True)
async def whatsmyip(ctx):
    """check your ip address"""
    embed = discord.Embed(title="You can check your ip here http://noface.cf/wmip/ ")
    await bot.say(embed=embed)

#-------------------------------------------------------------------------------
@bot.command(pass_context=True)
async def passwordgen(ctx):
    """get noface bot invite link"""
    embed = discord.Embed(title="Generate a password here http://noface.cf/pswrd ")
    await bot.say(embed=embed)

#-------------------------------------------------------------------------------

@bot.command(pass_context=True)
async def invite(ctx):
    """get noface bot invite link"""
    embed = discord.Embed(title=" http://noface.cf ")
    await bot.say(embed=embed)



#-------------------------------------------------------------------------------
@bot.command(pass_context=True)
async def flipcoin(ctx):
    """flips a coin"""
    pick = ['heads','tails']
    flip = random.choice(pick)
    await bot.say ("The coin landed on `" + flip + '`!')

#-------------------------------------------------------------------------------

@bot.command(pass_context=True)
async def eightball(ctx):
    """gives you a random answer from hell"""
    pick = ['probably','fuck yeah','nah','idk you tell me','ask charles','who the fuck knows','could be possible','black people','yah','the demons point to yes','bitch idk','kys','if you pay me i might say yeah','if you pay me i might say no','idk but what i do know is 4hed has the big gay']
    answer = random.choice(pick)
    await bot.say ("`" + answer + '`')



#-------------------------------------------------------------------------------
#Echo Repeat COMMAND
@bot.command()
@commands.has_role("staff")
async def say(*args):
    """bot copies whatever you want it to say """
    output = ''
    for words in args:
        output += words
        output += ' '
    await bot.say(output)
#-------------------------------------------------------------------------------

# CLEAR COMMAND
@bot.command(pass_context=True)
@commands.has_role("staff")
async def clear(ctx, amount=100):
    """delete chat messages up to 100 """
    channel = ctx.message.channel
    messages = []
    async for message in bot.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await bot.delete_messages(messages)
    await bot.say('`{} Messages Have Been Deleted.`'.format(amount,))

#-------------------------------------------------------------------------------

#BOT CREATOR INFO
@bot.command()
async def info():
    """information on who created the bot"""
    embed = discord.Embed(
        title = 'Creator of noface bot.',
        description = 'If you would like to use noface bot on your own server be sure to contact me via Private message. Thank you. ',
        color = discord.Color.red()
    )

    embed.set_footer(text='some credits to poke#0001')
    embed.set_thumbnail(url='https://images-ext-2.discordapp.net/external/zLVr30tyCBfz5vwxlKs_p12QmLod5o7w1l73vFINKcQ/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/396357155290349590/a_c718558fe4b985df93060f116c8b0a8e.gif?size=1024')
    embed.set_author(name='charles#0666')

    await bot.say(embed=embed)


#-------------------------------------------------------------------------------

#KICK/BAN COMMAND
@bot.command(pass_context=True)
@commands.has_role("staff")
async def kick(ctr, user: discord.Member):
    """kicks user from server """
    await bot.say('`{} has been kicked`'.format(user.name),)

    await bot.kick(user)


@bot.command(pass_context=True)
@commands.has_role("staff")
async def ban(ctr, user: discord.Member):
    """bans user of choice """
    await bot.say('`{} has been banned`'.format(user.name))
    await bot.ban(user)

@bot.command(pass_context = True)
async def banlist(ctx):
    '''banlist'''
    x = await bot.get_bans(ctx.message.server)
    x = '\n'.join([y.name for y in x])
    embed = discord.Embed(title = "banned users", description = x, color = 0x00000)
    return await bot.say(embed = embed)

#-------------------------------------------------------------------------------

#server info command
@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.channel)
async def serverinfo(ctx):
    """information about the current server"""
    embed = discord.Embed(name="{}'s info".format(ctx.message.server.name), description="Here's what I could find.", color=0x000000)
    embed.set_author(name="noface")
    embed.add_field(name="Name", value=ctx.message.server.name, inline=True)
    embed.add_field(name="ID", value=ctx.message.server.id, inline=True)
    embed.add_field(name="Roles", value=len(ctx.message.server.roles), inline=True)
    embed.add_field(name="Members", value=len(ctx.message.server.members))
    embed.set_thumbnail(url=ctx.message.server.icon_url)
    await bot.say(embed=embed)

#-------------------------------------------------------------------------------

#user info command
@bot.command(pass_context=True)
async def userinfo(ctx, user: discord.Member):
    """check user information"""
    embed = discord.Embed(title="{}'s info".format(user.name), description="Here's what I could find.", color=0x000000)
    embed.add_field(name="Name", value=user.name, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Status", value=user.status, inline=True)
    embed.add_field(name="Highest role", value=user.top_role)
    embed.add_field(name="Joined", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)
#-------------------------------------------------------------------------------

@bot.command(pass_context = True)
@commands.cooldown(1, 5, commands.BucketType.channel)
async def urban(ctx, *,msg: str):
     '''Urban Dictionary search'''
     word = ''.join(msg)
     api = "http://api.urbandictionary.com/v0/define"
     response = requests.get(api, params=[("term", word)]).json()
     embed = discord.Embed(title = ":mag: Word Searched:", description = word, timestamp = datetime.datetime.utcnow())
     embed.add_field(name = "Top definition:", value = response['list'][0]['definition'])
     embed.add_field(name = "Examples:", value = response['list'][0]["example"])
     await bot.say(embed = embed)
#-------------------------------------------------------------------------------

@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.channel)
@commands.has_role("staff")
async def poll(ctx, question, *options: str):
        if len(options) <= 1:
            await bot.say('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await bot.say('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
        embed = discord.Embed(title=question, description=''.join(description))
        react_message = await bot.say(embed=embed)
        for reaction in reactions[:len(options)]:
            await bot.add_reaction(react_message, reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await bot.edit_message(react_message, embed=embed)



@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.channel)
async def slots(ctx):
        """ Roll the slot machine """
        emojis = "👹🤡🤖👻👿"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]  **,"

        if (a == b == c):
            await bot.say(f"{slotmachine} `All matching!`  ")
        elif (a == b) or (a == c) or (b == c):
            await bot.say(f"{slotmachine} `2 in a row`  ")
        else:
            await bot.say(f"{slotmachine} `rip` ")
#-------------------------------------------------------------------------------

#SIMPLE BITCOIN COMMAND
@bot.command(pass_context=True)
async def btc(ctx):
    """shows Bitcoins latest ammount"""
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    response = requests.get(url)
    value = response.json()['bpi']['USD']['rate']
    await bot.send_message(ctx.message.channel, "Bitcoin price is: $" + value )

#-------------------------------------------------------------------------------

@bot.command(pass_context=True)
@commands.cooldown(1, 5, commands.BucketType.channel)
async def avatar(ctx, user: discord.Member):
    """grabs user of choices avatar"""
    embed = discord.Embed(title="".format(user.name), color=0x000000)
    embed.set_thumbnail(url=user.avatar_url)
    await bot.say(embed=embed)


#-------------------------------------------------------------------------------



@bot.command(pass_context=True)
@is_owner()
async def quit():
    """disconnects bot"""
    await bot.say("`Disconnecting from server.`")
    await bot.logout()


#-------------------------------------------------------------------------------



bot.loop.create_task(change_status())
bot.run(TOKEN)
