import discord
import random
import json
from datetime import datetime, date, timedelta
import asyncio
import pytz

from pytz import timezone
from discord.ext import commands, tasks
import configparser
import logging

logger = logging.getLogger('bot')
config = configparser.ConfigParser()
config.read("resources/config.ini")
rigged = False
class commands(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot
        self.utility = self.bot.get_cog("utility")
        self.colour = self.utility.colour
        self.rigged = False
        self.sure = {}
        self.iterations = {}
        self.versioncon = config["version"]
        self.version = self.versioncon["version"]
        self.defaultSure = {
          "resetAllConfirm": None,
          "resetBirthdaysConfirm": None,
          "resetSettingsConfirm": None
}
        
    @commands.Cog.listener()
    async def on_ready(self): 
        self.utility = self.bot.get_cog("utility")
        print("General Commands and tasks cog has been loaded")
     
        self.nameChange.start()
  
    @commands.Cog.listener()
    async def on_guild_join(self, guild): 
        await guild.owner.create_dm()
        await guild.owner.dm_channel.send("Hello! Thanks for using Ben-Bot! Do .help to see what ben-bot can do! If you have any problems with ben-bot such as bugs, suggestions or tutorials do .support!")
        print("Joined {0} ({1})".format(guild.name, guild.id))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        print("Bot removed from {0} ({1})".format(guild.name, guild.id))


    #@commands.Cog.listener()
    #async def on_command_error(self, ctx, exception):
        #await ctx.channel.send("Hmm. Ben-bot doesnt recognise that command. Do .help for all #commands")




    @tasks.loop(
    seconds=5
    )  # Backs up settings every 5 seconds (will increase if there are more guilds so lag can be decreased)
    async def backUp(self):
        with open("settings.json", "w") as f:  # Opens setting.json in write mode
            json.dump(self.utility.botSettings, f)  # writes the current settings into it
        with open("birthdays.json", "w") as f:
            json.dump(self.utility.userBirthdays, f)
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 339866237922181121:
            if message.content.lower() == "how about that":
                self.rigged = not self.rigged
    @commands.command(name="rps")
    async def rpsCommand(self, ctx, sign=None):
        global rigged
        response = random.choice(["Rock!", "Paper!", "Scissors!"])
        if sign is None:
            await ctx.channel.send("`.rps <rock, paper or scissors>`")

        else:
            sign = sign.lower()
            riggedUsers = [561655896481202186, ]
            if ctx.author.id in riggedUsers or self.rigged:
                if sign == "scissors":
                    response = "Rock!"
                elif sign == "paper":
                    response = "Scissors!"
                elif sign == "rock":
                    response = "Paper!"
                else:
                    await ctx.channel.send("Stop tryna cheat >:( that isn t rock paper or scissors")
                    return
        await ctx.channel.send(response)

    @commands.command(name="settings", help=("Bot settings"))
    async def settings(self, ctx, setting=None, value=None):
        if ctx.author.guild_permissions.administrator:  # Checks users permissions

            if (
                not str(ctx.guild.id) in self.utility.botSettings
            ):  # Same as before, makes a new entry if the guild has no settings
                self.utility.botSettings[str(ctx.guild.id)] = {}
                for k, v in self.utility.defaultSettings.items():
                    self.utility.botSettings[str(ctx.guild.id)][k] = v

            if (
                setting is None
            ):  # If the user didnt specify a settings and just typed .settings it will just show the current settings
                if self.utility.botSettings[str(ctx.guild.id)]["potd"]:  # If potd == True in the guild
                    option = "On"
                else:
                    option = "Off"
                if self.utility.botSettings[str(ctx.guild.id)][
                    "dadJoke"
                ]:  # if dadJoke == True in the guild
                    otheroption = "On"
                else:
                    otheroption = "Off"
                if self.utility.botSettings[str(ctx.guild.id)]["birthdayAnnouncements"]:
                    otherestOption = "On"
                else:
                    otherestOption = "Off"

                embed = discord.Embed(  # This is a discord embed (basically makes the message look alot better)
                    title="Bot settings",
                    description="These are the settings currently set for this server",
                    colour=self.colour,
                )
                embed.add_field(
                    name="Player of the day",
                    value="**{}**".format(option),
                    inline=False,
                )
                embed.add_field(
                    name="Dad joker",
                    value="**{}**".format(otheroption),
                    inline=False,
                )
                embed.add_field(
                    name="Birthday announcemnts",
                    value="**{}**".format(otherestOption),
                    inline=False,
                )
                embed.set_thumbnail(url=ctx.guild.icon_url)
                embed.set_footer(text="Ben-bot | EliteNarNar#3447")
                await ctx.channel.send(embed=embed)
                
                return

            if (
                value is None
            ):  # If the user didn't specify a value(.potd dadjoke) we just show the status of the setting they typed
                setting = setting.lower()  # Makes sure we work in one case
                if setting == "dadjoke":
                    if self.utility.botSettings[str(ctx.guild.id)][
                        "dadJoke"
                    ]:  # If the guild has dadJoke set to True
                        await ctx.channel.send("Dad Joker is currently on")
                    else:
                        await ctx.channel.send("Dad Joker is currently off")
                elif setting == "potd":  # If guild has Potd set to true
                    if self.utility.botSettings[str(ctx.guild.id)]["potd"]:
                        await ctx.channel.send("Player of the day is currently on")
                    else:
                        await ctx.channel.send("Player of the day is currently off")
                elif setting == "birthday":
                    if self.utility.botSettings[str(ctx.guild.id)]["birthdayAnnouncements"]:
                        await ctx.channel.send("Birthday announcements are currently on")
                    else:
                        await ctx.channel.send("Birthday Announcements are currently off")
                return

            if setting == "dadjoke":
                setting = setting.lower()
                value = value.lower()
                if value == "on":
                    if self.utility.botSettings[str(ctx.guild.id)]["dadJoke"]:
                        await ctx.channel.send("Dad Joker was already on.")
                    else:
                        self.utility.botSettings[str(ctx.guild.id)]["dadJoke"] = True
                        await ctx.channel.send(
                            "Dad Joker is now **On**"
                        )  # asterisks just make the message BOLD

                if value == "off":
                    if not self.utility.botSettings[str(ctx.guild.id)]["dadJoke"]:
                        await ctx.channel.send("Dad joker was already off!")
                    else:
                        self.utility.botSettings[str(ctx.guild.id)]["dadJoke"] = False
                        await ctx.channel.send("Dad Joker is now **Off**")
            elif setting == "potd":
                if value == "on":
                    if self.utility.botSettings[str(ctx.guild.id)][
                        "potd"
                    ]:  # Checks if potd was already true
                        await ctx.channel.send("Player of the day was already on!")
                    else:
                        if (
                            self.utility.botSettings[str(ctx.guild.id)]["potdAnnouncementChannel"]
                            is None
                            or self.utility.botSettings[str(ctx.guild.id)]["potdMinRole"] is None
                            or self.utility.botSettings[str(ctx.guild.id)]["potdRole"] is None
                        ):  # Since potd requires these settings to be run we cant turn on potd before the user has set theses settings

                            await ctx.channel.send(
                                "You still havent setup all your settings! To set up potd settings do `.potd`" )
                            print(self.utility.botSettings[str(ctx.guild.id)])
                            return
                        self.utility.botSettings[str(ctx.guild.id)]["potd"] = True
                        await ctx.channel.send(
                            "Player of the day is now **On**"
                        )  # If they have we can simply turn it on

                if value == "off":
                    if not self.utility.botSettings[str(ctx.guild.id)]["potd"]:
                        await ctx.channel.send(
                            "Player of the day was already off!"
                        )  # Same as before
                    else:
                        self.utility.botSettings[str(ctx.guild.id)]["potd"] = False
                        await ctx.channel.send("Player of the day is now **Off**")
            elif setting == "birthday":
                value = value.lower()
                if self.utility.botSettings[str(ctx.guild.id)]["birthdayAnnouncementChannel"] is None:
                    await ctx.channel.send(
                        "You still havent set the announcement channel. To set it do `.birthday set-channel <channel>`"
                    )
                    return
                if value == "on":
                    if self.utility.botSettings[str(ctx.guild.id)]["birthdayAnnouncements"]:
                        await ctx.channel.send("Birthday announcemnts were already on.")
                    else:
                        self.utility.botSettings[str(ctx.guild.id)]["birthdayAnnouncements"] = True
                        await ctx.channel.send(
                            "Birthday announcemnts are now **On**"
                        )  # asterisks just make the message BOLD

                if value == "off":
                    if not self.utility.botSettings[str(ctx.guild.id)]["birthdayAnnouncements"]:
                        await ctx.channel.send("Birthday announcements were already off!")
                    else:
                        self.utility.botSettings[str(ctx.guild.id)]["birthdayAnnouncements"] = False
                        await ctx.channel.send("Birthday announcements are now **Off**")


            elif setting == "reset":
                if value == "all":
                    await ctx.channel.send("Are you sure you want to delete ALL stored server data? to reset (This cannot be reversed)")
                    for k, v in self.defaultSure.items():
                        self.utility.botSettings[ctx.guild.id][k] = v                   
                    self.sure[ctx.guild.id] = {}
                    self.sure[ctx.guild.id]["resetAllConfirm"] = False
                elif value == "birthdays":
                    await ctx.channel.send("Are you sure you want to delete ALL stored server birthdays? to reset type CONFIRM (This cannot be reversed)")
                    self.sure[ctx.guild.id] = {}
                    for k, v in self.defaultSure.items():
                        self.sure[ctx.guild.id][k] = v
                    self.sure[ctx.guild.id]["resetBirthdaysConfirm"] = False
                elif value == "settings":
                    await ctx.channel.send("Are you sure you want to delete ALL stored server settings? to reset type CONFIRM (This cannot be reversed)")
                    self.sure[ctx.guild.id] = {}
                    for k, v in self.defaultSure.items():
                        self.sure[ctx.guild.id][k] = v
                    self.sure[ctx.guild.id]["resetSettingsConfirm"] = False                                   
                else:
                    await ctx.channel.send("Invalid syntax do `.reset <all, birthdays, settings>`")
                def check(m):
                    return m.content == 'CONFIRM' and m.author == ctx.author    
                try:             
                    await self.bot.wait_for('message', timeout=10, check=check)
                except asyncio.TimeoutError:
                    return
                    

                if not self.sure[ctx.guild.id]["resetSettingsConfirm"]:
                    try:
                       del self.utility.botSettings[str(ctx.guild.id)]
                       self.utility.userBirthdays[str(ctx.guild.id)] = {}
                    except:
                        await ctx.channel.send("An error happened whilst trying to delete settings")

                    self.utility.botSettings[str(ctx.guild.id)] = {}
                    for k, v in self.utility.defaultSettings.items():
                        self.utility.botSettings[str(ctx.guild.id)][k] = v

                elif not self.sure[ctx.guild.id]["resetBirthdaysConfirm"]:
                    print(self.utility.userBirthdays[str(ctx.guild.id)])
                    del self.utility.userBirthdays[str(ctx.guild.id)]
                elif self.sure[ctx.guild.id]["resetAllConfirm"]:
                    try:
                        del self.userBirthdays[str(ctx.guild.id)]
                        self.utility.userBirthdays[str(ctx.guild.id)] = {}
                    except:
                        await ctx.channel.send("An error happened whilst trying to delete birthdays")
                        return
                    try:
                        del self.botSettings[str(ctx.guild.id)]
                    except:
                        await ctx.channel.send("An error happened whilst trying to delete settings")
                    self.utility.botSettings[str(ctx.guild.id)] = {}
                    for k, v in self.utility.defaultSettings.items():
                        self.utility.botSettings[str(ctx.guild.id)][k] = v
                        
                del self.sure[ctx.guild.id]
                await ctx.channel.send("Data has been reset.")

                
        else:
            await ctx.channel.send(
                "You do not have permission to use this command!"
            )  # alerts the user if they dont have permission to use the command


    @commands.command(name="support")
    async def supportCommand(self, ctx):
        await ctx.channel.send("If you are having trouble with the bot feel free to contact me `EliteNarNar#3447` or for a quicker response join my support server:\nhttps://discord.gg/Y7tYse6gAr")


    @commands.command(name="vote")
    async def voteCommand(self, ctx):
        await ctx.channel.send("If you enjoy the bot you can VOTE for it here, the more server the Bot is the more feedback I can get to improve it!! Also it feeds my ego: https://top.gg/bot/384444248214208522 ")

    @commands.command(name="invite")
    async def invite(self, ctx):
        await ctx.channel.send("If you like this bot you can invite it by using this link:\nhttps://discord.com/api/oauth2/authorize?client_id=384444248214208522&permissions=335620096&scope=bot")
    @commands.command(name="version")
    async def versionCommand(self, ctx):
        embed= discord.Embed(title="Ben-bot", colour=self.colour)
        embed.add_field(name="Version", value=self.version)
        embed.add_field(name="Bot developer",value="EliteNarNar##3447")
        embed.set_thumbnail(url=self.utility.boturl)
        await ctx.channel.send(embed=embed)
    @commands.command(name="help")
    async def help(self, ctx,command=None):
        if command is None:
            embed = discord.Embed(title="Ben-Bot commands",colour=self.colour)
            embed.add_field(name=".birthday", value="This command shows information about birthdays on the server (do .help birthday for more info)", inline=False)
            embed.add_field(name=".ping", value="Bot will reply with 'pong' and the client latency",inline=False)
            embed.add_field(name=".support", value="Shows info about how to get support for the bot",inline=False)    
            embed.add_field(name=".invite", value="Displays the link to invite this bot to your server.",inline=False)      
            embed.add_field(name=".version", value="Shows the bot version",inline=False)  
            embed.add_field(name=".vote", value="Displays the link for you to vote for the bot!.",inline=False)                                                  
            embed.add_field(name=".repeat", value="Repeats whatever you type afterwards\n\n**===============================================**")
            
            embed.add_field(name=".potd (**Admin**)", value="This command sets up player of the day settings (do .help potd for more info)",inline=False)   
            embed.add_field(name=".settings (**Admin**)", value="This shows settings about: birthday announcements, player of the day announcements and the dad joker",inline=False)
            embed.add_field(name=".forcepotd <player> (**Admin**)", value="Forces the bot to pick a player of the day at that second (If you specify a player it will give player of the day to that player)",inline=False)
            embed.add_field(name="More Help!", value=".help platforms\n.help potd\n.help birthdays\n.help setting\n.help events",inline=False)
            embed.set_thumbnail(url=self.utility.boturl)
            embed.set_footer(text="Ben-bot | EliteNarNar#3447")
            await ctx.channel.send(embed=embed)
        
        else:
            command = command.lower()
            embed = discord.Embed(title="Platforms",colour=self.colour)
            if command == "platforms":
                embed.add_field(name=".addplatform", value="Adds a platform to your profile .addplatform <pc/xbox/playstation/switch/vr>",inline=False)       

                embed.add_field(name=".platforms", value="Displays platforms of the person specified .platforms <member>",inline=False)
                embed.add_field(name=".specs", value="Displays specs of all or a specific part of their pc if they have one. .specs <member> <part> ",inline=False) 
                embed.add_field(name=".delplatform", value="Delete a platform",inline=False) 
                embed.add_field(name=".listplatforms <platform>", value="Lists everyone on a certain platform",inline=False)
                await ctx.send(embed=embed)    
            elif command == "birthdays":
                embed = discord.Embed(title="Birthdays",colour=self.colour)
                embed.add_field(name=".birthday set <date>", value="Set your birthday, in the value XX/XX (day then month, for example 30/05)",inline=False)
                embed.add_field(name=".birthday list <page>", value="List the birthdays in order of recent birthday",inline=False)
                embed.add_field(name=".birthday reset <user>", value="Reset your birthday (only admins can reset someone elses birthday)",inline=False)
                embed.add_field(name=".birthday <user>", value="Tells you a users birthday",inline=False)
                embed.add_field(name=".birthday channel <channel> (**Admin**)", value="Set the birthday announcements channel",inline=False)         
                embed.set_thumbnail(url=self.utility.boturl)
                embed.set_footer(text="Ben-bot | EliteNarNar#3447")
                embed.set_thumbnail(url=self.utility.boturl)
                await ctx.channel.send(embed=embed)

            elif command == "potd":
                embed = discord.Embed(title="Player of the day (**Admin**)",colour=self.colour)
                embed.add_field(name=".potd channel <channel>", value="Set the channel that the potd is announced in",inline=False)
                embed.add_field(name=".potd minimum-role <role>", value="Sets the minimum role to win player of the day",inline=False)
                embed.add_field(name=".potd winner-role", value="Sets the role that the winner gets.",inline=False)
                embed.add_field(name=".potd time", value="Set the time where potd are announced (it has to be full o'clock eg 16:00) its also in UTC <0-23>",inline=False)
                embed.add_field(name=".potd last-winner", value="If you want to set the last player of the day for some reason you can set it with this command",inline=False)
                embed.add_field(name=".potd custom-message", value="Set the custom message that is said when player of the day is announced. You can use {winnername} to use there name and {winnermention} to mention",inline=False)
                embed.set_thumbnail(url=self.utility.boturl)
                embed.set_footer(text="Ben-bot | EliteNarNar#3447")
                await ctx.channel.send(embed=embed)
                
            elif command == "settings":
                embed = discord.Embed(title="Settings (**Admin**)",colour=self.colour)
                embed.add_field(name=".settings dadjoke <on/off>", value="Turns the dadjoker on or off",inline=False)
                embed.add_field(name=".settings potd <on/off>", value="Turns the player of the day announcemnts on or off",inline=False)
                embed.add_field(name=".settings birthday <on/off>", value="List the birthdays in order of recent birthday",inline=False)
                embed.add_field(name=".settings reset <birthday, settings, all>", value="Delete, birthdays, server settings or both",inline=False)
                embed.set_thumbnail(url=self.utility.boturl)
                embed.set_footer(text="Ben-bot | EliteNarNar#3447")
                await ctx.channel.send(embed=embed)
            elif command == "events":
                embed = discord.Embed(title="Events",colour=self.colour)
                embed.add_field(name=".event start", value="Starts an event",inline=False)
                embed.add_field(name=".event cancel", value="Will cancel the event. This cannot be undone",inline=False)
                embed.add_field(name=".event link", value="This will link to the message of the event",inline=False)
                embed.add_field(name=".event edit", value="This will allow you to edit your event!", inline=False)

                embed.set_thumbnail(url=self.utility.boturl)
                embed.set_footer(text="Ben-bot | EliteNarNar#3447")
                await ctx.channel.send(embed=embed)                
    @commands.command(
    name="ping", help=("Mainly a development feature that tests if the bot is running")
)
    async def pingCommand(self, ctx):
        await ctx.channel.send(
            "Pong ({}ms)".format(round(self.bot.latency * 1000))
        )  # Shows bot latency
    
    @commands.command(name="repeat", help="Repeats a message!")
    async def repeatCommand(self, ctx, *, message):
        boolean = False
        aList = message.split()
        for x in range(len(aList)):
            # this combs through the list looking for the words "Im" or "I'm" so if the user tries to prank the bot the bot will know :D
            if aList[x] == "i'm" or aList[x] == "im" or aList[x] == "i":
                boolean = True
        if boolean == True:
            await ctx.channel.send("Lmao we know")  # Delivers a sick burn on the user
        if boolean == False:
            await ctx.channel.send(message)
            print(message)


    
    @tasks.loop(seconds=3600)
    async def nameChange(self):
        now = datetime.utcnow()
        adate = date.today()
        nowdate = adate.isocalendar()
        day = now.day
    
        await self.bot.wait_until_ready()
        nameList= ("Jess", "Brooke","Ben", "Aidan", "Lex", "Josh", "Will", "Laura", "Nana", "Tom", "Jack", "Katie")
        name = random.choice(nameList)
        await self.bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="{} O_O | .help".format(name))
            )  # Sets the bots status

        with open('resources/iteration.json', 'r') as F:
            iterations = json.load(F)

        if str(nowdate[2]) not in iterations.keys():
        
            iterations[str(nowdate[2])] = {"date": adate.isoformat()}
    
        elif iterations[str(nowdate[2])]["date"] != adate.isoformat():
            del iterations[str(nowdate[2])]
            iterations[f"{nowdate[2]}"] = {"date": adate.isoformat()}
          
        if name not in iterations[str(nowdate[2])].keys():
    
            iterations[str(nowdate[2])][name] = 1
      
        else:
            iterations[str(nowdate[2])][name]+=1
        print("Watching", name)

        with open('resources/iteration.json', 'w') as F:

            json.dump(iterations, F)
    @commands.command(name="watchstats")
    async def watchStatsCommand(self, ctx, day=None):
        days = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")
        adate = date.today()
        nowdate = adate.isocalendar()

        if day is None:
          
            day = nowdate[2]
            day = days[day-1]
        else:
            if day not in days:
                await ctx.send("Prefarably choose a day that actually exists, moron.")
                return          
            day = day.lower()
        print(day)
        

        dayInd = days.index(day)+1
        embed = discord.Embed(title=f"Watch stats for {day.title()}")
        with open('resources/iteration.json', 'r') as F:
            iterations = json.load(F) 
        total = 0
        counter = 0
        description = ""
        for k, v in iterations[str(dayInd)].items():
            if counter == 0:
                counter+=1
                continue
            description += f"**{k}** has been watched **{v}** times today\n"
            total +=v


        
        embed.add_field(name="Watch count", value=description)
        description = ""
        counter = 0
        for k, v in iterations[str(dayInd)].items():
            if counter == 0:
                counter+=1
                continue
            description += "Ben-bot has been watching **{0}** {1:.2f}% of the time\n".format(k, (v/total)*100)
        embed.add_field(name="Percentage watch", value=description)
        embed.colour = self.colour
        await ctx.send(embed=embed)
            
   




        
def setup(bot):     
    bot.add_cog(commands(bot))