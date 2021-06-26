
from discord.ext import commands, tasks
class tripp(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        tripp = self.bot.get_guild(720323009503690762)
        if payload.message_id == 804023056250044436:
            if payload.emoji.id == 804017815366402088:
                role = tripp.get_role(804034175752732724)

            elif payload.emoji.id == 804020819164528671:
                role = tripp.get_role(804034258720915496)

            elif payload.emoji.id == 804019003487289344:
                role = tripp.get_role(804033851868577802)

            elif payload.emoji.id == 804021373441015848:
                role = tripp.get_role(804034042390642789)

            elif payload.emoji.id == 804019601322147870:
                role = tripp.get_role(804033980877111306)

            elif payload.emoji.id == 804016716458754053:
                role = tripp.get_role(804033618912739328)

            elif payload.emoji.id == 804018603774443530:
                role = tripp.get_role(804034666146562069)

            elif payload.emoji.id == 804017270443212861:
                role = tripp.get_role(804034752520781884)
                
            elif payload.emoji.id == 804427060525006848:
                role = tripp.get_role(804427779428712468)

            elif payload.emoji.id == 804428564714749962: # gta
                role = tripp.get_role(804428610357297152)

            elif payload.emoji.id == 804429359733669928: # lol
                role = tripp.get_role(804429560916475954)

            elif payload.emoji.id == 804429423729311775: # DBD
                role = tripp.get_role(804429615346352148)

            elif payload.emoji.id == 804427088219734017: #SOT
                role = tripp.get_role(804427544715591722) 

            elif payload.emoji.id == 804427484816605254: #OSU
                role = tripp.get_role(804427660528713758) 
                
            await payload.member.add_roles(role)
            await payload.member.create_dm()
            await payload.member.dm_channel.send((role.name + " role given!"))


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        tripp = self.bot.get_guild(720323009503690762)
        member = tripp.get_member(payload.user_id)
        if payload.message_id == 804023056250044436:
            if payload.emoji.id == 804017815366402088:
                role = tripp.get_role(804034175752732724)

            elif payload.emoji.id == 804020819164528671:
                role = tripp.get_role(804034258720915496)

            elif payload.emoji.id == 804019003487289344:
                role = tripp.get_role(804033851868577802)

            elif payload.emoji.id == 804021373441015848:
                role = tripp.get_role(804034042390642789)

            elif payload.emoji.id == 804019601322147870:
                role = tripp.get_role(804033980877111306)

            elif payload.emoji.id == 804016716458754053:
                role = tripp.get_role(804033618912739328)

            elif payload.emoji.id == 804018603774443530:
                role = tripp.get_role(804034666146562069)

            elif payload.emoji.id == 804017270443212861:
                role = tripp.get_role(804034752520781884)

            elif payload.emoji.id == 804427060525006848:
                role = tripp.get_role(804427779428712468)

            elif payload.emoji.id == 804428564714749962: # gta
                role = tripp.get_role(804428610357297152)
                
            elif payload.emoji.id == 804429359733669928: # lol
                role = tripp.get_role(804429560916475954)

            elif payload.emoji.id == 804429423729311775: # DBD
                role = tripp.get_role(804429615346352148)

            elif payload.emoji.id == 804427088219734017: #SOT
                role = tripp.get_role(804427544715591722) 

            elif payload.emoji.id == 804427484816605254: #OSU
                role = tripp.get_role(804427660528713758) 

            await member.remove_roles(role)
            await member.create_dm()
            await member.dm_channel.send((role.name + " role removed."))
    @commands.Cog.listener()
    async def on_ready(self): 
        print("Tripp specific cog has been loaded")
def setup(bot):     
    bot.add_cog(tripp(bot))