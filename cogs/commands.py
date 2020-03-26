import discord
from discord.ext import commands
from datetime import datetime


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="repeating of what you typed")
    async def echo(self, ctx, *, message):
        await ctx.send(message)

    @echo.error
    async def echo_error(self, ctx, error):
        await ctx.message.delete(delay=10)
        if isinstance(error, commands.MissingRequiredArgument):
            temp = await ctx.send("echo")
            await temp.delete(delay=10)

        raise error

    @commands.command(aliases=["cls"], help='clear the message with the given amount')
    async def clear(self, ctx, amount: int):

        """clear the message with the given amount"""

        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"{amount} messages deleted")

    @clear.error
    async def clear_error(self, ctx, error):
        await ctx.message.delete(delay=10)
        if isinstance(error, commands.MissingRequiredArgument):
            temp = await ctx.send("please specify the amount of messages to be deleted")
            await temp.delete(delay=10)
        if isinstance(error, commands.BadArgument):
            temp = await ctx.send("the amount need to be a whole positive number")
            await temp.delete(delay=10)

        raise error

    @commands.command()
    async def date(self, ctx):
        now = datetime.now()
        d = now.strftime("%B %d, %Y, %I:%M:%S %p")
        await ctx.send(d)


def setup(bot):
    bot.add_cog(Commands(bot))
