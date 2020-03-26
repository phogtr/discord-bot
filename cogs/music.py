import os
import re
import subprocess
import shutil
import youtube_dl
import discord
from discord.ext import commands
from discord.utils import get


def check_channel():
    channels = ["music", "bot-commands"]

    def predicate(ctx, *args, **kwargs):
        return str(ctx.channel) in channels
    return commands.check(predicate)


class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["connect"], help="join the voice channel that you are currently on")
    @check_channel()
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        voice = get(self.bot.voice_clients)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await ctx.send(f"Joined {channel}")

    @join.error
    async def join_error(self, ctx, error):
        await ctx.message.delete(delay=10)
        if isinstance(error, commands.CheckFailure):
            temp = await ctx.send("please use this command in the #music or #bot-commands channel")
            await temp.delete(delay=10)
        if isinstance(error, commands.CommandInvokeError):
            temp = await ctx.send("You need to be in a voice channel first")
            await temp.delete(delay=10)

        raise error

    @commands.command(aliases=["disconnect"], help="the bot leave the current voice channel that its on")
    @check_channel()
    async def leave(self, ctx):
        voice = get(self.bot.voice_clients)
        channel = voice.channel

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f"Left {channel}")

    @leave.error
    async def leave_error(self, ctx, error):
        await ctx.message.delete(delay=10)
        if isinstance(error, commands.CheckFailure):
            temp = await ctx.send("please use this command in the #music or #bot-commands channel")
            await temp.delete(delay=10)
        if isinstance(error, commands.CommandInvokeError):
            temp = await ctx.send("currently not in a voice channel")
            await temp.delete(delay=10)

        raise error

    @commands.command(aliases=["p"])
    @check_channel()
    async def play(self, ctx, *, url):

        def check_queue():
            queue_folder = os.path.isdir("./Queue")
            if queue_folder:
                queue_abspath = os.path.abspath(os.path.realpath("Queue"))
                queue_length = len(os.listdir(queue_abspath))

                try:
                    first = os.listdir(queue_abspath)[0]
                except:
                    return

                curr_path = os.path.dirname(__file__)
                main_path = os.path.join(curr_path, "..")
                song_path = os.path.abspath(
                    os.path.realpath("Queue") + "\\" + first)

                if queue_length != 0:
                    song = os.path.isfile("testing.mp3")
                    if song:
                        os.remove("testing.mp3")

                    shutil.move(song_path, main_path)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file, "testing.mp3")

                    voice.play(discord.FFmpegPCMAudio(
                        "testing.mp3"), after=lambda _: check_queue())
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 1
                    #print("At check")
                else:
                    return

        song = os.path.isfile("testing.mp3")
        if song:
            os.remove("testing.mp3")

        voice = get(self.bot.voice_clients)
        if voice and voice.is_connected():
            channel = voice.channel

            try:
                user_channel = ctx.author.voice.channel
            except AttributeError:
                user_channel = channel

            if channel != user_channel:
                await voice.move_to(user_channel)
                await ctx.send(f"Joined {user_channel}")
        else:
            user_channel = ctx.author.voice.channel
            voice = await user_channel.connect()
            await ctx.send(f"Joined {user_channel}")

        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        await ctx.send("Getting ready ...")
        yt_pattern = r"^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+"
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            if re.match(yt_pattern, url):
                ydl.download([url])
                info = ydl.extract_info(url, download=False)
                title = info['title']
            else:
                command = ["youtube-dl", "--get-id", "-e", "ytsearch:" + url]
                result = subprocess.run(command, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, universal_newlines=True).stdout.split("\n")
                # print(result)
                ydl.download([result[1]])
                title = result[0]

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "testing.mp3")

        voice.play(discord.FFmpegPCMAudio("testing.mp3"),
                   after=lambda e: check_queue())
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 1

        await ctx.send(f"Playing    :play_pause:   {title}   :musical_note:")
        # print("At play")

    @play.error
    async def play_error(self, ctx, error):
        await ctx.message.delete(delay=10)
        if isinstance(error, commands.CheckFailure):
            temp = await ctx.send("please use this command in the #music or #bot-commands channel")
            await temp.delete(delay=10)
        # In-Progress: to add song to the queue instead of throwing error here
        if isinstance(error, commands.CommandInvokeError):
            temp = await ctx.send("crrently busy. Please requests later")
            await temp.delete(delay=10)
        if isinstance(error, commands.MissingRequiredArgument):
            temp = await ctx.send("please specify of what you want to play")
            await temp.delete(delay=10)

        raise error

    @commands.command()
    @check_channel()
    async def pause(self, ctx):
        await ctx.message.delete(delay=10)
        voice = get(self.bot.voice_clients)

        if voice and voice.is_playing():
            voice.pause()
            await ctx.send("Paused  :pause_button:")
        else:
            temp = await ctx.send("Music is not playing")
            await temp.delete(delay=10)

    @pause.error
    async def pause_error(self, ctx, error):
        await ctx.message.delete(delay=10)
        if isinstance(error, commands.CheckFailure):
            temp = await ctx.send("please use this command in the #music or #bot-commands channel")
            await temp.delete(delay=10)

        raise error

    @commands.command()
    @check_channel()
    async def resume(self, ctx):
        await ctx.message.delete(delay=10)
        voice = get(self.bot.voice_clients)

        if voice and voice.is_paused():
            voice.resume()
            await ctx.send("Resumed   :play_pause:")
        else:
            temp = await ctx.send("Music is not paused")
            await temp.delete(delay=10)

    @resume.error
    async def resume_error(self, ctx, error):
        await ctx.message.delete(delay=10)
        if isinstance(error, commands.CheckFailure):
            temp = await ctx.send("please use this command in the #music or #bot-commands channel")
            await temp.delete(delay=10)

        raise error

    @commands.command()
    @check_channel()
    async def stop(self, ctx):
        await ctx.message.delete(delay=10)
        voice = get(self.bot.voice_clients)

        queue_folder = os.path.isdir("./Queue")
        if queue_folder:
            shutil.rmtree("./Queue")

        if voice and voice.is_playing():
            voice.stop()
            await ctx.send("Stop  :stop_button:")
        else:
            temp = await ctx.send("No music is playing")
            await temp.delete(delay=10)

    @stop.error
    async def stop_error(self, ctx, error):
        await ctx.message.delete(delay=10)
        if isinstance(error, commands.CheckFailure):
            temp = await ctx.send("please use this command in the #music or #bot-commands channel")
            await temp.delete(delay=10)

        raise error

    @commands.command(aliases=["q"])
    @check_channel()
    async def queue(self, ctx, *, url):
        queue_folder = os.path.isdir("./Queue")
        if queue_folder is False:
            os.mkdir("Queue")

        queue_abspath = os.path.abspath(os.path.realpath("Queue"))
        num = len(os.listdir(queue_abspath))
        num += 1

        song_path = os.path.abspath(os.path.realpath(
            "Queue") + f"\\testing{num}.%(ext)s")

        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "outtmpl": song_path,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        await ctx.send("Adding ...")
        yt_pattern = r"^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+"
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            if re.match(yt_pattern, url):
                ydl.download([url])
                info = ydl.extract_info(url, download=False)
                title = info['title']
            else:
                command = ["youtube-dl", "--get-id", "-e", "ytsearch:" + url]
                result = subprocess.run(command, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, universal_newlines=True).stdout.split("\n")
                print(result)
                ydl.download([result[1]])
                title = result[0]

        await ctx.send(f"Added   :musical_note:   {title}   :musical_note:   to the queue")
        # print("At queue")

    @queue.error
    async def queue_error(self, ctx, error):
        await ctx.message.delete(delay=10)
        if isinstance(error, commands.CheckFailure):
            temp = await ctx.send("please use this command in the #music or #bot-commands channel")
            await temp.delete(delay=10)
        if isinstance(error, commands.MissingRequiredArgument):
            temp = await ctx.send("please specify of what you want to add to the queue")
            await temp.delete(delay=10)

        raise error

    @commands.command(aliases=["next"])
    @check_channel()
    async def skip(self, ctx):
        await ctx.message.delete(delay=10)
        voice = get(self.bot.voice_clients)

        if voice and voice.is_playing():
            voice.stop()
            await ctx.send("Skipped  :fast_forward:")
        else:
            temp = await ctx.send("No music is playing")
            await temp.delete(delay=10)

    @skip.error
    async def skip_error(self, ctx, error):
        await ctx.message.delete(delay=10)
        if isinstance(error, commands.CheckFailure):
            temp = await ctx.send("please use this command in the #music or #bot-commands channel")
            await temp.delete(delay=10)

        raise error


def setup(bot):
    bot.add_cog(music(bot))
