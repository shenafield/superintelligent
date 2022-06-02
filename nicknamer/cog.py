import random
from datetime import datetime
from datetime import timedelta

from discord.ext import commands


class NicknamerCog(commands.Cog):
    def __init__(self, bot, nicknamer, probablility=0.01):
        self.bot = bot
        self.nicknamer = nicknamer
        self.probablility = probablility

    @commands.Cog.listener()
    @commands.has_role(981720280592420914) #  I'm too lazy to not hard code it
    async def on_message(self, message):
        if message.author.bot:
            return
        if random.random() > self.probablility:
            return
        chat = await message.channel.history(
            limit=20,
            after=datetime.now() - timedelta(minutes=15),
            before=message,
            oldest_first=True,
        ).flatten()
        chat = [message for message in chat if not message.author.bot]
        if not chat or chat[-1] != message:
            chat.append(message)
        nickname, explaination = self.nicknamer.comeupwith(chat)
        await message.author.edit(nick=nickname)
        await message.channel.send(f"I felt bored so I chose {message.author.mention} a new nickname - {nickname}.\nI chose this nickname because {explaination}.\n\nGimme money.")
