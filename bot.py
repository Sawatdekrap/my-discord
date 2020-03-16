import os

from discord.ext import commands

from config import COMMAND_PREFIX, BOT_TOKEN, HELP_COMMAND


bot = commands.Bot(command_prefix=COMMAND_PREFIX)


@bot.listen()
async def on_ready():
    print("Bot is ready.")


def load_cogs(bot: commands.Bot):
    for dir_entry in os.scandir('./cogs'):
        dir_name = dir_entry.name
        if dir_entry.is_dir() and dir_name != '__pycache__':
            print("Loading extension '{}'".format(dir_name))
            bot.load_extension("cogs.{}".format(dir_name))


if __name__ == '__main__':
    load_cogs(bot)
    bot.run(BOT_TOKEN, bot=True)
