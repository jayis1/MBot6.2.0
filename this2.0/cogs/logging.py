import discord
from discord.ext import commands
import logging

class LoggingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger('discord')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename='bot_activity.log', encoding='utf-8', mode='w')
        handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
        self.logger.addHandler(handler)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        self.logger.info(f"Message from {message.author}: {message.content}")

    @commands.Cog.listener()
    async def on_command(self, ctx):
        self.logger.info(f"Command '{ctx.command}' invoked by {ctx.author}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        self.logger.error(f"Command '{ctx.command}' raised an error: {error}")

async def setup(bot):
    await bot.add_cog(LoggingCog(bot))
