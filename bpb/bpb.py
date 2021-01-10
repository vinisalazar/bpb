import logging

from telegram.ext import Handler, Updater

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


class CodBonitoBot:
    def __init__(self, token):

        logging.info("Inicializando o bot...")

        self.token = token
        self._updater = Updater(token=self.token)

    def _add_handler(self, handler):
        if not isinstance(handler, Handler):
            raise ValueError("Handler deve ser do tipo Handler!")
        self._updater.dispatcher.add_handler(handler)

    def config_handlers(self, handlers):

        logging.info("Configurando os handlers...")

        for handler in handlers:
            self._add_handler(handler)

    def run(self):

        self._updater.start_polling()
        logging.info("Bot está rodando!")

        self._updater.idle()
