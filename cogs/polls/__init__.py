import random

from discord.ext import commands
from discord.ext.commands import Context
from discord import Forbidden, NotFound
from emoji.unicode_codes import UNICODE_EMOJI

from .checks import is_guild


class Poll:
    def __init__(self, multi, question, answer_list, emoji_list):
        self.message_id = None
        self.multi = multi
        self.question = question
        self.answer_list = answer_list
        self.emoji_list = emoji_list

    async def send_to_context(self, ctx: Context):
        message = await ctx.send(self)
        if self.message_id is None:
            self.message_id = message.id

        for emoji in self.emoji_list:
            await message.add_reaction(emoji)

    def __str__(self):
        poll_text = "**{}?**\n".format(self.question)
        for answer, emoji in zip(self.answer_list, self.emoji_list):
            poll_text += "{} {}\n".format(emoji, answer)
        return poll_text


class PollsCog(commands.Cog):
    USAGE_MESSAGE = '!poll <question_text>? <answer> [, <answer> ]*'
    EMOJI_LIST = list(UNICODE_EMOJI.keys())

    def __init__(self, bot):
        self.bot = bot
        self.server_polls = {}

    @commands.command()
    @is_guild()
    async def poll(self, ctx, *args):
        """Create a new poll"""
        multi = True  # TODO source this from user in command

        # Join all words and then split on newline to form question and answers
        text = ' '.join(args)
        if '?' not in text:
            await ctx.send(self.USAGE_MESSAGE)
        question, answer_text = text.split('?')
        question = question.strip()
        answers = [a.strip() for a in answer_text.split(',')]
        if len(answers) == 0:
            await ctx.send(self.USAGE_MESSAGE)
        answer_emoji = [self.EMOJI_LIST[random.randint(0, len(self.EMOJI_LIST))] for _ in range(len(answers))]
        poll = Poll(multi=multi, question=question, answer_list=answers, emoji_list=answer_emoji)
        await poll.send_to_context(ctx)

        # Add poll to local storage
        server_id = ctx.guild.id
        if server_id not in self.server_polls:
            self.server_polls[server_id] = {}
        self.server_polls[server_id][poll.message_id] = poll

    async def on_reaction(self, reaction, user):
        if user.id == self.bot.user.id:
            return

        message = reaction.message
        guild = message.guild
        if guild and guild.id in self.server_polls and message.id in self.server_polls[guild.id]:
            poll = self.server_polls[guild.id][message.id]
            if reaction.emoji not in poll.emoji_list:
                try:
                    await reaction.remove(user)
                except (Forbidden, NotFound) as e:
                    # Not able to clear the reaction - just leave it
                    print('Unable to remove invalid reaction from poll')
                    pass


def setup(bot: commands.Bot):
    basic_cog = PollsCog(bot)
    bot.add_cog(basic_cog)
    bot.add_listener(basic_cog.on_reaction, 'on_reaction_add')
