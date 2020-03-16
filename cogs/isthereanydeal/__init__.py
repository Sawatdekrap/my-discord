import re

import discord
from discord.ext import commands
from discord.ext.commands import Context

from .deals import get_info_from_game_title
from .formatter import get_info_embed


class DealCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='isthereanydeal')
    async def deal(self, ctx: Context, *args):
        searched_game_title = ' '.join(args)[:100]
        info = get_info_from_game_title(searched_game_title)
        embed = get_info_embed(info, searched_game_title)
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    basic_cog = DealCog(bot)
    bot.add_cog(basic_cog)
