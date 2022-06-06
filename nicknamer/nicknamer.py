import discord
from complete import Complete
import functools


class Nicknamer:
    def __init__(self, complete: Complete, prefix):
        self.complete = complete
        self.prefix = prefix

    @functools.cache
    def tokens_for_string(self, string: str):
        return [
            token["generatedToken"]["token"]
            for token in self.complete.predict(string, maxTokens=0)["prompt"]["tokens"]
        ]

    async def comeupwith(self, chat: list[discord.Message], subject: discord.User):
        placeholder = "[subject]"
        representation = "\n".join(
            f"{placeholder if message.author.id == subject.id else message.author.display_name}: {message.content}"
            for message in chat
        )

        # We don't want it to choose a nickname that has already been used
        names = []
        for member in set(message.author for message in chat):
            if isinstance(member, discord.User):
                try:
                    member = await chat[-1].guild.fetch_member(member.id)
                except discord.errors.NotFound:
                    pass  #  The member wasn't found
            if isinstance(member, discord.Member) and member.nick:
                names += member.nick.split(" ")
            names += member.name.split(" ")
        tokens = sum(
            (self.tokens_for_string(name) for name in set(names)),
            [],
        )
        bias = {token: -100 for token in set(tokens)}

        prompt = (
            self.prefix
            + representation
            + f"""
        
        {placeholder} needs a new nickname. What should that nickname be?
        Their nickname should be """
        )
        continuation = """
        I chose this nickname because """
        nickname = self.complete.complete(
            prompt,
            stopSequences=[".", "\n"],
            maxTokens=4,
            bias=bias,
        ).strip()
        explaination = self.complete.complete(
            prompt + nickname + continuation,
            stopSequences=[".", "\n"],
            maxTokens=32,
        )
        print(prompt + nickname + continuation + explaination)
        return nickname, explaination
