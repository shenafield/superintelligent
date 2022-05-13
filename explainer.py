import discord
import requests


class Explainer:
    def __init__(self, api_key, model="j1-jumbo"):
        self.key = api_key
        self.model = model
        self.prefix = open("prompt_example.txt").read()

    def predict(
        self,
        prompt,
        numResults=1,
        maxTokens=8,
        stopSequences=[],
        topKReturn=0,
        temperature=0.0,
    ):
        response = requests.post(
            f"https://api.ai21.com/studio/v1/{self.model}/complete",
            headers={"Authorization": f"Bearer {self.key}"},
            json={
                "prompt": prompt,
                "numResults": numResults,
                "maxTokens": maxTokens,
                "stopSequences": stopSequences,
                "topKReturn": topKReturn,
                "temperature": temperature,
            },
        )
        return response.json()

    def complete(self, prompt, **kwargs):
        return self.predict(prompt, **kwargs)["completions"][0]["data"]["text"]

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
        response = self.complete(prompt, stopSequences=[".", "\n"], maxTokens=32)
        print(prompt + response)
        return f"{subject} is sorry for " + response
