import json
from discord.ext import commands, tasks
import configparser
from datetime import datetime
import asyncio
import logging
#############SETTINGS#############
logger = logging.getLogger("bot")
class utility(commands.Cog):

    def __init__(self, bot): 
        self.bot = bot
        self.colour = 0x34ebc6
        self.boturl = "https://cdn.discordapp.com/avatars/384444248214208522/b24bf5966af80bc9de1e148c4a28a911.png"
        self.botSettings = {}  # Will be a dictionary of server settings
        self.userBirthdays = {}  # Will be a dictionary of users birthdays
        self.events = {}
        self.defaultSettings = {  # defines the default setting dictionary
            "dadJoke": True,
            "potd": False,
            "potdHour": 16,
            "potdRole": None,  # None variables will have no value until we set them (so we are basically declaring them)
            "potdMinRole": None,
            "potdAnnouncementChannel": None,
            "potdCustomMessage": None,
            "lastPotd": None,
            "birthdayAnnouncements": False,
            "birthdayAnnouncementChannel": None,
            "birthdayCustomMessage": None,
        }
        self.birthdayDict = {"birthday": None}
        
        self.parse.start() 
        self.backUp.start()

    # reading the setting.json file to get settings
        with open("resources/memberdata.json", "r") as file:
            self.memberData = json.load(file)
        with open("resources/settings.json", "r") as file:
            self.botSettings = json.load(file)
        with open("resources/birthdays.json", "r") as file:
            self.userBirthdays = json.load(file)
        with open("resources/events.json", "r") as file:
            self.events = json.load(file)
  

      

    @tasks.loop(seconds=5)  # Backs up settings every 5 seconds (will increase if there are more guilds so lag can be decreased)
    async def backUp(self):

        await self.bot.wait_until_ready()
        now = datetime.utcnow()
        with open("resources/settings.json", "w") as f:  # Opens setting.json in write mode
            self.botSettings["last-updated"] = f"{now.day}/{now.month} at {now.hour}:{now.minute}:{now.second}"
            
            json.dump(self.botSettings, f)  # writes the current settings into it

        with open("resources/birthdays.json", "w") as f:
            self.userBirthdays["last-updated"] = f"{now.day}/{now.month} at {now.hour}:{now.minute}:{now.second}"
            
            json.dump(self.userBirthdays, f)
        with open("resources/memberdata.json", "w") as f:
            self.memberData["last-updated"] = f"{now.day}/{now.month} at {now.hour}:{now.minute}:{now.second}"
            
            json.dump(self.memberData, f)
        with open("resources/events.json", "w") as f:
            json.dump(self.events, f)
    @backUp.before_loop
    async def before_backUp(self):
        await self.bot.wait_until_ready()
            

    
    @tasks.loop(minutes = 10)
    async def parse(self):
        await self.bot.wait_until_ready()
        guildIds = [str(x.id) for x in self.bot.guilds]
        try:
            for k, v in self.botSettings.items():
                if k not in guildIds:
                    del self.botSettings[str(k)]
                    logger.debug("Parsed {} settings".format(k))
            for k, v in self.userBirthdays.items():
                if str(k) not in guildIds:
                      del self.userBirthdays[str(k)]
                      logger.debug("Parsed {} birthdays".format(k))
        except RuntimeError as e:
            logger.debug(e)
              
            

    #@commands.Cog.listener()
    #async def on_command_error(self, ctx, error):
        #pass
    @commands.Cog.listener()
    async def on_ready(self): 
        print("\n\n==============================\nUtility cog has been loaded")


def setup(bot):

    bot.add_cog(utility(bot))