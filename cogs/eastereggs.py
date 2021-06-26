from discord.ext import commands, tasks
import discord
import random
import logging
import pickle
import asyncio
from datetime import datetime
logger = logging.getLogger('bot')



from discord import Embed
class easterEggs(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot
        self.utility = self.bot.get_cog("utility")

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.author != self.bot.user:
                sentence = message.content.lower()
                if "<@!384444248214208522>" in message.content:
                    await message.channel.send("Hello {}!".format(message.author.mention))
                if isinstance(message.channel, discord.DMChannel):
                    brooke = 243887352022433792
                    test = 339866237922181121
                    if message.author.id == brooke or message.author.id == test:
                        
                        if sentence == "give me a reason":
                            
                            with open('reasons.txt', 'rb') as f:
                                reasonsILoveBrooke = pickle.load(f)
                            randomReason = random.choice(reasonsILoveBrooke)                        
                            await message.channel.send('One thing Nana loves about you is he loves:\n\n"{}"'.format(randomReason))
                            logger.critical("Sent reason: '{}'".format(randomReason))
                            print("Sent reason: '{}'".format(randomReason))
                            return
                    sentence = message.content.lower()  # So that we can work with one case
                    if (
                        message.content == "raise-exception"
                    ):  # If discord wants us to raise an exception we do it. Never disobey the discord overlords. Ever.
                        raise discord.DiscordException

                    # checks if the message is not the bot so it doesnt process its own message.
                if sentence == "oh? so you're approaching me?" or sentence == "oh? so youre approaching me":  # if this is the message we
                    await message.channel.send(
                        "I can't beat the shit out of you without getting closer."
                    )
                    return

                # This function splits sentences into list like so > ["this", "is", "a,", "sentence"]
                thisList = sentence.split()
                prankOp = False
                for x in range(len(thisList)):
                    # this combs through the list looking for the words "Im" or "I'm" and identifies where it is in the sentence
                    if thisList[x] == "i'm" or thisList[x] == "im":
                        pointer = x
                        prankOp = True
                    # this does the same thing but looks for the words "I" and "am" in consecutive positions
                    elif thisList[x] == "i" and thisList[x + 1] == "am":
                        pointer = x + 1
                        prankOp = True
                if (
                    not str(message.guild.id) in self.utility.botSettings
                ):  # We first have to converth the guild id into a string since json converts all dict keys to strings
                    self.utility.botSettings[
                        str(message.guild.id)
                    ] = (
                        {}
                    )  # If the guild does not have any settings for the bot we create a new entry in the dictionary in the guild with custom settings
                    for k, v in self.utility.defaultSettings.items():
                        self.utility.botSettings[str(message.guild.id)][k] = v
                if (
                    prankOp == True
                    and self.utility.botSettings[str(message.guild.id)]["dadJoke"] == True
                ):
                    del thisList[0 : pointer + 1]
                    if (
                        len(thisList) > 5
                    ):  # If there are more than 5 words after "I am" or "im" we just ignore the rest since the joke wouldnt work if there is a whole paragraph after I am
                        pass
                    else:
                        themessage = " "
                        for y in range(len(thisList)):

                            if y != len(thisList) - 1:
                                # Adding the words after "I am" or "im" into an empty string with the " " as a space.
                                themessage += thisList[y] + " "
                            else:
                                themessage += thisList[y]

                        await message.channel.send("Hi{}, I'm Dad :)".format(themessage))
                if "ora" in sentence:
                    oraList = sentence.split()
                    ora = True
                    for x in oraList:
                        if x != "ora":
                            ora = False
                    if ora:
                        oraReply = ""
                        for x in range(len(oraList)):
                            oraReply += "Muda! "
                        await message.channel.send(oraReply)
                if "ora!" in sentence:
                    oraList = sentence.split()
                    ora = True
                    for x in oraList:
                        if x != "ora!":
                            ora = False
                    if ora:
                        oraReply = ""
                        for x in range(len(oraList)):
                            oraReply += "Muda! "
                        await message.channel.send(oraReply)
                if "muda" in sentence:
                    mudaList = sentence.split()
                    muda = True
                    for x in mudaList:
                        if x != "muda":
                            muda = False
                    if muda:
                        mudaReply = ""
                        for x in range(len(mudaList)):
                            mudaReply += "Ora! "
                        await message.channel.send(mudaReply) 
                if "muda!" in sentence:
                    mudaList = sentence.split()
                    muda = True
                    for x in mudaList:
                        if x != "muda!":
                            muda = False
                    if muda:
                        mudaReply = ""
                        for x in range(len(mudaList)):
                            mudaReply += "Ora! "
                        await message.channel.send(mudaReply)  
        except:
          pass



    @commands.Cog.listener()
    async def on_ready(self): 
        self.utility = self.bot.get_cog("utility")
        print("Easter eggs has been loaded")

        
     
def setup(bot):
    bot.add_cog(easterEggs(bot))
    