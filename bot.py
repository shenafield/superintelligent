import os

from discord.ext import commands
from dotenv import load_dotenv

from cog import ExplainerCog
from explainer import Explainer


def main():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    bot_token = os.getenv("BOT_TOKEN")

    bot = commands.Bot()
    explainer = Explainer(api_key)
    bot.add_cog(ExplainerCog(bot, explainer))
    bot.run(bot_token)


if __name__ == "__main__":
    main()
