import discord
from discord import Embed
from discord import FFmpegPCMAudio
import asyncio
from discord.ext import commands
class voicechat(commands.Cog):
    def __init__(self, bot):
      self.bot = bot

    

    @commands.Cog.listener()
    async def on_ready(self):
        print("Voice chat client cog has been loaded\n==============================\n\n")
    
    @commands.command(name="join")
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
          await ctx.send("You aren't in a voice channel!")
    @commands.command(name="sfx")
    async def soundFXCommand(self, ctx,*, effect):
        effect = effect.lower()
        if ctx.author.voice:

            channel = ctx.author.voice.channel
            voice= await channel.connect()     
          
            if effect == "wtf":
                source = FFmpegPCMAudio('resources/wtf.mp3')
            elif effect == "my cock":
                source = FFmpegPCMAudio('resources/mycock.mp3')

            player = voice.play(source)
            await asyncio.sleep(5)
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.send("You aren't in a voice channel!")
    @commands.command(name="leave")
    async def leave(self, ctx):
        if ctx.voice_client:
          await ctx.guild.voice_client.disconnect()
        else:
          await ctx.send("I'm not in a voice channel!!!")

      
   ## @commands.Cog.listener()
  #  async def on_voice_state_update(self, member, before, after):
    #  if member.id == 339866237922181121:
       # if before.channel is None:
 
          #  channel = after.channel
          #  voice = await channel.connect()
         #   source = FFmpegPCMAudio("resources/applause.wav")
            #voice.play(source)
          #  await asyncio.sleep(5)
           # await #member.guild.voice_client.disconnect#()






def setup(bot):
  bot.add_cog(voicechat(bot))




