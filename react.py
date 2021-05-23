import discord
from discord.ext import commands
from discord.utils import get
import datetime
from datetime import datetime
from config import *

TOKEN = 'ODQ1ODE3NTA1MzA5MTMwNzgy.YKme7w.v60JDY0du-xIq5YIh97KtiZ4Vzk'
BOT_PREFIX = '!'
ROLE = "Test Role"

client = commands.Bot(command_prefix=BOT_PREFIX, description="Test")

@client.event
async def on_message(message):
    empty_array = []
    modmail_channel = discord.utils.get(client.get_all_channels(), name="modmail")
    
    if message.author == client.user:
        return
    if str(message.channel.type) == "private":
        if message.attachments != empty_array:
            files = message.attachments
            #await modmail_channel.send("[" + message.author.display_name + "]")
            await modmail_channel.send("[" + str(message.author) + "]")
            for file in files:
                await modmail_channel.send(file.url)
        else:
            #await modmail_channel.send("[" + message.author.display_name + "]" + message.content)
            await modmail_channel.send("[" + str(message.author) + "]" + message.content)

    elif str(message.channel) == "modmail" and message.content.startswith("<"):
        member_object = message.mentions[0]
        if message.attachments != empty_array:
            files = message.attachments
            await member_object.send("[" + message.author.display_name + "]")
            for file in files:
                await member_object.send(file.url)
        else:
            index = message.content.index(">")
            string = message.content
            mod_message = string[index+1:]
            await member_object.send("[" + message.author.display_name + "]" + mod_message)

#initialize
@client.event
async def on_ready():
    print("Logged in as: " + client.user.name + "\n")

#hello command
@client.command()
@commands.has_permissions(administrator=True)
async def dm(ctx,member:discord.Member):
    await ctx.send('Message:')
    def check(m):
        return m.author.id == ctx.author.id
    
    message = await client.wait_for('message', check=check)
    await ctx.send(f'sent message to {member}')
    
    await member.send(f'{ctx.author.mention} Has a message for you:\n {message.content}')
    

#embed
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def now(ctx):
    embed = discord.Embed(
        title="React to schedule appointment",
        description='Only react if you have bought the 15 dollar service fee',
        url='https://www.paypal.com/paypalme/mrmyst/15',
        timestamp=datetime.now(),
        color=0x1abc9c
    )
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('✅')
    await ctx.message.add_reaction('✅')

#reaction add role
@client.event
async def on_raw_reaction_add(payload):
    ourMessageID = 845836362921934879

    if ourMessageID == payload.message_id:
        member = payload.member
        guild = member.guild

        emoji = payload.emoji.name
        if emoji == '✅':
            role = discord.utils.get(guild.roles, name="Scheduled")
        await member.add_roles(role)

#reaction remove role
@client.event
async def on_raw_reaction_remove(payload):
    ourMessageID = 845836362921934879

    if ourMessageID == payload.message_id:
        guild = await(client.fetch_guild(payload.guild_id))
        emoji = payload.emoji.name
        if emoji == '✅':
            role = discord.utils.get(guild.roles, name="Scheduled")
        member = await(guild.fetch_member(payload.user_id))
        if member is not None:
            await member.remove_roles(role)
        else:
            print("member not found")


#clear messages
@client.command(pass_conxtext=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: str):
    if amount == 'all':
        await ctx.channel.purge()
    else:
        await ctx.channel.purge(limit=(int(amount) +1))

#error
@client.event
async def on_command_error(ctx, error):
    print(ctx.command.name + " was invoked incorrectly.")
    print(error)


client.run(TOKEN, bot=True, reconnect=True)
