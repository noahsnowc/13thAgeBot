import discord
from discord.ext import commands
import random

class Marv(commands.Cog, name="Marv"):
    """Class definition for Marv Cog."""
    responseFlag = 'Neutral'
    marvword = ['marv','roll','joke', 'scream', 'mean', 'state']

    Roller = ""

    def __init__(self, bot):
        self.bot = bot
        
    @commands.group(case_insensitive=True, help="Its Marv.")
    async def marv(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"What do you want, meatbag? I ain't got all day.")

    @marv.command(name='talk', help="Do I need to explain this meatbag?")
    async def marv_talk(self, ctx):
        await ctx.send(f"AAAAAAAAH")
    
    # ==============================
    # Message Response
    #  ==============================

    @commands.Cog.listener("on_message")
    async def respond(self, message):
        user_message =  message.content.lower()
        if message.author != self.bot.user and self.marvword[0] in user_message:
            print(self.responseFlag)
            await message.channel.send(self.marv_response(user_message))
        elif message.author != self.bot.user and self.responseFlag == 'Rolling':
            return

    
    def marv_response(self, message):
        if self.responseFlag == 'Neutral':
            if self.marvword[1] in message:
                print(self.responseFlag)
                return self.rolling_proc_message(message)
            elif self.marvword[2] in message:
                return "You're life. Laugh, fleshling."
            else:
                return "What do you want organic spare parts? I haven't got all day."
        if self.responseFlag == 'Rolling':
            return "What do you want organic spare parts? I haven't got all day."
        

    def rolling_proc_message(self, message):
        self.responseFlag = 'Rolling'
        return "What would you like to roll, meatbag?"    


def setup(bot):
    """Discord module required setup for Cog loading."""
    bot.add_cog(Marv(bot))