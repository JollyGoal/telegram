import telebot
import requests
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '1024735974:AAFZZoTuOHDYEnOw6TCt-J-CKR9QAIDxaCQ'
bot = telebot.TeleBot(TOKEN)


def button(message):
    r = requests.get('http://127.0.0.1:8000/api/button/')
    data = json.loads(r.text)
    key = ReplyKeyboardMarkup(True, False)
    text = 'Привет, {}'.format(
        message.from_user.first_name) + ' !Это бот, к которому Абдумалик должен придумать приветствие и описание'
    for i in range(len(data['data'])):
        buttons = KeyboardButton(data['data'][i]['name'])
        key.add(buttons)
    bot.send_message(message.from_user.id, text, reply_markup=key)


@bot.message_handler(commands=['start'])
def start(message):
    button(message)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Help text. Как работает бот")


@bot.message_handler(content_types=["text"])
def send_anytext(message):
    chat_id = message.chat.id
    if message.text == 'qqq':
        text = 'qqqqqqq'
        key = ReplyKeyboardMarkup(True, False)
        bot.send_message(message.from_user.id, text, reply_markup=key)
    else:
        bot.reply_to(message, 'Я не понимаю, чего вы от меня хотите 😔')
    # r = requests.get('http://127.0.0.1:8000/api/text/?btn=' + message.text)
    # data = json.loads(r.text)
    # print(data)
    # key = ReplyKeyboardMarkup(True, False)
    # bot.reply_to(message, data['data'][0]['text'], reply_markup=key)


@bot.message_handler(content_types=["text"])
def send_oplatit(message):
    if message.text == '💴Вывести средства':
        bot.reply_to(message, 'У вас недостаточно средств для вывода :-(')


if __name__ == '__main__':
    bot.polling(none_stop=True)
