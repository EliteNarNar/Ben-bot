
import re
import discord
from discord import Embed
import asyncio
from datetime import datetime
import random
import logging
logger = logging.getLogger('bot')
from discord.ext import commands, tasks
class playerOfTheDay(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot
        self.utility = self.bot.get_cog("utility")
        self.colour = self.utility.colour

    @commands.Cog.listener()
    async def on_ready(self): 
        self.utility = self.bot.get_cog("utility")
        print("Player of the day cog has been loaded")
        self.postPotd.start()
    @commands.command(name="forcepotd", help="Forces bot to choose potd")
    async def forcePotd(self, ctx, player=None):
        if (
            ctx.author.guild_permissions.administrator
        ):  # Checks if user has the administrator permission

            await self.chooseThePotd(
                str(ctx.guild.id), True, player
            )  # Calls the choose the player of the day function
        else:
            await ctx.channel.send("You do not have permission to use this command!")

            
    @commands.command(name="potd", help=("Potd settings"))
    async def potdSettings(
        self, ctx, setting=None, *, value=None
    ):  # We preset the parameters to be None so the code doesnt break if the user doesnt specify certain paramaters
        # The asterisk is there so that the value can be more than one word.
        if ctx.author.guild_permissions.administrator:  # Chcks perms
            if (
                not str(ctx.guild.id) in self.utility.botSettings
            ):  # Creates new entry if guild has no settings
                self.utility.botSettings[str(ctx.guild.id)] = {}
                for k, v in self.utility.defaultSettings.items():
                    self.utility.botSettings[str(ctx.guild.id)][k] = v

            if (
                ctx.guild.get_role(
                    self.utility.botSettings[str(ctx.guild.id)]["potdMinRole"]
                )  # Checks if the role the user specified is actually in the server
                in ctx.guild.roles
            ):
                mRole = ctx.guild.get_role(
                    self.utility.botSettings[str(ctx.guild.id)]["potdMinRole"]
                )  # If it does it will get the
            else:
                mRole = None  # if not we set it to None
            if (
                ctx.guild.get_role(
                    self.utility.botSettings[str(ctx.guild.id)]["potdRole"]
                )  # Again checking if the role is actually in the server (basically the same for all other vars)
                in ctx.guild.roles
            ):
                wRole = ctx.guild.get_role(self.utility.botSettings[str(ctx.guild.id)]["potdRole"])
            else:
                wRole = None
            if (
                ctx.guild.get_channel(
                    self.utility.botSettings[str(ctx.guild.id)]["potdAnnouncementChannel"]
                )
                in ctx.guild.channels
            ):
                aChannel = ctx.guild.get_channel(
                    self.utility.botSettings[str(ctx.guild.id)]["potdAnnouncementChannel"]
                )
            else:
                aChannel = None

            if setting is None:
                if (
                    self.utility.botSettings[str(ctx.guild.id)]["potdHour"] is None
                    or wRole is None
                    or mRole is None
                    or aChannel
                    is None  # if any one of these variables are None then we show users what settings they havent set
                ):

                    embed = discord.Embed(
                        title="Bot settings",
                        description="To continue please set the following settings",  # Discord embed
                        colour=self.colour,
                    )

                    if (
                        aChannel is None
                    ):  # If a variable isnt set we add the field to the embed so the user knows what setting hasnt been set
                        embed.add_field(
                            name="Announcement channel",
                            value="`.potd channel <channel>`",
                            inline=False,
                        )
                    if mRole is None:
                        embed.add_field(
                            name="Minimum role",
                            value="`.potd minimum-role <role>`",
                            inline=False,
                        )

                    if wRole is None:
                        embed.add_field(
                            name="Winner role",
                            value="`.potd winner-role <role>`",
                            inline=False,
                        )
                    embed.set_thumbnail(url=self.utility.boturl)
                    embed.set_footer(text="Brooke-Bot | EliteNarNar#3447")
                    await ctx.channel.send(embed=embed)

                    return  # exits the function
                else:
                    if self.utility.botSettings[str(ctx.guild.id)]["potd"]:  # If potd is True for the
                        status = "on"
                    else:
                        status = "off"
                    embed = discord.Embed(
                        title="Player of the day settings",
                        description="These are the settings currently set for this server \nPlayer of the day is currently **{}**".format(
                            status
                        ),
                        colour=self.colour,
                    )

                    embed.add_field(
                        name="Announcement time",
                        value="The announcement time is set to {}:00 UTC".format(
                            self.utility.botSettings[str(ctx.guild.id)]["potdHour"]
                        ),
                        inline=False,
                    )
                    embed.add_field(
                        name="Announcement channel",
                        value="The announcement channel is {}".format(
                            aChannel.mention
                        ),  # Mention is a discor mention
                        inline=False,
                    )
                    embed.add_field(
                        name="Winner's role",
                        value="The winner is given '{}''".format(wRole.name),
                        inline=False,
                    )
                    embed.add_field(
                        name="Minimum role",
                        value="The minimum role to win is '{}'".format(mRole.name),
                        inline=False,
                    )
                    if self.utility.botSettings[str(ctx.guild.id)]["potdCustomMessage"] is not None:
                        cm = "None"
                    else:
                        cm = self.utility.botSettings[str(ctx.guild.id)]["potdCustomMessage"]
                    embed.add_field(
                        name="Custom message",
                        value=cm,
                        inline=False,
                    )
                    embed.add_field(
                        name="Last player of the day",
                        value="The last winner was {}".format(
                            ctx.guild.get_member(self.utility.botSettings[str(ctx.guild.id)]["lastPotd"])
                        ),
                        inline=False,
                    )
                    embed.set_footer(text="Brooke-Bot | EliteNarNar#3447")
                    embed.set_thumbnail(url=ctx.guild.icon_url)
                    await ctx.channel.send(embed=embed)

            elif (
                value is None
            ):  # If the user didn't specify a value we just show setting they specify
                if setting == "channel":
                    if aChannel is not None:
                        await ctx.channel.send(
                            "The current announcement channel is {} to change it do `.potd channel <channel>`".format(
                                aChannel.mention
                            )
                        )
                    else:
                        await ctx.channel.send(
                            "The announcement channel has not been set yet. To set it do `.potd channel <channel>`"
                        )
                elif setting == "minimum-role":
                    if mRole is not None:
                        await ctx.channel.send(
                            "The current minimum role to get player of the day is {} to change it do `.potd minimum-role <role>".format(
                                mRole.mention
                            )
                        )
                    else:
                        await ctx.channel.send(
                            "The minimum role to get player of the day has currently not been set. To set it do `.potd minimum-role <role>`"
                        )

                elif setting == "winner-role":
                    if wRole is not None:
                        await ctx.channel.send(
                            "The current winning role that is given to player of the day is {} to change it do `.potd winner-role <role>`".format(
                                wRole.mention
                            )
                        )
                    else:
                        await ctx.channel.send(
                            "The role that is given to the player of the day has not been set. To set it do `.potd winner-role <role>`"
                        )
                elif setting == "time":
                    await ctx.channel.send(
                        "The current time the winners are announced is {}:00 UTC to change it do `potd time <hour(0-23)>`".format(
                            self.utility.botSettings[str(ctx.guild.id)]["potdHour"]
                        )
                    )
                elif setting == "custom-message":
                    if self.utility.botSettings[str(ctx.guild.id)]["potdCustomMessage"] is None:
                        await ctx.channel.send(
                            "There is currently no custom announcement. To set one do `.potd custom-message <message>` you can use {winnername} to add the users name and {winnermention} to mention them"
                        )
                    else:
                        await ctx.channel.send(
                            "This is the current announcement message:\n{}\nTo change it do `.potd custom-message <message>`".format(
                                self.utility.botSettings[str(ctx.guild.id)]["potdCustomMessage"]
                            )
                        )
                elif setting == "last-winner":
                    if self.utility.botSettings[str(ctx.guild.id)]["lastPotd"] is None:
                        await ctx.channel.send(
                            "There is currently not a last winner set. To change it do `potd last-winner <member>`"
                        )
                    else:
                        await ctx.channel.send(
                            "The last winner was {}".format(
                                ctx.guild.get_member(
                                    self.utility.botSettings[str(ctx.guild.id)]["lastPotd"]
                                ).name  # we use name and not mention because we dont want the last player of the day to be pinged everytime this command is run
                            )
                        )
                else:
                    await ctx.channel.send("Potd doesnt have that subcommand, do .help potd")
            else:
                setting = setting.lower()
                if setting == "channel":
                    channelMatch = re.match(
                        "<#(\d+)>", value
                    )  # This line checks whether the user mentioned a channel since channel mentions are in the form <#43253226432632>
                    if channelMatch:  # If it matches
                        try:
                            chanGuild = ctx.guild.get_channel(
                                int(channelMatch.group(1))
                            )  # the .group() function returns only what inside the brackets which would be the channel id
                            self.utility.botSettings[str(ctx.guild.id)]["potdAnnouncementChannel"] = int(
                                channelMatch.group(1)
                            )
                            await ctx.channel.send(
                                "The channel has been successfully set to {}!".format(
                                    chanGuild.mention  # We mention the channel it has been set to
                                )
                            )
                            aChannel = ctx.guild.get_channel(
                                self.utility.botSettings[str(ctx.guild.id)]["potdAnnouncementChannel"]
                            )
                        except:
                            await ctx.channel.send(
                                "That channel doesn't exist in this server!"
                            )

                    else:
                        await ctx.channel.send("Please enter a valid channel.")

                elif setting == "minimum-role":
                    roleMatch = re.match(
                        "<@&(\d+)>", value
                    )  # Roles mentions are in the syntax <&@416841842616482168>
                    if roleMatch:
                        try:
                            guildRole = ctx.guild.get_role(
                                int(roleMatch.group(1))
                            )  # Gets just the string on numbers which is the role id
                            self.utility.botSettings[str(ctx.guild.id)]["potdMinRole"] = int(
                                roleMatch.group(1)
                            )
                            await ctx.channel.send(
                                "The minimum role has been successfully set to {}!".format(
                                    guildRole.mention
                                )
                            )
                            mRole = ctx.guild.get_role(
                                self.utility.botSettings[str(ctx.guild.id)]["potdMinRole"]
                            )
                        except:
                            await ctx.channel.send(
                                "That role doesn't exist in this server!"
                            )
                    else:
                        await ctx.channel.send("Please enter a valid role.")

                elif setting == "winner-role":
                    roleMatch = re.match("<@&(\d+)>", value)  # same as before
                    if roleMatch:
                        try:
                            guildRole = ctx.guild.get_role(int(roleMatch.group(1)))
                            self.utility.botSettings[str(ctx.guild.id)]["potdRole"] = int(
                                roleMatch.group(1)
                            )
                            await ctx.channel.send(
                                "The role given to winners has been successfully set to {}!".format(
                                    guildRole.mention
                                )
                        )
                        except:
                            await ctx.channel.send(
                                "That role doesn't exist in this server!"
                            )
                    else:
                        await ctx.channel.send("Please enter a valid channel.")

                elif setting == "time":
                    try:
                        value = int(value)
                        if value >= 0 and value <= 23:  # checks if its a valid hour
                            self.utility.botSettings[str(ctx.guild.id)][
                                "potdHour"
                            ] = value  # Sets the potdHour to the value the user specified
                            await ctx.channel.send(
                                "Succesfully set announcement time to {}:00 UTC!".format(
                                    value
                                )  # COnfirms that it was successfully set
                            )
                        else:
                            await ctx.channel.send("Must be a number between 0 and 23!")
                    except:
                        await ctx.channel.send("Must be a number between 0 and 23!")
                elif setting == "custom-message":
                    self.utility.botSettings[str(ctx.guild.id)]["potdCustomMessage"] = value
                    await ctx.channel.send(
                        "The custom announcement has been set to:\n{}".format(value)
                    )
                elif setting == "last-winner":
                    memberMatch = re.match("<@!(\d+)>", value)
                    if ctx.guild.get_member(int(memberMatch.group(1))) is None:
                        print("This member does not exist")
                    else:
                        member = ctx.guild.get_member(int(memberMatch.group(1)))
                        self.utility.botSettings[str(ctx.guild.id)]["lastPotd"] = member.id
                        await ctx.channel.send(
                            "The last player of the day has been set to {}".format(
                                member.name
                            )
                        )
        else:
            await ctx.channel.send("You do not have permission to use this command!")
    @tasks.loop(hours=1)  # Task loops every hour (see before_postPotd first)
    async def postPotd(self):
        chosen = False  # initialise chosen
        await asyncio.sleep(
            1
        )  # we wait a second to make sure this code is being executed in the hour specified
        now = datetime.utcnow()  # Time NOW this very second
        logger.debug("Checking if time to activate")
        for (
            guildId,
            guildSettings,
        ) in (
            self.utility.botSettings.items()
        ):  # Checks all the guilds to see if any of them have the potd hour set to this hour
            try:
                if guildSettings["potdHour"] == now.hour:
                    try:
                        logger.debug("Choosing player of the day for "+self.bot.get_guild(int(guildId)).name)
                    except Exception as e:
                        logger.critical("Error while choosing the player of the day for guild: "+guildId+"\n"+e)
                    chosen = (
                        True  # we alert the code that at least one guild has picked this hour
                    )
                    await self.chooseThePotd(
                        guildId, False
                    )  # We give the function the guildId and specify that it was NOT forced (False)
            except TypeError as e:
                print(e)
                print(guildSettings)
                hour = guildSettings
                logger.debug(f"Exeption: {e}\n The value of guild settings is {hour}")

        if not chosen:  # If chosen is still false then no guilds picked this hour
            logger.debug("No guilds have chosen this hour to pick")

    @postPotd.before_loop
    async def before_postPotd(self):  # This will run before postPotd starts to make sure that if the bot is ran we sleep until it is a whole o'clock eg 1:00 then we keep looping every hour
        await self.bot.wait_until_ready()
        now = datetime.utcnow()
        future = datetime(now.year, now.month, now.day, now.hour + 1, 0, 0, 0)
        logger.debug("Player of the day sleeping for {} seconds".format((future - now).seconds))
        await asyncio.sleep((future - now).seconds)


    async def chooseThePotd(self, guildId, forced, member=None):
        if not self.utility.botSettings[str(guildId)][
            "potd"
        ]:  # If the guild has potd disabled we just return
            print("Guild currently has potd disabled")
            return
        chosen = False
        guild = self.bot.get_guild(int(guildId))
        minRole = guild.get_role(self.utility.botSettings[str(guildId)]["potdMinRole"])
        annChannel = guild.get_channel(self.utility.botSettings[str(guildId)]["potdAnnouncementChannel"])
        winRole = guild.get_role(self.utility.botSettings[str(guildId)]["potdRole"])
        lastWinner = guild.get_member(
            int(self.utility.botSettings[str(guildId)]["lastPotd"])
        )  # We are getting the role, channel and member objects from the guild object
        if (
            lastWinner is not None
        ):  # If there is a last winner we remove the player of the day role from them before selecting a new winner
            try:
                await lastWinner.remove_roles(winRole)
                logger.debug("Player of the day role removed from {}".format(lastWinner.name))
                print("Player of the day role removed from {}".format(lastWinner.name))
                for member in guild.members:
                    for role in member.roles:
                        if role.id == winRole.id:
                            await member.remove_roles(winRole)
                            logger.debug("Player of the day role removed from {} who was detected to have the role".format(member.name))

            except Exception as e:
                logger.critical("Error while removing roles:\n {}".format(e))
                await annChannel.send("The bot doesnt have permission to add / remove roles.")
        if not forced or (
            forced and member is None
        ):  # If the .forcepotd command wasnt used or it WAS used but the user didnt specify a member we have to choose a member

            while not chosen:
                contender = random.choice(guild.members)
                logger.debug("Contender is '{0}'".format(contender.name))
                if (
                    contender.top_role >= minRole and not contender.bot
                ):  # Checks if person has the minimum role or higher and that it isnt a bot
                    if (
                        contender.id != self.utility.botSettings[str(guildId)]["lastPotd"]
                    ):  # Checks that it isnt the last player
                        chosen = True  # sets chosen to true, ending the loop
                        logger.debug(contender.name+" has been selected")
                        break
                    else:
                        logger.debug(
                            "Person was player of the day last time! Choosing someone else"
                        )
                        continue
                else:
                    logger.debug("Person is either a bot or not high enough ranked")
                    continue
        else:  # This will happen if the command was forced and the member was specified
            print(member)
            memberMatch = re.match(
                "<@!(\d+)>", member
            )  # THis will get the member id because member mentions are in the form <@!35732985738298735273>
            contender = guild.get_member(
                int(memberMatch.group(1))
            )  # Gets the member object
            if (
                contender is None
            ):  # If the contender is None it means the member does not exist
                logger.critical("Member does not exist")
                
                return
        await contender.add_roles(winRole)  # Will add winner role to the winner
        self.utility.botSettings[str(guildId)]["lastPotd"] = contender.id  # Will make this member last player of the day
        logger.debug("{} has been set as last winner".format(guild.get_member(self.utility.botSettings[str(guildId)]["lastPotd"]).name))
        logger.debug("Potd is {}".format(contender.name))
        if (
            self.utility.botSettings[str(guildId)]["potdCustomMessage"] is None
        ):  # If the guild hasnt got a custom message set
            embed = discord.Embed(
                title="Player of the day",
                description="Today's player of the day goes to {0}".format(
                    contender.mention
                ),
                colour=self.colour,
            )
            embed.set_thumbnail(url=contender.avatar_url)
            embed.set_footer(text="Brooke-bot | EliteNarNar#3447")
            await annChannel.send(content=contender.mention,embed=embed)

        else:
            url = str(contender.avatar_url)
            announcement = self.utility.botSettings[guildId]["potdCustomMessage"]
            announcement = announcement.replace(
                "{winnermention}", contender.mention
            )  # So that the user can mention a user
            announcement = announcement.replace(
                "{winnername}", contender.name
            )  # So that the user can use the name of a user
            embed = discord.Embed(
                title="Player of the day",
                description=announcement,
                colour=self.colour,
            )
            embed.set_footer(text="Brooke-Bot | EliteNarNar#3447")
            embed.set_thumbnail(url=url)
            await annChannel.send(embed=embed)
        self.utility.botSettings[str(guildId)]["lastPotd"] = contender.id  # Will make this member last player of the day
        if contender.id != self.utility.botSettings[str(guildId)]["lastPotd"]:
            logger.critical("Contender has not been set as lastpotd correctly")
        logger.debug("{} has been set as last winner again just in case".format(guild.get_member(self.utility.botSettings[str(guildId)]["lastPotd"])))
        
def setup(bot):     
    bot.add_cog(playerOfTheDay(bot))