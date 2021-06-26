
import re
from datetime import datetime
import asyncio
from discord.ext import commands, tasks
import discord
import logging
from discord import Embed
logger = logging.getLogger('bot')
class birthdays(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot
        self.utility = self.bot.get_cog("utility")
        self.colour = self.utility.colour

    @commands.command(name="birthday")  ## This is a 
    async def birthdays(self, ctx, action=None, value=None, user=None):
        if (
            not str(ctx.guild.id) in self.utility.botSettings
        ):  # Same as before, makes a new entry if the guild has no settings
            self.utility.botSettings[str(ctx.guild.id)] = {}
            for k, v in self.utility.defaultSettings.items():
                self.utility.botSettings[str(ctx.guild.id)][k] = v
        if (
            not str(ctx.guild.id) in self.utility.userBirthdays
        ):  # Same as before, makes a new entry if the guild has no settings
            self.utility.userBirthdays[str(ctx.guild.id)] = {}
        if value is not None:
            value = value.lower()
        if action is not None:
            action = action.lower()
        if action is None:
            await ctx.channel.send("`.birthday <action>`")

        elif value is None:
            if action == "set":
                await ctx.channel.send(
                    "`.birthday set <birthday>` Make sure your birthday is in the form XX/XX"
                )
            elif action == "list":
                await self.listBirthdays(ctx, 1)
            elif action == "set-channel":
                await ctx.channel.send("`.birthday set-channel <channel>`")
            elif action == "channel":
                if (
                    self.utility.botSettings[str(ctx.guild.id)]["birthdayAnnouncementChannel"]
                    is not None
                ):
                    await ctx.channel.send(
                        "The current announcement channel is {} to change it do `.birthday set-channel <channel>`".format(
                            ctx.guild.get_channel(
                                int(
                                    self.utility.botSettings[str(ctx.guild.id)][
                                        "birthdayAnnouncementChannel"
                                    ]
                                )
                            ).mention
                        )
                    )
                else:
                    await ctx.channel.send(
                        "The current announcement channel has not been set yet to set it do `.birthday set-channel <channel>"
                    )
            else:
            
                channelMatch = re.match("<@!(\d+)>", action)
                if channelMatch:
                    guy = ctx.guild.get_member(int(channelMatch.group(1)))
                    if guy is None:
                        await ctx.channel.send("This member does not exist in this server!")
                        return
                    try:
                        await ctx.channel.send(
                            "{}'s birthday is {}".format(
                                guy.name,
                                self.utility.userBirthdays[str(ctx.guild.id)][
                                    str(channelMatch.group(1))
                                ]["birthday"],
                            )
                        )
                    except:
                        await ctx.channel.send(
                            "{} hasn't set their birthday yet".format(guy.name)
                    )
                else:
                    await ctx.channel.send("Invalid argument")
        else:
            if action == "set":
                birthdayMatch = re.match("(\d{2})\/(\d{2})", value)
                if birthdayMatch:
                    birthdayMonth = int(birthdayMatch.group(2))
                    birthdayDay = int(birthdayMatch.group(1))

                    if birthdayMonth > 12 or birthdayMonth < 0:
                        await ctx.channel.send(
                            "This isnt a valid date! Remember the first number is the day and the second number is the month"
                        )
                        return

                    elif (
                        (birthdayDay > 31)
                        or (
                            (birthdayDay > 30)
                            and (
                                birthdayMonth == 4
                                or birthdayMonth == 6
                                or birthdayMonth == 9
                                or birthdayMonth == 11
                            )
                        )
                        or ((birthdayMonth == 2) and (birthdayDay > 29))
                    ):
                        await ctx.channel.send(
                            "This isnt a valid date! Remember the first number is the day and the second number is the month"
                        )
                        return
                    else:
                        if user is None:
                            if (
                                not str(ctx.author.id) in self.utility.userBirthdays[str(ctx.guild.id)]
                            ):  # Same as before, makes a new entry if the guild has no settings
                                self.utility.userBirthdays[str(ctx.guild.id)][str(ctx.author.id)] = {}
                                self.utility.userBirthdays[str(ctx.guild.id)][str(ctx.author.id)] = {
                                    "birthday": None
                                }
                            self.utility.userBirthdays[str(ctx.guild.id)][str(ctx.author.id)][
                                "birthday"
                            ] = value
                            await ctx.channel.send(
                                "Your birthday has been set to {}".format(value)
                            )

                        else:

                            memberMatch = re.match("<@!(\d+)>", user)
                            if memberMatch:
                                member = ctx.guild.get_member(int(memberMatch.group(1)))
                                if member is None:
                                    await ctx.channel.send(
                                        "This member is not in this guild."
                                    )
                                    return

                                else:
                                    if (
                                        ctx.author.guild_permissions.administrator
                                        or member.id == ctx.author.id
                                    ):
                                        if (
                                            not str(member.id)
                                            in self.utility.userBirthdays[str(ctx.guild.id)]
                                        ):  # Same as before, makes a new entry if the guild has no settings
                                            self.utility.userBirthdays[str(ctx.guild.id)][
                                                str(member.id)
                                            ] = {}
                                            self.utility.userBirthdays[str(ctx.guild.id)][
                                                str(member.id)
                                            ] = {"birthday": None}

                                        self.utility.userBirthdays[str(ctx.guild.id)][str(member.id)][
                                            "birthday"
                                        ] = value
                                        await ctx.channel.send(
                                            "Set {}'s birthday to {}".format(
                                                member.mention, value
                                            )
                                        )
                                    else:
                                        await ctx.channel.send(
                                            "You do not have permission to use this command!"
                                        )

                else:
                    await ctx.channel.send("Invalid syntax. It has to be in form XX/XX")
                    return

            elif action == "list":
                await self.listBirthdays(ctx, value)
            elif action == "reset":
                if value is None:
                    del self.utility.userBirthdays[str(ctx.guild.id)][str(ctx.author.id)]
                    await ctx.channel.send("Reset your birthday!")
                else:
                    if ctx.author.guild_permissions.administrator:
                        memberMatch = re.match("<@(\d+)>", value)
                        if memberMatch:
                            member = ctx.guild.get_member(int(memberMatch.group(1)))
                            del self.utility.userBirthdays[str(ctx.guild.id)][memberMatch.group(1)]
                            await ctx.channel.send("Reset {}'s' birthday!".format(member.name))   
                        else:
                            await ctx.channel.send("That member does not exist")      
                    else:
                        await ctx.channel.send("You do not have permmision to reset other users birthdays!")            

            elif action == "set-channel":
                  if ctx.author.guild_permissions.administrator:
                      channelMatch = re.match(
                          "<#(\d+)>", value
                      )  # This line checks whether the user mentioned a channel since channel mentions are in the form <#43253226432632>
                      if channelMatch:
                          channel = ctx.guild.get_channel(int(channelMatch.group(1)))
                          if channel is not None:
                              self.utility.botSettings[str(ctx.guild.id)][
                                  "birthdayAnnouncementChannel"
                              ] = channelMatch.group(1)
                              await ctx.channel.send(
                                  "Birthday announcement channel has been set to {}".format(
                                      channel.mention
                                  )
                              )
                          else:
                              await ctx.channel.send(
                                  "This channel does not exist in this server!"
                              )
                      else:
                          await ctx.channel.send("That is not a valid channel!")
                  else:
                      await ctx.channel.send("You don't have permission to use this command!")


    @tasks.loop(hours=24)
    async def birthdayTask(self):
        chosen = False
        await asyncio.sleep(5)
        now = datetime.utcnow()
        logger.debug("Checking if its anyones birthday...")
        #now = datetime(now.year, now.month, now.day-1, 23,59, 55, 0)
        for guildId, playerSettings in self.utility.userBirthdays.items():
            for player, birthday in playerSettings.items():
                birthdayMatch = re.match("(\d{2})\/(\d{2})", birthday["birthday"])

                birthdayMonth = int(birthdayMatch.group(2))
                birthdayDay = int(birthdayMatch.group(1))

                if birthdayMonth == now.month and birthdayDay == now.day:
                    await self.birthdayAnnounce(player, guildId)
                    chosen = True
                else:
                    continue
        if not chosen:
            logger.debug("Its no ones birthday today.")



    @birthdayTask.before_loop
    async def before_birthdayTask(self):
        await self.bot.wait_until_ready()
        now = datetime.utcnow()
        #now = datetime(now.year, now.month, now.day -1, 23, 59, 57, 0)
        if now.hour < 9:
            future = datetime(now.year, now.month, now.day, 9, 0, 0, 0)
        else:
            future = datetime(now.year, now.month, now.day+1, 9, 0, 0, 0)
        logger.debug("Birthday Sleeping for {} seconds".format((future - now).seconds))

        await asyncio.sleep((future - now).seconds)
    async def listBirthdays(self,ctx, page):
        try:
            page = int(page)
        except:
            await ctx.channel.send("That is not an integer.")
            return
        secondCounter = 0
        for member, birthday in self.utility.userBirthdays[str(ctx.guild.id)].items(): # counts how many birthdays there are
            secondCounter += 1
        lastPage = secondCounter % 8 # divide by how many terms we want in our embed and throw away the remainder
        if lastPage == 0:
            lastPage = int(secondCounter / 8) # If its divisible by 8 then the last page will be full 
        else:
            lastPage = int((secondCounter // 8) + 1) # if not we would need an extra page for the remaining birthdays

        guild = self.bot.get_guild(ctx.guild.id) # gets the guild the command is in
        if page >= 1 and page <= lastPage:
            embed = discord.Embed(
                title="Birthdays",
                description="These the members birthdays:",
                colour=self.colour,
            )
            text = "page {0}/{1}                          Sorted by closest birthday".format(page, lastPage)
            embed.set_footer(text=text)
            counter = 1
            birthdayList = []
            ######## SORTING BY LATEST BIRTHDAY
            for member, birthday in self.utility.userBirthdays[str(ctx.guild.id)].items():
                birthdayList.append([member, birthday["birthday"]])
            now = datetime.utcnow()
            for x in range(len(birthdayList)):

                for y in range(0, len(birthdayList) - x - 1):
                    birthdayMatch = re.match("(\d{2})\/(\d{2})", birthdayList[y][1])

                    birthdayMonth = birthdayMatch.group(2)
                    birthdayDay = birthdayMatch.group(1)
                    AbirthdayMatch = re.match("(\d{2})\/(\d{2})", birthdayList[y + 1][1])

                    AbirthdayMonth = AbirthdayMatch.group(2)
                    AbirthdayDay = AbirthdayMatch.group(1)

                    birthdayMonth = int(birthdayMonth)
                    AbirthdayMonth = int(AbirthdayMonth)
                    birthdayDay = int(birthdayDay)
                    AbirthdayDay = int(AbirthdayDay)
                    if birthdayMonth > AbirthdayMonth:

                        birthdayList[y], birthdayList[y + 1] = birthdayList[y + 1], birthdayList[y],
                        
            for x in range(len(birthdayList)):

                for y in range(0, len(birthdayList) - x - 1):
                    birthdayMatch = re.match("(\d{2})\/(\d{2})", birthdayList[y][1])
                    AbirthdayMatch = re.match(
                        "(\d{2})\/(\d{2})", birthdayList[y + 1][1]
                    )
                    birthdayMonth = int(birthdayMatch.group(2))
                    birthdayDay = int(birthdayMatch.group(1))

                    AbirthdayMonth = int(AbirthdayMatch.group(2))
                    AbirthdayDay = int(AbirthdayMatch.group(1))
                    if birthdayDay > AbirthdayDay:
                        if birthdayMonth == AbirthdayMonth:
                            birthdayList[y], birthdayList[y + 1] = birthdayList[y+1], birthdayList[y],
            newBirthdayList = []
            acounter = 0      

            for birthday in birthdayList:
    
                birthdayMatch = re.match("(\d{2})\/(\d{2})", birthdayList[acounter][1])

                newBirthdayDay = int(birthdayMatch.group(1))
                newBirthdayMonth = int(birthdayMatch.group(2))

                if newBirthdayMonth < now.month or (newBirthdayMonth == now.month and newBirthdayDay <= now.day):
                    newBirthdayList.append(birthdayList[acounter])

                    del birthdayList[acounter]
                    acounter-=1
                acounter+=1
            for x in newBirthdayList:
                birthdayList.append(x)
            ##displaying the list
            for x in birthdayList:
                if counter > (8 * (page - 1)) and counter < ((page * 8)+1):

                    person = guild.get_member(int(x[0]))
                    if person is None:
                        del self.utility.userBirthdays[str(ctx.guild.id)][str(x[0])]
                        continue

                    if person.nick is None: # if person doesnt have a nickname
                        embed.add_field(
                            name=person.name,
                            value="This members birthday is **{}**".format(
                                x[1]
                            ),
                          inline=False,
                      )
                    else: # else
                      embed.add_field(
                          name=person.name+"  ({})".format(person.nick),
                          value="This members birthday is **{}**".format(
                              x[1], 
                          ),
                          inline=False, )                     
                counter += 1
            embed.set_thumbnail(url=ctx.guild.icon_url)
            await ctx.channel.send(embed=embed)
        else:
            await ctx.channel.send("This page does not exist!")


    async def birthdayAnnounce(self, player, guildId):
        if self.utility.botSettings[str(guildId)]["birthdayAnnouncements"]:
            guild = self.bot.get_guild(int(guildId))
            birthdayMember = guild.get_member(int(player))
            channel = guild.get_channel(
                int(self.utility.botSettings[str(guildId)]["birthdayAnnouncementChannel"])
            )
            embed = discord.Embed(
                title="Birthdays!",
                description=" @everyone, its {}'s birthday today! Wish {} a happy birthday!".format(
                    birthdayMember.mention, birthdayMember.name
                ),
            )
            url = str(birthdayMember.avatar_url)
            embed.set_thumbnail(url=url)
            await channel.send(content="@everyone",embed=embed)
        else:
            print("{} has birthday announcements disabled".format(self.bot.get_guild(int(guildId)).name))

    
    
    @commands.Cog.listener()
    async def on_ready(self): 
        self.utility = self.bot.get_cog("utility")
        print("Birthdays cog has been loaded")
        self.birthdayTask.start()
def setup(bot):     
    bot.add_cog(birthdays(bot)) 