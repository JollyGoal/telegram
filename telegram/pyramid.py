import telebot
import requests
import json
TOKEN = '1024735974:AAFZZoTuOHDYEnOw6TCt-J-CKR9QAIDxaCQ'
bot = telebot.TeleBot(TOKEN)


# getMe
user = bot.get_me()
@bot.message_handler(commands=['start'])
def start(message):
    text = 'Привет, {}'.format(message.from_user.first_name) + ' это бот'
    bot.send_message(message.from_user.id, text)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(content_types='text')
def Send_Message(message):
    pass

bot.polling(none_stop=False, interval=0, timeout=20)

file_info = bot.get_file(file_id)
file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))


