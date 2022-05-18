import discord
from complete import Complete


class Nicknamer:
    def __init__(self, complete: Complete, prefix):
        self.complete = complete
        self.prefix = prefix

    def comeupwith(self, chat: list[discord.Message]):
        subject = chat[-1].author
        placeholder = "[subject]"
        representation = "\n".join(
            f"{placeholder if message.author == subject else message.author.display_name}: {message.content}" for message in chat
        )
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
        explaination = self.complete.complete(prompt + nickname + continuation, stopSequences=[".", "\n"], maxTokens=32)
        print(prompt + nickname + continuation + explaination)
        return nickname, explaination
