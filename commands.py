
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
WEATHERKEY = os.getenv("weather")
CURRENKEY = os.getenv("CURRENCY")

weather_url = "http://api.openweathermap.org/data/2.5/weather?"


class botCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


        @bot.command()
        async def ping(ctx):
            await ctx.send("pong!")

        @bot.command()
        @commands.has_permissions(administrator = True)
        async def ban(ctx, member: discord.Member, *, reason = None):
            """:with great power comes great responsibility"""
            if reason == None:
                reason = "no reason lol"
            await ctx.guild.ban(member)
            await ctx.send(f"User {member.mention} has been banned for {reason}. Goodbye back to the lobby!")



        @bot.command()
        async def cointoss(ctx):
            """:flips a coin"""
            rng = random.randint(1,2)
            if rng == 1:
                await ctx.send("heads")
            else:
                await ctx.send("tails")


        @bot.command()
        async def dice(ctx, rolls: int, type):
            """:[number of rolls] [type of dice (d1,d2,...d20)]"""
            ret = []
            sides = int(type[1:])
            i = 0
            while i < rolls:
                rng = random.randint(1,sides)
                ret.append(rng)
                i += 1
            await ctx.send(f"dice tosses: {ret}")

        @bot.command()
        async def calculate(ctx, a: int, op: str, b: int):
            """:can only add, subtract, multiply, divide, and modulo for now"""
            ret = 0
            if op == "+":
                ret = a + b
            elif op == "-":
                ret = a - b
            elif op == "*":
                ret = a * b
            elif op == "/":
                ret = a / b
            elif op == "%":
                ret = a % b
            else:
                ret = "im not that advanced chill"
            await ctx.send(ret)

        @bot.command()
        async def weather(ctx, *, city: str):
            """:[city]"""
            city_name = city
            complete_url = weather_url + "appid=" + WEATHERKEY + "&q=" + city_name
            response = requests.get(complete_url)
            x = response.json()
            channel = ctx.message.channel
            
            #getting all the deets on the weather
            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_temperature_celsius = str(round(current_temperature - 273.15))
                current_pressure = y["pressure"]
                current_humidity = y["humidity"]
                z = x["weather"][0]
                weather_description = z["description"]

                #making the reply look formatted and neat
                embed = discord.Embed(
                    title=f"Weather forecast - {city_name}",
                    color=0x7289DA,
                    timestamp=ctx.message.created_at,
                )
                embed.add_field(
                    name="Description",
                    value=f"**{weather_description}**",
                    inline=False)
                embed.add_field(
                    name="Temperature(C)",
                    value=f"**{current_temperature_celsius}°C**",
                    inline=False)
                embed.add_field(
                    name="Humidity(%)", value=f"**{current_humidity}%**", inline=False)
                embed.add_field(
                    name="Atmospheric Pressure(hPa)",
                    value=f"**{current_pressure}hPa**",
                    inline=False)
                embed.set_footer(text=f"Requested by {ctx.author.name}")

                await channel.send(embed=embed)

            else:
                await channel.send(f"bruh where is that")

        @bot.command()
        async def exchange(ctx, currency1, currency2):
        
            """:[currency1] [currency2]"""
            url = f"https://openexchangerates.org/api/latest.json?app_id={CURRENKEY}&base={'USD'}"

            response = requests.get(url)
            x = response.json()

            if currency1.upper() not in x['rates'] or currency2.upper() not in x['rates']:
                await ctx.send('Invalid currency code!')
                return
            
            rate = x['rates'][currency1.upper()] / x['rates'][currency2.upper()]

            await ctx.send(f"1 {currency2.upper()} = {rate:.2f} {currency1.upper()}")


        @bot.command()
        async def sayit(ctx):
            await ctx.send("RISHEN GAP")
