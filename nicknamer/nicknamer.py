import discord
from complete import Complete


class Nicknamer:
    def __init__(self, complete: Complete, prefix):
        self.complete = complete
        self.prefix = prefix

    async def comeupwith(self, chat: list[discord.Message]):
        subject = chat[-1].author
        placeholder = "[subject]"
        representation = "\n".join(
            f"{placeholder if message.author == subject else message.author.display_name}: {message.content}" for message in chat
        )

        # We don't want it to choose a nickname that has already been used
        names = []
        for member in set(message.author for message in chat):
            if isinstance(member, discord.User):
                member = await chat[-1].guild.fetch_member(member.id)
            if isinstance(member, discord.Member) and member.nick:
                names += member.nick.split(" ")
            names += member.name.split(" ")
        tokens = sum(([token["generatedToken"]["token"] for token in self.complete.predict(name, maxTokens=0)["prompt"]["tokens"]] for name in set(names)), [])
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
        nickname = self.complete.complete(prompt, stopSequences=[".", "\n"], maxTokens=4).strip()
        explaination = self.complete.complete(prompt + nickname + continuation, stopSequences=[".", "\n"], maxTokens=32, bias=bias)
        print(prompt + nickname + continuation + explaination)
        return nickname, explaination
