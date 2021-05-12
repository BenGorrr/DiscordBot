# -*- coding: utf-8 -*-
import discord, asyncio, os, time, random
from discord.ext import commands
import config
from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

bot = commands.Bot(command_prefix = '.')

def isBen(ctx):
    return ctx.author.id == 171175305036300299
def is_bot(ctx):
    return ctx.author == bot.user

@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))

bot.engine = create_engine(DATABASE_URL, pool_pre_ping=True)
Base.metadata.create_all(bot.engine)
bot.Session = sessionmaker(bind=bot.engine)

bot.load_extension("CogManager")
bot.load_extension("main")
bot.load_extension("r6stats")
bot.load_extension("lyrics")
bot.load_extension("classes")
bot.load_extension("images")
bot.load_extension("keywords")
bot.run(os.environ.get('DISCORD_KEY', '-1'))
