# simple discord bot
import discord
import os

from api import getEmotion, getGif, getKeywordFromMessage

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

DISCORD_KEY = os.getenv("DISCORD_KEY")

bot = commands.Bot(command_prefix='%')


# print when bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_message(message):
    # CHECK IF THE MESSAGE SENT TO THE CHANNEL IS "HELLO".
    if message.content == "hello":
        # SENDS A MESSAGE TO THE CHANNEL.
        await message.channel.send("pies are better than cakes. change my mind.")

    # INCLUDES THE COMMANDS FOR THE BOT. WITHOUT THIS LINE, YOU CANNOT TRIGGER YOUR COMMANDS.
    await bot.process_commands(message)


@bot.command()
async def react(ctx):
    message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    # emotion = getEmotion(message.content)

    # {'emotion': {'Happy': 0.2648372342, 'Excited': 0.1429308198, 'Angry': 0.1006374564, 'Fear': 0.1902021548, 'Sad': 0.1344127347, 'Bored': 0.1669796001}}
    # get the highest probability
    # emotion = sorted(emotion.items(), key=lambda x: x[1])
    # emotion = emotion[-1][0]

    keyword = getKeywordFromMessage(message.content)

    gif = getGif(keyword)

    print(keyword)
    await ctx.send(gif)


bot.run(DISCORD_KEY)
