import re
import discord
import random
from discord.ext import commands
from bs4 import BeautifulSoup
from urllib.request import urlopen


def check_channel():
    """restrict the bot to respond in the "bot-commands" channel only"""

    def predicate(ctx, *args, **kwargs):
        return str(ctx.channel) == "bot-commands"
    return commands.check(predicate)


class search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @check_channel()
    async def image(self, ctx, *, key):
        if ' ' in key:
            key = key.replace(' ', '+')
            print(key)

        url = "http://results.dogpile.com/serp?qc=images&q=" + key

        res = urlopen(url)
        soup = BeautifulSoup(res, "lxml")
        results = []
        https_pattern = r"^(http(s)?:\/\/)"

        images = soup.findAll('img')
        for image in images:
            link = image['src']
            if re.match(https_pattern, link):
                results.append(link)

        await ctx.send(random.choice(results))

    @image.error
    async def image_error(self, ctx, error):
        await ctx.message.delete(delay=10)
        if isinstance(error, commands.CheckFailure):
            temp = await ctx.send("please use this command in the #bot-commands channel")
            await temp.delete(delay=10)
        if isinstance(error, commands.MissingRequiredArgument):
            temp = await ctx.send("please specify of what you want to search")
            await temp.delete(delay=10)

        raise error


def setup(bot):
    bot.add_cog(search(bot))
