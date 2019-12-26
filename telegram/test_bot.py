""" Пример сообщения с разными стилями шрифтов:
    - жирный
    - наклонный
    - ссылка
    - однострочный код
    - многострочный код

    А так же как прикрепить картинку под текст
"""
import telebot
from logging import getLogger
from telebot import types
from telegram import Bot
from telegram import ParseMode
from telegram import InputMediaPhoto
from telegram import Update
from telegram.ext import CommandHandler
from telegram.ext import CallbackContext
from telegram.ext import CallbackQueryHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import TypeHandler
from telegram.ext import Updater
from telegram.utils.request import Request

from .conf import load_config
from .utils import debug_requests

config = load_config()

logger = getLogger(__name__)


@debug_requests
def do_start(update: Update, context: CallbackContext):
    text = [
        '*нажми команду*',
        '/url2 -- ссылка в тексте',
        '/img -- хак: картинка под текстом',
        '/kartinka -- картинка с диска',
    ]
    update.message.reply_text(
        text='\n'.join(text),
        parse_mode=ParseMode.MARKDOWN,
    )


@debug_requests
def text_with_url_md(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Подпишись на мой [канал](https://www.youtube.com/channel/UCAlRksF5338XmSMbwS3W7eA/)! '
        'Там много информации для самообразования',
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )


@debug_requests
def text_with_url_html(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Подпишись на мой <a href="https://www.youtube.com/channel/UCAlRksF5338XmSMbwS3W7eA/">канал</a>! '
        'Там много информации для самообразования',
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


@debug_requests
def image_hack_html(update: Update, context: CallbackContext):
    text = [
        'бла-бла <a href="https://picsum.photos/200/300">&#8205;</a>',
        'тут может быть любое количество текста, главное чтобы картинка была <b>первой</b> ссылкой '
        'во всём тексте, и внутри тега "a" был невидимый пробел',
    ]
    update.message.reply_text(
        text='\n'.join(text),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=False,
    )


@debug_requests
def image_kartinka(update: Update, context: CallbackContext):
    img = open('kartinka.PNG', 'rb')
    bot.send_photo(message.chat.id, img)
    update.message.reply_text(
        text='\n'.join(text),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=False,
    )


def main():
    logger.info('Started Markup-Bot')

    req = Request(
        connect_timeout=0.5,
        read_timeout=1.0,
    )
    bot = Bot(
        token=config.TG_TOKEN,
        request=req,
        base_url=config.TG_API_URL,
    )
    updater = Updater(
        bot=bot,
        use_context=True,
    )

    # Проверить что бот корректно подключился к Telegram API
    info = bot.get_me()
    logger.info(f'Bot info: {info}')

    # Навесить обработчики команд
    start_handler = CommandHandler("start", do_start)

    # Произвести демонстрацию разного форматирования
    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(CommandHandler('url1', text_with_url_md))
    updater.dispatcher.add_handler(CommandHandler('url2', text_with_url_html))
    updater.dispatcher.add_handler(CommandHandler('img', image_hack_html))
    updater.dispatcher.add_handler(TypeHandler('kartinka', image_kartinka))

    # Начать бесконечную обработку входящих сообщений
    updater.start_polling()
    updater.idle()
    logger.info('Stopped Markup-Bot')


if __name__ == '__main__':
    main()
