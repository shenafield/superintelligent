import requests


class Complete:
    def __init__(self, api_key, model="j1-jumbo"):
        self.key = api_key
        self.model = model

    def predict(
        self,
        prompt,
        numResults=1,
        maxTokens=8,
        stopSequences=[],
        topKReturn=0,
        temperature=0.0,
        bias={},
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
                "logitBias": bias,
            },
        )
        a = response.json()
        print(a)
        return a

    def complete(self, prompt, **kwargs):
        return self.predict(prompt, **kwargs)["completions"][0]["data"]["text"]