import telebot
import requests
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '1024735974:AAFZZoTuOHDYEnOw6TCt-J-CKR9QAIDxaCQ'
bot = telebot.TeleBot(TOKEN)


def button(message):
    r = requests.get('http://127.0.0.1:8000/api/button')
    data = json.loads(r.text)
    key = ReplyKeyboardMarkup(True, False)
    print(data)
    for i in range(len(data['data'])):
        buttons = KeyboardButton(data['data'][i]['name'])
        key.add(buttons)
    text = 'Выберите опцию:'
    bot.send_message(message.from_user.id, text, reply_markup=key)


@bot.message_handler(commands=['start'])
def start(message):
    text = 'Привет, {}'.format(
        message.from_user.first_name) + ' !Это бот, к которому Абдумалик должен придумать приветствие и описание'
    bot.send_message(message.from_user.id, text)
    button(message)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Help text. Как работает бот")


@bot.message_handler(content_types='text')
def Send_Message(message):
    pass


if __name__ == '__main__':
    bot.polling(none_stop=True)
