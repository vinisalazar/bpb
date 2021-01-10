import os
from bpb.bpb import CodBonitoBot
from bpb.handlers import get_handlers

if __name__ == "__main__":

    token = os.environ.get("TEL_TOKEN")

    bot = CodBonitoBot(token)

    handlers = get_handlers()

    bot.config_handlers(handlers)

    bot.run()
