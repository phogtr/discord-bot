import discord
import os
import random
from discord.ext import commands


def check_channel():
    """restrict the bot to respond in the "bot-commands" channel only"""

    def predicate(ctx, *args, **kwargs):
        return str(ctx.channel) == "bot-commands"
    return commands.check(predicate)


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["8ball"], help="play 8ball")
    @check_channel()
    async def _8ball(self, ctx, *, question):

        """Play 8ball"""

        cur_path = os.path.dirname(__file__)
        new_path = os.path.join(cur_path, '..', 'rsrc', '8ball.txt',)

        try:
            with open(new_path, 'r') as f:
                contents = f.readlines()
                await ctx.send("{}\nQuestion: {}\nAnswer: {}".format(ctx.author.mention, question, random.choice(contents)))
        except Exception as e:
            print("8ball.txt cannot be read")
            raise e

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        await ctx.message.delete(delay=10)
        if isinstance(error, commands.CheckFailure):
            temp = await ctx.send("please use this command in the #bot-commands channel")
            await temp.delete(delay=10)
        if isinstance(error, commands.MissingRequiredArgument):
            temp = await ctx.send("please specify the message")
            await temp.delete(delay=10)

        raise error

    @commands.command(aliases=["fortune cookies"], help="display a quote from fortune cookie")
    @check_channel()
    async def fortune(self, ctx):

        """display a quote from the fortune cookie"""

        cur_path = os.path.dirname(__file__)
        new_path = os.path.join(cur_path, '..', 'rsrc', 'fortune_quote.txt',)

        try:
            with open(new_path, 'r') as f:
                myline = random_line(f)
                await ctx.send("{}\n{}".format(ctx.author.mention, myline))
        except Exception as e:
            print("fortune_quote,txt cannot be read")
            raise e

    @fortune.error
    async def fortune_error(self, ctx, error):
        await ctx.message.delete(delay=10)
        if isinstance(error, commands.CheckFailure):
            temp = await ctx.send("please use this command in the #bot-commands channel")
            await temp.delete(delay=10)

        raise error


def random_line(theFile):
    """simplified Waterman's "Reservoir Algorithm" """

    line = next(theFile)
    for num, line in enumerate(theFile, 2):
        if random.randrange(num):
            continue
        myline = line
    return myline


def setup(bot):
    bot.add_cog(Games(bot))
