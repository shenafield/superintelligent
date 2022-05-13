import time
from datetime import datetime
from datetime import timedelta

from discord.ext import commands


class ExplainerCog(commands.Cog):
    def __init__(self, bot, explainer):
        self.bot = bot
        self.explainer = explainer

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if "sorry" not in message.content:
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
        explaination = self.explainer.explain(chat)
        dynos_msg = None
        carls_id = 235148962103951360
        start = time.time()
        while not carls_msg and time.time() - start < 15:
            chat = message.channel.history(after=message)
            async for processed in chat:
                if processed.author.id == carls_id:
                    carls_msg = processed
        await carls_msg.reply(explaination + "\n\nCarl u dumbass")
