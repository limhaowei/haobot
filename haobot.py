
import typing
import discord
import asyncio
from discord.ext import commands
import json
import datetime 
from discord import app_commands
import random
import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")




intents = discord.Intents.default()
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix = "$", intents = discord.Intents.all())



#telling time
time  = datetime.datetime.now()
today = datetime.date.today()

#weather API

weather_url = "http://api.openweathermap.org/data/2.5/weather?"




@bot.event
async def on_ready():
    # channel = bot.get_channel(1118081575163269193)
    print('haobot is online!')



@bot.command(aliases=["die"])
@commands.has_permissions(administrator=True)
async def close(ctx):
    """:kills haobot"""
    await ctx.send("brb getting milk")
    print("haobot died")
    await bot.close()
    

@bot.event
async def on_message(message):  
    if message.author == bot.user:
        return
    
    elif message.content.startswith("hello!"):
        async with message.channel.typing():
            await message.channel.send("hi!")

    elif message.content.startswith("what's the time now?"):
        await message.channel.send("The current date and time is: " + today.strftime(r"%d/%m/%Y") + " " + time.strftime(r"%I:%M %p"))
    
    elif message.content.startswith("fuck off"):
        async with message.channel.typing():
            await message.channel.send("no u")
    
    elif message.content.startswith("thank you haobot"):
        async with message.channel.typing():
            await message.channel.send("no problem")


    await bot.process_commands(message)



