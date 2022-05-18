import discord
from complete import Complete


class Explainer:
    def __init__(self, complete: Complete, prefix):
        self.complete = complete
        self.prefix = prefix

    def explain(self, chat: list[discord.Message]):
        representation = "\n".join(
            f"{message.author.display_name}: {message.content}" for message in chat
        )
        subject = chat[-1].author.display_name
        prompt = (
            self.prefix
            + representation
            + f"""
        
        Q: what is {subject} sorry for?
        A: {subject} is sorry for """
        )
        response = self.complete.complete(prompt, stopSequences=[".", "\n"], maxTokens=32)
        print(prompt + response)
        return f"{subject} is sorry for " + response
