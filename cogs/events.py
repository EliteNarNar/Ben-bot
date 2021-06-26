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

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utility = self.bot.get_cog("utility")
        self.colour = self.utility.colour
    @commands.Cog.listener()
    async def on_ready(self):
        print("Events cog Loaded!")
    
        self.eventLoop.start()
        self.checkActivities.start() 
    class Event():
        def __init__(self, startTime, game, roles, channel, platforms, description, organiser, title, offset, maxMembers):
            self.startTime = startTime 
            self.game = game 
            self.acceptedMembers = None
            self.declinedMembers = None
            self.roles = roles
            self.channel = channel
            self.embed = None
            self.organiser = organiser
            self.title = title
            self.description = description
            self.platforms = platforms
            self.offset = offset
            self.maxMembers = maxMembers
            
    @commands.command("event")
    async def eventCommand(self, ctx, subCommand = None, confirm = None):
        user = ctx.author
        
        async def waitForMessage():
            def check(m):
                return m.author == ctx.author and m.channel == ctx.author.dm_channel
            try:             
                message = await self.bot.wait_for('message', timeout=300, check=check)
            except asyncio.TimeoutError:
                await ctx.author.dm_channel.send("Timed out.")
            return message.content
        if confirm is not None:
            if confirm.lower() == "confirm":
                confirmed = True
            else:
                confirmed = False
        else:
            confirmed = False
        subCommand = subCommand.lower()
        if subCommand is None:
            await ctx.send("You need a subcommand! do .help events!")
        elif subCommand == "cancel" and not confirmed:
            await ctx.send("Are you sure? do `.event cancel confirm` to confirm")
        elif subCommand == "cancel" and confirmed:
            if str(ctx.author.id) in self.utility.events[str(ctx.guild.id)]:
              try:
                  record = self.utility.events[str(ctx.guild.id)][str(ctx.author.id)]["event"]
                  guild = ctx.guild
                  channel = guild.get_channel(int(record["channel"]))
                  message = await channel.fetch_message(int(record["messageid"]))
                  await message.delete()
              except:
                  pass
              del self.utility.events[str(ctx.guild.id)][str(ctx.author.id)]
              await ctx.send("Event has been deleted")
        elif subCommand == "link":
            if str(ctx.guild.id) not in self.utility.events.keys():
                self.utility.events[str(ctx.guild.id)] = {}
            if str(ctx.author.id) not in self.utility.events[str(ctx.guild.id)].keys():
                await ctx.send("You dont have an event!")
                print(self.utility.events[str(ctx.guild.id)].keys())
                return
            event = self.utility.events[str(ctx.guild.id)][str(ctx.author.id)]["event"]
            embed = discord.Embed(title=event["title"])
            link = "https://discord.com/channels/"+str(ctx.guild.id)+ "/"+ str(event["channel"]) + "/" + str(event["messageid"])
            embed.description = f"You can find the details of this event [here]({link})"
            await ctx.send(embed=embed)
        elif subCommand == "edit":
            if str(ctx.guild.id) not in self.utility.events.keys():
                self.utility.events[str(ctx.guild.id)] = {}
            if str(ctx.author.id) not in self.utility.events[str(ctx.guild.id)].keys():
                await ctx.send("You dont have an event!")
                return 
            event = self.utility.events[str(ctx.guild.id)][str(ctx.author.id)]["event"]
            await ctx.author.create_dm()
            await ctx.author.dm_channel.send("What would you like to edit? fields: (title, time, game, description, maxmembers, roles, platforms)")
            
            message = await waitForMessage()
            message = message.lower()
            if message == "game":
                if self.utility.events[str(ctx.guild.id)][str(ctx.author.id)]["event"]["game"] == "None":
                    await ctx.author.dm_channel.send("Your event is a non-game event. To add a game cancel your event and make a new one")
                    return
                
                await ctx.author.dm_channel.send("What game do you want to change your event to?")
                game = await waitForMessage()
                event["game"] = game
                await ctx.author.dm_channel.send(f"Game has successfully been set to {game}!")
            elif message == "description":
                await ctx.author.dm_channel.send("What would you like the new description to be?")
                description = await waitForMessage()
                event["description"] = description
            elif message == "title":
                await ctx.author.dm_channel.send("What would you like the new title to be?")
                title = await waitForMessage()
                event["title"] = title
            elif message == "maxmembers":
                
                await ctx.author.dm_channel.send("What would you like the new maximum amount of members to be (-1 for unlimited)\nNote: editing this will clear people who have currently accepted!")
                message = await waitForMessage()
                try:
                    number = int(message)
                except:
                    await ctx.author.dm_channel.send("That isn't a number!")
                    return
                if number > 0 or number == -1:
                    event["maxMembers"] = number
                    event["acceptedMembers"] = []
                else:
                    await ctx.channel.send("You can set the maximum members to that value!")
            elif message == "time":
                await ctx.author.dm_channel.send("When would you like the event to start?\nMake sure its in this form: `DD/MM/YYYY HH:MM`for example 30/05/2021 14:35 ")
                message = await waitForMessage()
                dateMatch= re.match("(\d{2})\/(\d{2})\/(\d{4}) (\d{2}):(\d{2})", message)
                if dateMatch:

                    try:
                        ustartDate = datetime(int(dateMatch.group(3)), int(dateMatch.group(2)), int(dateMatch.group(1)), int(dateMatch.group(4)), int(dateMatch.group(5)))
                        
                    except ValueError as e:
                        await ctx.author.dm_channel.send("That isnt a valid time!")
                
                        return
                
                else:
                    await ctx.author.dm_channel.send("That does not match the syntax.")
                
                    return
                timz = event["startTime"][-1]    
                event["startTime"] = [int(dateMatch.group(3)), int(dateMatch.group(2)), int(dateMatch.group(1)), int(dateMatch.group(4)), int(dateMatch.group(5)), timz]
            elif message == "roles":
                await ctx.author.dm_channel.send("What roles can join the event? \nMake sure its in this form: `role1, role2, role3, etc...`\n or just type \"any\"")
                roles = await waitForMessage()
                if roles.lower() == "any":
                    roles = []
                else:
                    roles = roles.split(",")
                    newroles = [role.strip() for role in roles]
                    roles = []
                    valid = True
                    sValid = False
                    for role in newroles:
                        
                        for guildRole in ctx.guild.roles:
                            if role.lower() == guildRole.name.lower():
                                roles.append(guildRole.id)
                                sValid = True
                                break
                        if not sValid:
                            valid = False
                            break


                    
                    if not valid:
                        await ctx.author.dm_channel.send("One or more of these roles doesn't exist in the server!")
                        return 
                    event["roles"] = roles
            elif message == "platforms":
                    if event["game"] != "None":
                        await ctx.author.dm_channel.send("What platform(s) are you playing on. If its more than one make sure its in this form: xbox, playstation, pc etc")
                        platforms = await waitForMessage()
                        platforms = platforms.split(",")
                        
                        newplatforms = [platform.strip() for platform in platforms]
                        event["platforms"] = newplatforms

                    else:
                        await ctx.channel.send("Your event is a non-game event! To add a game cancel this event and make another one! ")                   
            startFrmt = "%Y-%m-%d %H:%M"
            embed = discord.Embed(title=event["title"], description=event["description"])
            startTime = datetime(event["startTime"][0],event["startTime"][1],event["startTime"][2],event["startTime"][3],event["startTime"][4])
            _timezone = pytz.timezone(event["startTime"][5])
            localStartDate = _timezone.localize(startTime)
            startTime = localStartDate.astimezone(_timezone)
            organiser = event["organiser"]
            game = event["game"]
            info = f"Organised by {ctx.guild.get_member(organiser).name}\nGame: {game}\n Platforms: "
            for platform in event["platforms"]:
                info +=(platform+",")
        
            infoList = [x for x in info]
            infoList.pop()
            newInfo = ""
            for x in infoList:
                newInfo+= x            
            
            guild = ctx.guild

            embed.add_field(name="Starts at:", value=startTime.strftime(startFrmt))
            embed.add_field(name="Info", value=newInfo)
            embed.colour = self.colour
            maxMembers = event["maxMembers"]
            
            acceptedMembers = ""
            for member in event["acceptedMembers"]:
                user = guild.get_member(int(member))
                acceptedMembers += f"{user.mention}\n"
            if acceptedMembers == "":
                acceptedMembers = "-"
            if event["maxMembers"] != -1:
                embed.add_field(name=f"Accepted (0/{maxMembers})", value=acceptedMembers,inline=False)
            else:
                embed.add_field(name=f"Accepted", value=acceptedMembers,inline=False)
            
            

            declinedMembers = ""
            for member in event["declinedMembers"]:
                user = guild.get_member(int(member))
                declinedMembers += f"{user.mention}\n"
            if declinedMembers == "":
                declinedMembers = "-"
            embed.add_field(name="Declined", value=declinedMembers)


            tentativeMembers = ""
            for member in event["declinedMembers"]:
                user = guild.get_member(int(member))
                tentativeMembers += f"{user.mention}\n"
            if tentativeMembers == "":
                tentativeMembers = "-"



            embed.add_field(name="Not Sure", value =tentativeMembers,inline=False)
            roleMentions = ""
            for role in event["roles"]:
                roleMentions += ctx.guild.get_role(role).mention + "\n"
            if roleMentions == "":
                roleMentions="Any role can join!"          
            embed.add_field(name="Required roles", value=roleMentions)
                    
            channel = self.bot.get_channel(int(event["channel"]))
            message = await channel.fetch_message(int(event["messageid"]))
            
            await ctx.author.dm_channel.send("Edited your event!")
            print(event)
            await message.edit(embed=embed, content=roleMentions)
        elif subCommand == "start" and not confirmed:
            await ctx.send("Are you sure you want to start an event? Do `.event start confirm` to confirm")

        elif subCommand == "start" and confirmed:
            await ctx.author.create_dm()
            if str(ctx.guild.id) not in self.utility.events.keys():
                self.utility.events[str(ctx.guild.id)] = {}
            if str(user.id) not in self.utility.events[str(ctx.guild.id)].keys():
                pass
            else:

                await ctx.author.dm_channel.send("You already have an event!")
                return               
                                
            ##########################################
            await ctx.author.dm_channel.send("What would you like the name of the event to be?")
            message = await waitForMessage()
            title = message
            await ctx.author.dm_channel.send("When would you like the event to start?\nMake sure its in this form: `DD/MM/YYYY HH:MM`for example 30/05/2021 14:35 ")
            message = await waitForMessage()
            dateMatch= re.match("(\d{2})\/(\d{2})\/(\d{4}) (\d{2}):(\d{2})", message)
            if dateMatch:

              try:
                ustartDate = datetime(int(dateMatch.group(3)), int(dateMatch.group(2)), int(dateMatch.group(1)), int(dateMatch.group(4)), int(dateMatch.group(5)))
                
              except ValueError as e:
                await ctx.author.dm_channel.send("That isnt a valid time!")
         
                print(e)
                return
            
            else:
                await ctx.author.dm_channel.send("That does not match the syntax.")
                return
            now = datetime.utcnow()
            frmt= "%Y-%m-%d %H:%M"
            await ctx.author.dm_channel.send(f"How many hours are you away from UTC? Its currently {now.strftime(frmt)} UTC\n Note: if timezones change when the events start time will be incorrect. If they change enter how many hours away from UTC you are when the event starts. ")
            message = await waitForMessage()

            try:
                if int(message) >= -14 and int(message) <= 14:
                  number = int(message)
                  if int(message) > 0:
                      _timezone = "Etc/GMT+" + str(number)
                  else:
                      _timezone = "Etc/GMT" + str(number)
                  offset = int(message)
            except ValueError:
                await ctx.author.dm_channel.send("That is not a number!")
            
                

            startList = [int(dateMatch.group(3)), int(dateMatch.group(2)), int(dateMatch.group(1)), int(dateMatch.group(4)), int(dateMatch.group(5)), _timezone]
            #############################
           
            ######################
           
            await ctx.author.dm_channel.send("What game is the event on? You can type \"none\" if you would like.")

            game = await waitForMessage()
            if game.lower() == "none":
                game = "None"
            ############################
            await ctx.author.dm_channel.send("What roles can join the event? \nMake sure its in this form: `role1, role2, role3, etc...`\n or just type \"any\"")
            roles = await waitForMessage()
            if roles.lower() == "any":
                roles = []
            else:
                roles = roles.split(",")
                newroles = [role.strip() for role in roles]
                roles = []
                valid = True
                sValid = False
                for role in newroles:
                    
                    for guildRole in ctx.guild.roles:
                        if role.lower() == guildRole.name.lower():
                            roles.append(guildRole.id)
                            sValid = True
                            break
                    if not sValid:
                        valid = False
                        break


                
                if not valid:
                    await ctx.author.dm_channel.send("One or more of these roles doesn't exist in the server!")
                    return


            #############################
            await ctx.author.dm_channel.send("How many members are allowed to join? say -1 for unlimited")
            message = await waitForMessage()
            try:
                maxMembers = int(message)
                if maxMembers <-1:
                    await ctx.author.dm_channel.send("That isn't a valid number")
                    return
            except:
                await ctx.author.dm_channel.send("That isnt a number!")
            
            #############################
            await ctx.author.dm_channel.send("What is the name of the channel you want the event message to be sent in? (this needs to be exact)")
            message = await waitForMessage()
            converter = commands.TextChannelConverter()
            try:
                channel=await converter.convert(ctx=ctx, argument=message.lower())
            except Exception as e:
                await ctx.author.dm_channel.send("This channel does not exist")
                print(e) 
                return
            ############################

            if game != "None":
                await ctx.author.dm_channel.send("What platform(s) are you playing on. If its more than one make sure its in this form: xbox, playstation, pc etc")
                platforms = await waitForMessage()
                platforms = platforms.split(",")
                newplatforms = [platform.strip() for platform in platforms]
            else:
                newplatforms = ["N/A"]
            ###############################
            
            await ctx.author.dm_channel.send("What would you like the description of the event to be?")
            description = await waitForMessage()

            newEvent = self.Event(roles=roles, description=description, startTime=startList,game=game,channel=channel.id, organiser = ctx.author.id, title=title, platforms=newplatforms, offset=offset, maxMembers=maxMembers)
            self.utility.events[str(ctx.guild.id)][str(user.id)] = {"event": {"roles": newEvent.roles, "description": newEvent.description, 
            "startTime": newEvent.startTime,  "game": newEvent.game, "channel": newEvent.channel, "organiser": newEvent.organiser, "title": newEvent.title,
             "platforms": newEvent.platforms,"offset": newEvent.offset, "maxMembers": maxMembers, "acceptedMembers": [], "declinedMembers": [], "tentativeMembers": []}}

            embed = discord.Embed(title=newEvent.title, description=newEvent.description)
            info = f"Organised by {ctx.guild.get_member(newEvent.organiser).name}\nGame: {newEvent.game}\n Platforms: "
            for platform in newEvent.platforms:
                info +=(platform+",")
            
            infoList = [x for x in info]
            infoList.pop()
            newInfo = ""
            for x in infoList:
                newInfo+= x

           
            startFrmt = "%Y-%m-%d %H:%M"
         
            startTime = datetime(newEvent.startTime[0],newEvent.startTime[1],newEvent.startTime[2],newEvent.startTime[3],newEvent.startTime[4])
            _timezone = pytz.timezone(newEvent.startTime[5])
            localStartDate = _timezone.localize(ustartDate)
            startTime = localStartDate.astimezone(_timezone)            
            
            

            embed.add_field(name="Starts at:", value=startTime.strftime(startFrmt))
            embed.add_field(name="Info", value=newInfo)
            embed.colour = self.colour
            if newEvent.maxMembers != -1:
                embed.add_field(name=f"Accepted (0/{newEvent.maxMembers})", value="-",inline=False)
            else:
                 embed.add_field(name=f"Accepted", value="-",inline=False)
            embed.add_field(name="Declined", value="-")
            embed.add_field(name="Not Sure", value ="-",inline=False)
            roleMentions = ""
            for role in newEvent.roles:
                roleMentions += ctx.guild.get_role(role).mention + "\n"
            if roleMentions == "":
                roleMentions="Any role can join!"          
            embed.add_field(name="Required roles", value=roleMentions)

            message = await ctx.guild.get_channel(newEvent.channel).send(content=roleMentions, embed=embed)
            self.utility.events[str(ctx.guild.id)][str(user.id)]["event"]["messageid"]= message.id
            await message.add_reaction("✅")
            await message.add_reaction("❌")
            await message.add_reaction("❓")
            
            


                        
    @tasks.loop(seconds = 60)
    async def eventLoop(self):
        for guildId, events in self.utility.events.items():
            for member, event in events.items():
                eventList = event["event"]["startTime"]
                eventStart = datetime(eventList[0], eventList[1], eventList[2], eventList[3], eventList[4])
               
                _timezone = pytz.timezone(eventList[5])
                localStart = _timezone.localize(eventStart)
                eventStart = localStart.astimezone(_timezone)
                offset = event["event"]["offset"]
                
                now =  datetime.utcnow()
                localNow = _timezone.localize(now)
                now = localNow.astimezone(_timezone)
      
                aminute = eventStart.minute - 10
                ahour = eventStart.hour
                aday = eventStart.day
                amonth = eventStart.month
                ayear = eventStart.year
                def correctTime(minute, hour, day, month, year):
                    if minute < 0:
                        minute = 60+minute
                        hour -= 1
                        if hour <0:
                            hour = 24+hour
                            day-=1
                            if day <0:
                                if month in [9, 4, 6, 11]:
                                    day = 30 + day
                                elif month == 2:
                                    if year%4 == 0:
                                        day = 29 + day
                                    else: 
                                        day = 28 + day
                                else:
                                    day = 31 + day
                                month -=1
                                if month <0:
                                    month = 11
                                    year-=1
                    return minute, hour, day, month, year

                minute, hour, day, month, year = correctTime(aminute, ahour, aday, amonth, ayear)
                aminute = eventStart.minute 
                ahour = eventStart.hour -1
                aday = eventStart.day
                amonth = eventStart.month
                ayear = eventStart.year                            

                bminute, bhour, bday, bmonth, byear = correctTime(aminute, ahour, aday, amonth, ayear)
 

                if (now.minute == minute) and (now.year == year and now.month == month and now.hour+offset == hour and day== now.day):
                    guild = self.bot.get_guild(int(guildId))

                    for member in event["event"]["acceptedMembers"]:
                        person = guild.get_member(int(member))
                        await person.create_dm()
                        title = event["event"]["title"]
                        await person.dm_channel.send(f"The event **\"{title}\"**, is starting in 10 minutes")

                elif now.minute == bminute and now.year == byear  and now.month == bmonth and bhour == now.hour+offset and bday ==now.day:
                    guild = self.bot.get_guild(int(guildId))
                    title = event["event"]["title"]
                    for member in event["event"]["acceptedMembers"]:
                          person = guild.get_member(int(member))
                          await person.create_dm()
                          await person.dm_channel.send(f'The event **"{title}"** starts in one hour!')                   


                                            
                elif now.minute == eventStart.minute and now.year == eventStart.year and now.month == eventStart.month and now.hour+offset == eventStart.hour:
                    guild = self.bot.get_guild(int(guildId))
                    title = event["event"]["title"]
                    for member in event["event"]["acceptedMembers"]:
                          person = guild.get_member(int(member))
                          await person.create_dm()
                          await person.dm_channel.send(f'The event **"{title}"** starts now!')                   
                    await asyncio.sleep(300)
                    record = event["event"]
                    
                    channel = guild.get_channel(int(record["channel"]))
                    message = await channel.fetch_message(int(record["messageid"]))
                    await message.delete()
              
                    del self.utility.events[str(guild.id)][str(member)]
                    

    @eventLoop.before_loop
    async def before_eventLoop(self):
        await self.bot.wait_until_ready()
        
        now = datetime.utcnow()
        future = datetime(now.year, now.month, now.day, now.hour, now.minute+1, 0, 0)
        logger.debug("Events sleeping for {} seconds".format((future - now).seconds))
        await asyncio.sleep((future - now).seconds+1)
        

    @tasks.loop(seconds=2)
    async def checkActivities(self):
        
        for guildId, events in self.utility.events.items():
            for member, event in events.items():
                event = event["event"]
             
                guild = self.bot.get_guild(int(guildId))
                channel = guild.get_channel(int(event["channel"]))
                try:
                   message = await channel.fetch_message(int(event["messageid"]))
                except:

                  continue
                acceptedMembers = ""
                for member in event["acceptedMembers"]:
                    participant = guild.get_member(int(member))
                    
                    valid = False
                    for activity in participant.activities:
                        if event["game"].lower() in activity.name.lower():
                            acceptedMembers+= participant.mention+ " **in game!**\n"
                            valid = True
                    if not valid:
                        acceptedMembers+= participant.mention + "\n"
                  
                embed = message.embeds[0]
                embed.remove_field(2)
                membersAccepted = len(event["acceptedMembers"])
                maxMembers = event["maxMembers"]
                if acceptedMembers == "":
                    acceptedMembers = "-"
                if event["maxMembers"] != -1:
                    embed.insert_field_at(2,name=f"Accepted ({membersAccepted}/{maxMembers})",value=acceptedMembers, inline=False)
              
                else:
                    embed.insert_field_at(2,name=f"Accepted",value=acceptedMembers, inline=False) 
                                          
                await message.edit(embed=embed)
       


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        theEvent = None
        if payload.user_id == 384444248214208522 or payload.user_id == 803623248146595860:
            return
        if str(payload.emoji) == "❌" or str(payload.emoji) == "✅" or str(payload.emoji) == "❓":
        
            if str(payload.member.guild.id) in self.utility.events:
                for member, event in self.utility.events[str(payload.member.guild.id)].items():
            
                    if payload.message_id == int(event["event"]["messageid"]):
                        
                        theEvent = self.utility.events[str(payload.member.guild.id)][member]["event"]
                        break

                if theEvent is None:
                    return
      
                channel = self.bot.get_channel(int(theEvent["channel"]))
                message = await channel.fetch_message(int(theEvent["messageid"]))
                guild = self.bot.get_guild(payload.guild_id)
                member = guild.get_member(payload.user_id)
                
                embed = message.embeds[0]
                if str(payload.emoji) == "❌":
                    if payload.user_id in theEvent["acceptedMembers"] or payload.user_id in theEvent["tentativeMembers"]:
                        await message.remove_reaction(payload.emoji, member)
                        return
                    theEvent["declinedMembers"].append(payload.member.id)
                    declinedMembers = ""
                    for member in theEvent["declinedMembers"]:
                        user = self.bot.get_guild(payload.guild_id).get_member(int(member))
                        declinedMembers += f"{user.mention}\n"
                        
                    embed.remove_field(3)
                    embed.insert_field_at(3,name="Declined",value=declinedMembers,inline=False)
                  
                elif str(payload.emoji) == "✅":
                    if payload.user_id in theEvent["declinedMembers"] or payload.user_id in theEvent["tentativeMembers"]:
                        await message.remove_reaction(payload.emoji, member)
                        return 
                    valid = True
                    if len(theEvent["roles"]) != 0:
                        for role in theEvent["roles"]:
                            guild.get_role(int(role))
                            if guild.get_role(int(role)) not in member.roles:
                                valid = False
                    if valid:
                        if len(theEvent["acceptedMembers"])  != theEvent["maxMembers"]:
                            
                            theEvent["acceptedMembers"].append(payload.member.id)
                            acceptedMembers = ""
                            for member in theEvent["acceptedMembers"]:
                                user = self.bot.get_guild(payload.guild_id).get_member(int(member))
                                acceptedMembers += f"{user.mention}\n"
                                

                            embed.remove_field(2)
                            membersAccepted = len(theEvent["acceptedMembers"])
                            maxMembers = theEvent["maxMembers"]
                            if theEvent["maxMembers"] != -1:
                                embed.insert_field_at(2,name=f"Accepted ({membersAccepted}/{maxMembers})",value=acceptedMembers, inline=False)
                            else:
                                embed.insert_field_at(2,name=f"Accepted",value=acceptedMembers, inline=False)                         
                        else:
                            await message.remove_reaction(payload.emoji, member)
                            await channel.send(content=f"{member.mention}! The max amount of people have already joined!", delete_after=3)
                            return
                    else:
                        await message.remove_reaction(payload.emoji, member)
                        await channel.send(content=f"{member.mention}! You don't have one or more of the roles needed to join the event!", delete_after=3)
                        return                       
                elif str(payload.emoji) == "❓":
                    if payload.user_id in theEvent["acceptedMembers"] or payload.user_id in theEvent["declinedMembers"] :
                        await message.remove_reaction(payload.emoji, member)
                        return                    
                    theEvent["tentativeMembers"].append(payload.member.id)
                    tentativeMembers = ""
                    for member in theEvent["tentativeMembers"]:
                        user = self.bot.get_guild(payload.guild_id).get_member(int(member))
                        tentativeMembers += f"{user.mention}\n"
                        

                    embed.remove_field(4)
                    embed.insert_field_at(4,name="Not Sure",value=tentativeMembers, inline=False)    
                await message.edit(embed=embed)      
                
        else:
            for member, event in self.utility.events[str(payload.member.guild.id)].items():
            
                if payload.message_id == int(event["event"]["messageid"]):
                        
       
                    guild = self.bot.get_guild(payload.guild_id)
                    channel = guild.get_channel(payload.channel_id)
                    message = await channel.fetch_message(payload.message_id)
                    await message.remove_reaction(payload.emoji, payload.member)
                    return
               


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id == 384444248214208522 or payload.user_id == 803623248146595860:
            return        
            
        if str(payload.emoji) == "❌" or str(payload.emoji) == "✅" or str(payload.emoji) == "❓":
            
            if str(payload.guild_id) in self.utility.events:
                theEvent = None
                for member, event in self.utility.events[str(payload.guild_id)].items():
                    if payload.message_id == int(event["event"]["messageid"]):
                        theEvent = self.utility.events[str(payload.guild_id)][member]["event"]
                        break

                if theEvent is None:
                    return
                channel = self.bot.get_channel(int(theEvent["channel"]))
                message = await channel.fetch_message(int(theEvent["messageid"]))
                embed = message.embeds[0]
                try:
                      if str(payload.emoji) == "❌":
                          theEvent["declinedMembers"].remove(payload.user_id)
                          declinedMembers = ""
                          for member in theEvent["declinedMembers"]:
                              user = self.bot.get_guild(payload.guild_id).get_member(int(member))
                              declinedMembers += f"{user.mention}\n"
                          if len(theEvent["declinedMembers"]) == 0:
                              declinedMembers = "-"                        
                          embed.remove_field(3)
                          embed.insert_field_at(3,name="Declined",value=declinedMembers, inline=False)
                      
                      
                      elif str(payload.emoji) == "✅":
                          theEvent["acceptedMembers"].remove(payload.user_id)
                          acceptedMembers = ""
                          for member in theEvent["acceptedMembers"]:
                              user = self.bot.get_guild(payload.guild_id).get_member(int(member))
                              acceptedMembers += f"{user.mention}\n"
                          if len(theEvent["acceptedMembers"]) == 0:
                              acceptedMembers = "-"

                          embed.remove_field(2)
                          membersAccepted = len(theEvent["acceptedMembers"])
                          maxMembers = theEvent["maxMembers"]
                          if maxMembers != -1:
                              embed.insert_field_at(2,name=f"Accepted ({membersAccepted}/{maxMembers})",value=acceptedMembers, inline=False)
                          else:
                              embed.insert_field_at(2,name=f"Accepted",value=acceptedMembers, inline=False)               
                      elif str(payload.emoji) == "❓":
                          theEvent["tentativeMembers"].remove(payload.user_id)
                          tentativeMembers = ""
                          for member in theEvent["tentativeMembers"]:
                              user = self.bot.get_guild(payload.guild_id).get_member(int(member))
                              tentativeMembers += f"{user.mention}\n"
                          if len(theEvent["tentativeMembers"]) == 0:
                              tentativeMembers = "-"

                          embed.remove_field(4)
                          embed.insert_field_at(4,name="Not Sure",value=tentativeMembers, inline=False)                          
                except:
                    pass
                await message.edit(embed=embed)


def setup(bot):
    bot.add_cog(Events(bot))
