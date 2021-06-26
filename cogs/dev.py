
owner = 339866237922181121
import discord
from discord import Embed
from discord.ext import commands
import sys
import logging
import main
import asyncio
import json
import pytz
import configparser
logger = logging.getLogger('bot')
config = configparser.ConfigParser()
config.read("resources/config.ini")
cogList = config["cogs"] # A list of all cognames
patchNotes = config["version"]["patchNotes"] # the patchNotes
version = config["version"]["version"] # The version
class Dev(commands.Cog):

    def __init__(self, bot):
        self.bot = bot # When we use classes we have to redifine bot as self.bot so we can uses it
        self.utility = self.bot.get_cog("utility") # This allows us to use our databases
        self.potd = self.bot.get_cog("potd")
        self.platforms = self.bot.get_cog("platforms")
        self.commands = self.bot.get_cog("birthdays")
        self.colour = self.utility.colour
    @commands.Cog.listener()
    async def on_ready(self): 
        print("Dev cog has been loaded") 


    @commands.command(name = "load", hidden = True)
    async def _load(self, ctx, ext: str):
        if ctx.author.id == owner: # So only I can use it
          try:
              self.bot.load_extension("cogs." + ext) #cogs.<cogname> is the format
              await ctx.channel.send("Loaded {} extension".format(ext))
          except Exception as e:
              await ctx.channel.send(e) # Tells us the error

    @commands.command(name = "unload", hidden = True)
    async def _unload(self, ctx, ext: str):
        if ctx.author.id == owner: #So only I can use it
            try:
                self.bot.unload_extension("cogs." + ext)
                await ctx.channel.send("Unloaded {} extension".format(ext))
            except Exception as e:
                await ctx.channel.send(e)
    @commands.command(name = "reload", hidden = True)
    async def _reload(self, ctx, ext: str):
  
        if ctx.author.id == owner:
            with open("resources/memberdata.json", "r") as file:
                self.memberData = json.load(file)
            with open("resources/settings.json", "r") as file:
                self.botSettings = json.load(file)
            with open("resources/birthdays.json", "r") as file:
                self.userBirthdays = json.load(file)             
            try:
                await asyncio.sleep(1)
                self.bot.reload_extension("cogs." + ext)
                await ctx.channel.send("Reloaded {} extension".format(ext))
            except Exception as e:
                await ctx.channel.send(e)
    
    @commands.command(name = "reloadall", hidden = True)
    async def _reloadall(self, ctx):
        if ctx.author.id == owner:
            with open("resources/memberdata.json", "r") as file:
                self.memberData = json.load(file)
            with open("resources/settings.json", "r") as file:
                self.botSettings = json.load(file)
            with open("resources/birthdays.json", "r") as file:
                self.userBirthdays = json.load(file)          
                embed = discord.Embed(title="Bot cogs:", colour=self.colour) # defines an embed
                counter = 0
            for ext in cogList:
                try:
                    self.bot.reload_extension("cogs." + ext) # WIll load the cog
                    embed.add_field(name=ext+".py", value= "This cog has been loaded succesfully",inline=False) # Then it will add a field with saying that this has been loaded succesfully
                    counter+=1 #imcrements the counter
                except Exception as e:
                    embed.insert_field_at(0, name=ext+".py  **ERROR**", value=e,inline=False) # If there is an error we will put it at the top and the description will be the error
            if counter < 7:
                embed.color =self.colour #If not all cogs have been loaded we will make the color yellow
            if counter == 0:
                embed.color = self.colour #If all cogs have not been loaded we make it red.
            await ctx.channel.send(embed=embed) #sends the embed



    @commands.command(name = "loadall", hidden = True)                
    async def _loadall(self, ctx):
        if ctx.author.id == owner:
            counter = 0
            embed = discord.Embed(title="Bot cogs:", colour=self.colour)
            for ext in cogList:
                try:
                    self.bot.load_extension("cogs." + ext)
                    embed.add_field(name=ext+".py", value = "This cog has been loaded succesfully",inline=False)
                    counter+=1
                except Exception as e:
                    embed.insert_field_at(0, name=ext+".py  **ERROR**", value=e,inline=False)
            if counter < 7:
                embed.color = self.colour
            
            if counter == 0:
                embed.color = self.colour
            await ctx.channel.send(embed=embed)


    @commands.command(name = "unloadall", hidden = True)
    async def _unloadall(self, ctx):
        if ctx.author.id == owner:
            counter = 0
            embed = discord.Embed(title="Bot cogs:", colour=self.colour)
            for ext in cogList:
                try:
                    if ext != "dev":
                        self.bot.unload_extension("cogs." + ext)
                        embed.add_field(name=ext+".py", value= "This cog has been unloaded succesfully",inline=False)
                        
                        counter+=1   
                except Exception as e:
                    embed.insert_field_at(0, name=ext+".py  **ERROR**", value=e,inline=False)
            if counter < 6:
                embed.color = self.colour
            
            if counter == 0:
                embed.color = self.colour          
            await ctx.channel.send(embed=embed)

    @commands.command(name = "shutdown", hidden = True)
    async def _shutdown(self, ctx):
        if ctx.author.id == owner:
            await ctx.channel.send("Bot shutting down...")
            sys.exit()
    @commands.command(name ="announce", hidden = True)
    async def _announce(self, ctx, channelId, everyone=None):
        if ctx.author.id == owner:
            patch = patchNotes.replace('\\n', '\n\n') # replaces \\n with two new lines 
            embed= discord.Embed(title="New patch!", colour=self.colour)
            embed.add_field(name="Patch-Notes ({})".format(version), value=patch+"\n\nThanks for using Ben-Bot!")
            embed.set_footer(text="Ben-bot | EliteNarNar#3447")
            embed.set_thumbnail(url=self.utility.boturl)
            channel = ctx.guild.get_channel(int(channelId))
            if everyone == "1":
                await channel.send("@everyone",embed=embed)
            if everyone == "0":
                await channel.send(embed=embed)
    @commands.command(name ="listguilds", hidden = True)
    async def _listGuilds(self, ctx):
        if ctx.author.id == owner:
          await ctx.channel.send(self.bot.guilds)
    @commands.command(name="diagnostics", hidden = True)
    async def _diagnostics(self, ctx):
        if ctx.author.id == owner:
            await ctx.send(f"Diagnostics!\nMemberData\n```{self.utility.memberData} ```\nEvents\n{self.utility.events}")
            print(self.bot.get_guild(810318689584545863).name)
    @commands.command(name="command")
    async def command(self, messageOwner):
        guild = self.bot.get_guild(810318689584545863)
        await guild.owner.create_dm()
        for member in guild.members:
            print(member.name)
        
  
    @commands.command(name ="status", hidden = True)
    async def _status(self, ctx, status,*, thing=None):
        if ctx.author.id == owner:
            activity = None
            if status == "listen":
                activity=discord.Activity(type=discord.ActivityType.listening, name=thing)
                act = "Listening to"
            elif status == "watch":
                act = "Watching"
                activity=discord.Activity(type=discord.ActivityType.watching, name=thing)
            elif status == "game":
                act = "Playing"
                activity=discord.Game(name=thing)
            elif status == "me":
                await ctx.send(f"activity is {ctx.author.activity}")
                return
        await self.bot.change_presence(activity=activity)
        logger.debug(act+" "+thing)
        await ctx.channel.send('Status changed to "{0} {1}"'.format(act, thing))
    @commands.command(name="message", hidden=True)   
    async def messageCommand(self, ctx, id,*,message):
        if ctx.author.id ==owner:
            try:
                recipient = self.bot.get_user(int(id))
            except:
                await ctx.send("NO")
            
            await recipient.create_dm()
            await recipient.dm_channel.send(message)



def setup(bot):
    bot.add_cog(Dev(bot))