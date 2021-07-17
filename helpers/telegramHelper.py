from django.conf import settings
from telegram.ext import Updater


class TelegramHelper:
    def __init__(self, token=settings.TELEGRAM_TOKEN):
        self.updater = Updater(token=token, use_context=True)
        dispatcher = updater.dispatcher

        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO) 

        start_handler = CommandHandler('info', self.info)
        dispatcher.add_handler(start_handler)
        updater.start_polling()

    def info(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


