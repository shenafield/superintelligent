import random
from datetime import datetime
from datetime import timedelta

import discord
from discord.ext import commands
from discord.utils import get


class NicknamerCog(commands.Cog):
    def __init__(self, bot, nicknamer, probablility=0.01, roles=None):
        self.bot = bot
        self.nicknamer = nicknamer
        self.probablility = probablility
        self.roles = roles

    @commands.Cog.listener()
    #main script, activates on detection of new message
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        responded_to = message.reference and (await message.channel.fetch_message(message.reference.message_id)).author
        if responded_to == self.bot.user or random.random() > self.probablility:
            return
        guild: discord.Guild = message.guild
        allowed = self.roles is None
        for role_id in self.roles or []:
            role = get(guild.roles, id=role_id)
            if role in message.author.roles:
                allowed = True
                break
        if not allowed:
            print("discarded: no role found")
            return
        chat = await message.channel.history(
            limit=20,
            after=datetime.now() - timedelta(minutes=15),
            before=message,
            oldest_first=True,
        ).flatten()
        chat = [message for message in chat if message.author.bot == False]
        if  not chat or chat[-1] != message:
            chat.append(message)
        
        nickname, explaination = self.nicknamer.comeupwith(chat)
        await message.author.edit(nick=nickname)
        await message.channel.send(f"I felt bored so I chose {message.author.mention} a new nickname - {nickname}.\nI chose this nickname because {explaination}.\n\nGimme money.")

@bot.command(description='Use this for a random rename.')
async def rename(message: discord.Message, ctx):
    guild: discord.Guild = message.guild
    nickname, explaination = self.nicknamer.comeupwith(chat)
    await message.author.edit(nick=nickname)
    await ctx.respond(f"I chose {message.author.mention} a new nickname - {nickname} because they're lazy and asked me to choose one for them.\nI chose this nickname because {explaination}.\n\nGimme money.")
