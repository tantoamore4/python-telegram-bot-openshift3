import logging
from queue import Queue
from threading import Thread
from telegram import Bot
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Updater, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
TOKEN = '693266929:AAHv5cYEQmTI0kkClSWNK-CtRr7oqrXp3mI'


def start(bot, update):
    update.message.reply_text('Welcome to the Test Bot! I will reply you what you will write me.')


def help(bot, update):
    update.message.reply_text('You can get any help here.')

    keyboardButtons = [[InlineKeyboardButton("Help", callback_data="1")],
                       [InlineKeyboardButton("Examples", callback_data="2")]]
    keyboard = InlineKeyboardMarkup(keyboardButtons)



def button(bot, update):
    query = update.callback_query
    if query.data == "1":
        text = "You can choose any of the following actions: +, -, /, *"
    elif query.data == "2":
        text = "3+4, 44-12, 43/2, 12*9"
    bot.editMessageText(text = text, chat_id = query.message.chat_id,
                        message_id = query.message.message_id)


def ar(bot, update):
    num = update.message.text
    try:
        ar = eval(num)
    except (NameError, SyntaxError):
        ar = "Error"
    bot.send_message(chat_id=update.message.chat_id, text=ar)


"""def echo(bot, update):
    update.message.reply_text('You said:  ' + update.message.text)
"""

"""def dolintenge(bot, update, args):
    dollars = int(args)
    tenge = dollars * 356
    update.message.reply_text(text=tenge)
"""

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))

# Write your handlers here


def setup(webhook_url=None):
    """If webhook_url is not passed, run with long-polling."""
    logging.basicConfig(level=logging.WARNING)
    if webhook_url:
        bot = Bot(TOKEN)
        update_queue = Queue()
        dp = Dispatcher(bot, update_queue)
    else:
        updater = Updater(TOKEN)
        bot = updater.bot
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", help))
        dp.add_handler(CommandHandler("dolintenge", dolintenge))
        dp.add_handler(CallbackQueryHandler(button))

        # on noncommand i.e message - echo the message on Telegram
        """dp.add_handler(MessageHandler(Filters.text, echo))"""
        dp.add_handler(MessageHandler(Filters.text, ar))

        # log all errors
        dp.add_error_handler(error)
    # Add your handlers here
    if webhook_url:
        bot.set_webhook(webhook_url=webhook_url)
        thread = Thread(target=dp.start, name='dispatcher')
        thread.start()
        return update_queue, bot
    else:
        bot.set_webhook()  # Delete webhook
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    setup()
