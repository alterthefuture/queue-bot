from discord.ext import commands
import discord

import motor.motor_asyncio
from pathlib import Path
import json
import os

from util.mongo import Document

cwd = Path(__file__).parents[0]
cwd = str(cwd)

async def get_prefix(client,message):
    if not message.guild:
        return commands.when_mentioned_or(";")(client,message)

    try:
        data = await client.config.find(message.guild.id)

        if "prefix" not in data:
            return commands.when_mentioned_or(";")(client,message)
        return commands.when_mentioned_or(data['prefix'])(client,message)
    except:
        return commands.when_mentioned_or(";")(client,message)

intents=discord.Intents.all()
secret_file = json.load(open(cwd+'/secrets.json'))

bot = commands.Bot(command_prefix=get_prefix,intents=intents,case_insensitive=True)
bot.remove_command(name="help")

bot.config_token = secret_file['token']
bot.connection_url = secret_file['mongo']

@bot.event
async def on_ready():
    print("Bot is online.")

    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(bot.connection_url))
    bot.db = bot.mongo['luxa']

    bot.config = Document(bot.db,'config')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(bot.config_token)