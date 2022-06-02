import json
import os

from discord.ext import commands
from dotenv import load_dotenv

from complete import Complete
from explainer.cog import ExplainerCog
from explainer.explainer import Explainer
from nicknamer.cog import NicknamerCog
from nicknamer.nicknamer import Nicknamer


def main():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    bot_token = os.getenv("BOT_TOKEN")
    model = os.getenv("MODEL", "j1-jumbo")
    nick_freq = os.getenv("NICKNAME_FREQ", 0.05)
    roles = json.loads(os.getenv("NICKNAME_ROLES", "null"))

    bot = commands.Bot()
    completer = Complete(api_key, model=model)
    explainer = Explainer(completer, open("prefixes/sorry.txt", "r").read())
    bot.add_cog(ExplainerCog(bot, explainer))
    nicknamer = Nicknamer(completer, open("prefixes/nicknames.txt", "r").read())
    bot.add_cog(NicknamerCog(bot, nicknamer, nick_freq, roles))
    bot.run(bot_token)


if __name__ == "__main__":
    main()
