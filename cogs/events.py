import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        hpbd_list = ["happy birthday", "hpbd"]
        hpbd = any(elem in message.content.lower() for elem in hpbd_list)
        if (hpbd):
            await message.channel.send(f"{message.content.title()} :tada: :birthday: :tada: ")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await ctx.message.delete(delay=10)
        if isinstance(error, commands.CommandNotFound):
            temp = await ctx.send("the command does not exist")
            await temp.delete(delay=10)

        raise error


def setup(bot):
    bot.add_cog(Events(bot))
