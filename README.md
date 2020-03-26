# Discord-bot

A bot that can interact with the user commands.

---

## Youtube Music/Audio

users enter a youtube link or enter their normal youtube-search, then the bot will play the audio from that inputs. The users can pause and resume the audio. The users can also add a new audio to a queue (playlist), which the bot will play them after it finishes the current the audio. The users can skip the current audio, then the bot will play the next audio from the queue.

**Note**: The user can only use these commands in the **#music** or **#bot-commands** text-channel only. Create one if you do not have it already.

- `~play`: Enters your search or youtube link here, then the bot will play the audio for you.
- `~pause`: Pauses the current audio.
- `~resume`: resumes the paused audio.
- `~queue`: Enters your search or youtube link here (just like `~play` command), the bot will add it to a queue. After the bot finished its current audio, it will play the next audio in the queue.
- `~skip`: skips the current audio, play the next one in the queue.
- `~stop`: stops playing the audio. (the queue will be clear)
- `~join`: tells the bot to join your voice channel
- `~leave`: tells the bot to leave the voice channel

---

## Search Image

users enter their search-terms, then the bot will post an image based on that input. The results will be different each time for the same searching. (randomize from a poll of results)

**Note**: The user can only use the command in the **#bot-commands** text-channel only. Create one if you do not have it already.

- `~image`: Enter your search here. The bot will post an image relevant to your search. Use this command again if you do not like the current result. The bot will give you a new one.

---

## Mini-games/Fun

Just some simple games for the users to play with.

**Note**: The user can only use the command in the **#bot-commands** text-channel only. Create one if you do not have it already.

- `~8ball`: Ask the bot a question, it will reply. Answers might vary. (https://en.wikipedia.org/wiki/Magic_8-Ball)
- `~fortune`: Give you a random fortune-cookie quote. (from a list of 839 quotes)

---

## Others/Misc.

Other simple commands:

- `~clear`: tells the bot how many messages you want to be deleted. Useful for cleaning the chat/channel.
- `~date`: returns the current time and date.

---

## In-Progress:

- Automatically adding the new audio to the queue using `~play` command.
- Add more features.
