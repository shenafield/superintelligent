import random
from datetime import datetime
from datetime import timedelta
from typing import Optional

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
    async def on_message(self, message: discord.Message):
        """This triggers when the bot sees a message anywhere"""
        if message.author.bot:
            # We don't want to change other bots' nicknames
            return
        # Check if this is someone yelling at the bot
        responded_to = (
            message.reference
            and (
                await message.channel.fetch_message(message.reference.message_id)
            ).author
        )
        # When to not trigger
        if responded_to != self.bot.user and random.random() > self.probablility:
            return

        # Does thie member have the role that allows us to change their nickname?
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

        chat = await self.get_chat(message.channel, message)
        nickname, explaination = await self.nicknamer.comeupwith(chat)
        await message.author.edit(nick=nickname)
        await message.channel.send(
            f"I felt bored so I chose {message.author.mention} a new nickname - {nickname}.\nI chose this nickname because {explaination}.\n\nGimme money."
        )

    @commands.slash_command(description="Get a brand new nickname")
    async def nickme(self, ctx):
        await ctx.defer()
        chat = await self.get_chat(ctx.channel)
        nickname, explaination = await self.nicknamer.comeupwith(chat)
        try:
            await ctx.author.edit(nick=nickname)
            await ctx.respond(
                f"I was asked to choose {ctx.author.mention} a new nickname - {nickname}.\nI chose this nickname because {explaination}.\n\nGimme money."
            )
        except discord.errors.Forbidden:
            await ctx.respond(
                "Failed to change your nickname; I might not have the permissions to do it",
                ephemeral=True,
            )

    async def get_chat(
        self, channel: discord.TextChannel, message: Optional[discord.Message] = None
    ):
        """Get the list of messages in the chat given the trigger one"""
        chat = await channel.history(
            limit=20,
            after=datetime.now() - timedelta(minutes=15) if message else None,
            before=message,
            oldest_first=True,
        ).flatten()
        chat = [message for message in chat if not message.author.bot]
        if message and (not chat or chat[-1] != message):
            chat.append(message)
        return chat
