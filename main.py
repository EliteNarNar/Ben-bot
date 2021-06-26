import configparser
import discord
import json
import asyncio
import os
import sys
from datetime import datetime
from discord.ext import commands, tasks
from discord import Embed
from dotenv import load_dotenv
import subprocess
import logging
import logging.handlers

testing = True


intents = discord.Intents.all()  # required to work with server members
intents.members = True
intents.reactions = True

# Its nice to keep your alterable variables in a config file so users can edit the bot to their need without having to alter the code.
config = configparser.ConfigParser()
config.read("resources/config.ini")
load_dotenv()
# We store the TOKEN in a .env file since it is secret and if anyone gains access to it they can control the bot (.env files are usually ignored in most code sharing services
if not testing:
	TOKEN = os.getenv("DISCORD_TOKEN")
        



else:
        TOKEN = os.getenv("TEST_TOKEN")
        bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)  


# the object bot represents our connection to discord

def setupLogging():
	logger = logging.getLogger('bot')
	logger.setLevel(logging.DEBUG)

	handler = logging.handlers.TimedRotatingFileHandler(
	    filename='logs/bot.log',
	    when='h',
	    interval=8,
	    backupCount=3,
	    encoding='utf-8')
	handler.setFormatter(
	    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
	logger.addHandler(handler)


@bot.event
async def on_message(message):
	logger = logging.getLogger('bot')
	try:
		await bot.process_commands(message)
	except Exception as e:
		logger.debug(f"Error while processing commands: {e}")


def loadExtensions():
	logger = logging.getLogger('bot')

	startupExtensions = config["cogs"]
	logger.debug("Brooke bot starting...")
	for extension in startupExtensions:
		try:
			bot.load_extension("cogs." + extension)
		except Exception as e:
			logger.critical("Failed to load {} extension\n".format(extension))
			logger.critical(e)
			print(e)
	print("Loaded Cogs")


setupLogging()
loadExtensions()


bot.run(TOKEN)
