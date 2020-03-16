import random

import discord
from discord.ext import commands
from discord.ext.commands import Context


class BasicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send("Welcome {0.mention".format(member))

    @commands.command()
    async def ping(self, ctx: Context):
        await ctx.send('pong')

    @commands.command()
    async def roll(self, ctx: Context):
        await ctx.send("{}".format(random.randint(1, 6)))


def setup(bot: commands.Bot):
    basic_cog = BasicCog(bot)
    bot.add_cog(basic_cog)
