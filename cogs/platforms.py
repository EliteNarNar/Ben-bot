import discord
from discord.ext import commands, tasks

import re
import asyncio
import json
from datetime import datetime
import pytz
from pytz import timezone
import logging

logger = logging.getLogger('bot')

class Platform(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utility = self.bot.get_cog("utility")
        self.colour = self.utility.colour
    @commands.Cog.listener()
    async def on_ready(self):
        print("Platforms cog Loaded!")
    

                
    @commands.command(name="addplatform")
    async def setPlatformCommand(self, ctx, platform=None, member: discord.Member=None):
        if platform is None:
            await ctx.send("You haven't specified a platform")
            return
        user = ctx.author
        if ctx.author.guild_permissions.administrator and member is not None:
            user = member
        
        async def waitForMessage():
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:             
                message = await self.bot.wait_for('message', timeout=60, check=check)
            except asyncio.TimeoutError:
                await ctx.send("Timed out.")
            return message.content
        platform = platform.lower()
        if str(ctx.guild.id) not in self.utility.memberData.keys():
            self.utility.memberData[str(ctx.guild.id)] = {}
        if str(user.id) not in self.utility.memberData[str(ctx.guild.id)].keys():
            self.utility.memberData[str(ctx.guild.id)][str(user.id)] = {"platforms": {}}  
        guildData = self.utility.memberData[str(ctx.guild.id)]     
        if platform == "xbox":
            await ctx.send("What type of Xbox do you have?")
            embed = discord.Embed(title="Types of Xbox", description="**Xbox** (2001)\n**Xbox 360** (2006)\n**Xbox 360 S** (2010)\n**Xbox 360 E** (2010)\n**Xbox One** (2013)\n**Xbox One S** (2016)\n**Xbox One X** (2017)\n**Xbox Series X** (2020)\n**Xbox series S** (2020)", colour=0x2ec700)
            await ctx.send(embed=embed)
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:             
                message = await self.bot.wait_for('message', timeout=60, check=check)
            except asyncio.TimeoutError:
                await ctx.send("Timed out.")
            message = message.content.lower()
            if message in ["xbox", "xbox 360", "xbox 360 s", "xbox 360 e","xbox one", "xbox one s", "xbox one x", "xbox series x", "xbox series s"]:
                guildData[str(user.id)]["platforms"]["Xbox"] = message.title()
                await ctx.send(f"Added xbox as a platform and {message.title()} as your console!")
            else:
                await ctx.send("Invalid console!")

            
              
        elif platform == "playstation" or platform == "ps":
            await ctx.send("What type of Playstation do you have?")
            embed = discord.Embed(title="Types of Playstation", description="**Playstation** (2000)\n**Playstation 2** (2000)\n**Playstation 3** (2006)\n**Playstation 4** (2013)\n**Playstation 4 Slim** (2016)\n**Playstation 4 Pro** (2016)\n**Playstation 5** (2020)", colour=0x3072ff)
            await ctx.send(embed=embed)
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:             
                message = await self.bot.wait_for('message', timeout=60, check=check)
            except asyncio.TimeoutError:
                await ctx.send("Timed out.")
                pass
            message = message.content.lower()
            if message in ["playstation", "psone", "playstation 2", "ps2", "playstation 3", "ps3", "playstation 4", "ps4", "playstation 5", "ps5"]:
                if message == "psone":
                    message = "playstation 1"                            
                elif message == "ps2":
                    message = "playstation 2"                        
                elif message == "ps3":
                    message = "playstation 3"                        
                elif message == "ps4":
                    message = "playstation 4"                        
                elif message == "ps5":
                    message = "playstation 5"                        


                guildData[str(user.id)]["platforms"]["PlayStation"] = message.title()
                await ctx.send(f"Added PlayStation as a platform and {message.title()} as your console!")
            else:
                await ctx.send("Invalid console!")
        elif platform == "pc" or platform == "windows" or platform == "mac" or platform == "MacOS":
            self.utility.memberData[str(ctx.guild.id)][str(user.id)]["platforms"]["PC"] = {}
            await ctx.send("What would you like to name your pc/laptop")
            pcSpecs = self.utility.memberData[str(ctx.guild.id)][str(user.id)]["platforms"]["PC"]
            pcSpecs["Name"]= await waitForMessage()
            await ctx.send("What is operating system?")
            pcSpecs["Operating System"] = await waitForMessage()
            if pcSpecs["Operating System"].lower() in ["macOS", "mac", "apple"] or "mac" in pcSpecs["Operating System"].lower(): 
                await ctx.send("What Model is your Mac?")
                pcSpecs["Model"] = await waitForMessage()

            await ctx.send("What is the model of your processor?")
            pcSpecs["Processor"] = await waitForMessage()
            await ctx.send("How much ram do you have (you can add the type if you'd like)")
            pcSpecs["RAM"] = await waitForMessage()
            await ctx.send("What graphics card do you have? You can type None if you'd like")
            pcSpecs["Graphics Card"] = await waitForMessage()
            await ctx.send("What motherboard do you have? Type skip if you dont want to include it")
            message = await waitForMessage()
            if message.lower() == "skip":
                pass
            else:
                pcSpecs["Motherboard"] = message
            
            string = ""
            embed = discord.Embed(title=f"{user.name}'s specs have been set to:", colour=0x339931)
            for k, v in guildData[str(user.id)]["platforms"]["PC"].items():
                string+= f"**{k}:** {v}\n"  
            embed.description = string     
            await ctx.send(embed=embed) 
        elif platform == "vr":
            await ctx.send("What is the model of your VR headset?")       
            message = await waitForMessage()
            self.utility.memberData[str(ctx.guild.id)][str(user.id)]["platforms"]["VR"] = message.title()
            await ctx.send(f"Added Virtual Reality as a platform and {message.title()} as your console!")               
        elif platform == "switch":
            await ctx.send("Do you have a Nintendo Switch or a Nintendo Switch Lite?")
            message = await waitForMessage()
            message = message.lower()
            if message in ["nintendo switch", "nintendo switch lite"]:
            
                self.utility.memberData[str(ctx.guild.id)][str(user.id)]["platforms"]["Switch"] = message.title()
                await ctx.send(f"Added Nintendo Switch as a platform and {message.title()} as your console!")
            else:
              await ctx.send("Invalid console!")
        with open("resources/memberdata.json", "w") as f:
            json.dump(self.utility.memberData, f)
            
    @commands.command(name="delplatform")
    async def delPlatformCommand(self, ctx, platform=None, member: discord.Member=None):
        if platform is None:
            await ctx.send("You haven't provided a platform!")
            return
        person = ctx.author
        if member is not None:
            person = member

        
        else:
            memberPlat = self.utility.memberData[str(ctx.guild.id)][str(person.id)]["platforms"]
            try:
              if platform.lower() == "PC":
                  del memberPlat["PC"]
                  await ctx.send("You have deleted PC as a platform")
              platform = platform.lower()
              if platform == "playstation":
                  del memberPlat["PlayStation"]
                  await ctx.send("You have deleted PlayStation as a platform")
              elif platform == "switch":
                  del memberPlat["Switch"]
                  await ctx.send("You have deleted Switch as a platform")

              elif platform == "Xbox":
                  del memberPlat["Xbox"] 
                  await ctx.send("You have deleted Xbox as a platform")
              elif platform == "vr":
                  del memberPlat["VR"]
                  await ctx.send("You have deleted VR as a platform")
              with open("resources/memberdata.json", "w") as f:
                  json.dump(self.utility.memberData, f)
              
            except Exception as e:
                await ctx.send("You haven't added this platform")
                print(e)
    @commands.command(name="platforms") 
    async def platformCommand(self, ctx, guy: discord.Member=None, platform=None):
      
        if guy is None:
            guy = ctx.author 
      
        if str(ctx.guild.id) not in self.utility.memberData.keys():
            self.utility.memberData[str(ctx.guild.id)] = {}
       
        if str(guy.id) not in self.utility.memberData[str(ctx.guild.id)].keys():
            await ctx.send("This member has not set any platforms ")
        memberPlatforms = self.utility.memberData[str(ctx.guild.id)][str(guy.id)]["platforms"]
        
        memberPlats = [[platform, info] for platform, info in memberPlatforms.items()]
        embed = discord.Embed(title=f"{guy.name}'s platforms")
        for x in memberPlats:
              
              if x[0] == "PC":
                  string = ""
                  for k, v in x[1].items():
                    string+= f"**{k}:** {v}\n"
                  if x[0] == "PC":
                      embed.add_field(name="PC", value =string)

                  
              else:     
                  embed.add_field(name=x[0], value =f"**Console:** {x[1]}",inline=False)
        
        embed.colour = self.colour
        
        await ctx.send(embed=embed)
    @commands.command(name="listplatforms")
    async def listPlatformsCommand(self, ctx, platform=None, page=None):
        platform = platform.lower()
        if platform is None:
            await ctx.send("You haven't specified a platform!")
        if page is None:
            page = 1
        if platform == "playstation":
            await self.listPlatforms(ctx=ctx, platform="PlayStation", page=page)
        if platform == "xbox":
            await self.listPlatforms(ctx=ctx, platform="Xbox", page=page)        
        if platform == "switch":
            await self.listPlatforms(ctx=ctx, platform="Switch", page=page)
        if platform == "pc":
            await self.listPlatforms(ctx=ctx, platform="PC", page=page)
        if platform == "vr":
            await self.listPlatforms(ctx=ctx, platform="VR", page=page)






    @commands.command(name="specs")
    async def specsCommand(self, ctx,guy: discord.Member=None,*, part=None, ):
        guildData = self.utility.memberData[str(ctx.guild.id)]
        if guy is None:
            guy = ctx.author


        

        if str(guy.id) not in guildData.keys():
            await ctx.send("This person hasn't added any platforms!")
        elif "PC" not in guildData[str(guy.id)]["platforms"].keys():
            await ctx.send("This person does not have a PC")
            
        
        else:
            if part is None:
                
                string = ""
                embed = discord.Embed(title=f"{guy.name}'s specs", colour=0x339931)
                for k, v in guildData[str(guy.id)]["platforms"]["PC"].items():
                    string+= f"**{k}:** {v}\n"  
                embed.description = string     
                await ctx.send(embed=embed)             
            elif part.lower() in ["processor","graphics card", "ram", "motherboard"]:
                part = part.lower()
                part = part.title()
                if part == "Ram":
                    part = "RAM"
                thePart = guildData[str(guy.id)]["platforms"]["PC"][part]
                await ctx.send(f"{guy.name}'s {part} is {thePart}")
            else:
                await ctx.send("That part is not valid")







          
    async def listPlatforms(self, ctx, page, platform):
        try:
            page = int(page)
        except:
            await ctx.channel.send("That is not an integer.")
            return
        itemsPerPage = 4
        platformList = []
        guildData = self.utility.memberData[str(ctx.guild.id)]
        secondCounter = 0
        for member, platforms in guildData.items(): # counts how many birthdays there are
            if platform in platforms["platforms"].keys():
                secondCounter += 1
                platformList.append([member, platforms["platforms"][platform]])
        lastPage = secondCounter % 8 # divide by how many terms we want in our embed and throw away the remainder
        if lastPage == 0:
            lastPage = int(secondCounter / itemsPerPage) # If its divisible by 8 then the last page will be full 
        else:
            lastPage = int((secondCounter // itemsPerPage) + 1) # if not we would need an extra page for the remaining birthdays

        guild = self.bot.get_guild(ctx.guild.id) # gets the guild the command is in
        if page >= 1 and page <= lastPage:
            embed = discord.Embed(
                title=f"Members of the server on {platform}",
                colour=0x339931,
            )
            text = "page {0}/{1}         ".format(page, lastPage)
            embed.set_footer(text=text)
            counter = 1
            for x in platformList:
                
                if counter > (itemsPerPage * (page - 1)) and counter < ((page * itemsPerPage)+1):

                    person = guild.get_member(int(x[0]))
                    if person is None:
                        del self.utility.memberData[str(ctx.guild.id)][str(x[0])]
                        continue
                    if platform != "PC" and platform != "MacOS":
                        if person.nick is None: # if person doesnt have a nickname
                            embed.add_field(
                                name=person.name,
                                value="This members console is **{}**".format(
                                    x[1]
                                ),
                              inline=False,
                          )
                        else: # else
                          embed.add_field(
                              name=person.name+"  ({})".format(person.nick),
                              value="This members console is **{}**".format(
                                  x[1], 
                              ),
                              inline=False, )       
                    else:
                        if platform == "PC":
                            string = ""
                            
                            for k, v in x[1].items():
                                string+= f"**{k}:** {v}\n"  
                                                    
                            if person.nick is None: # if person doesnt have a nickname

                                embed.add_field(
                                    name=person.name,
                                    value=string,
                                    
                                  inline=False,
                              )
                                  

                            else: # else
                              embed.add_field(
                                  name=person.name+"  ({})".format(person.nick),
                                  value=string,
                                  inline=False, )                                      
                counter += 1
            embed.set_thumbnail(url=ctx.guild.icon_url)
            if platform.lower() == "switch":
                embed.colour = 0xf50505
                file = discord.File("resources/switch.png", "switch.png")
            if platform.lower() == "playstation":
                embed.colour =0x1420ff
                file = discord.File("resources/playstation.png", "playstation.png")
            if platform.lower() == "pc":
                embed.colour =0x000000
                file = discord.File("resources/PC.png", "PC.png")
            if platform.lower() == "xbox":
                embed.colour = 0x00c213
                file = discord.File("resources/xbox.png", "xbox.png")
            if platform.lower() == "vr":
                file = discord.File("resources/VR.png", "VR.png")
                embed.colour = 0xfcfcfc

            embed.set_thumbnail(url="attachment://"+file.filename)
            await ctx.channel.send(embed=embed, file=file)

        else:
            await ctx.send("This page does not exist")



       
def setup(bot):
  
  bot.add_cog(Platform(bot))