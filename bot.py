import discord
import os
from discord.ext import commands

bot = commands.Bot(command_prefix='~')


@bot.event
async def on_ready():
    print("Bot is awake!")
    print("_______________________________")
    print()


@bot.command()
async def reload(ctx, cog):
    try:
        bot.unload_extension(f"cogs.{cog}")
        bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"{cog} got reloaded")
    except Exception as e:
        print(f"{cog} cannot be loaded")
        raise e


for cog in os.listdir(".\\cogs"):
    if cog.endswith(".py"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f"{cog} cannot be loaded")
            raise e

token = os.environ.get("DISCORD_BOT_TOKEN")
bot.run(token)
