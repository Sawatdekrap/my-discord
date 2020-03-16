from discord.ext import commands


def is_guild():
    async def predicate(ctx):
        return ctx.guild
    return commands.check(predicate)
