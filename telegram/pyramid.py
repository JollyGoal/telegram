import telebot
import requests
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '1024735974:AAFZZoTuOHDYEnOw6TCt-J-CKR9QAIDxaCQ'
bot = telebot.TeleBot(TOKEN)


def main_btns(message):
    chat_id = message.chat.id
    key = ReplyKeyboardMarkup(True, False)
    key.add('💸 Вывести средства', '💴 Пополнить баланс')
    key.add('🔗 Рефферальная ссылка', '👥 Мои реффералы')
    key.add('❓ Информация')
    key.add('👤 Баланс')
    return key


@bot.message_handler(commands=['start'])
def start(message):
    text = 'Привет, {}'.format(
        message.from_user.first_name) + ' !Это бот, к которому Абдумалик должен придумать приветствие и описание'
    bot.send_message(message.from_user.id, text, reply_markup=main_btns(message))


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Help text. Как работает бот")  # TODO
    bot.reply_to(message, message.from_user.id)
    bot.reply_to(message, message)


@bot.message_handler(content_types=["text"])
def send_anytext(message):
    chat_id = message.chat.id
    key = ReplyKeyboardMarkup(True, False)
    if message.text == '💸 Вывести средства':
        text = 'Принятие заявки'
        bot.reply_to(message, text, reply_markup=key)
    elif message.text == '💴 Пополнить баланс':
        bot.reply_to(message,
                     'Чтобы пополнить свой баланс вам необходимо перечислить средства на счёт: <b>"0000 0000 0000"</b> \n'
                     'Если вы уже перечислили деньги, то просто отправьте мне фото трансакции, или номер карты с суммой перевода, \n'
                     'Например: ',
                     reply_markup=key, parse_mode='HTML')
        # bot.forward_message(to_chat_id, from_chat_id, message_id)
    elif message.text == '🔗 Рефферальная ссылка':
        bot.reply_to(message, 'Ваша рефферальная ссылка: ', reply_markup=key)
    elif message.text == '👥 Мои реффералы':
        text = 'Кол-во реффералов: <b>0</b> \n Список ваших реффералов:'
        bot.reply_to(message, text, parse_mode='HTML', reply_markup=key)
    elif message.text == '❓ Помощь':
        bot.reply_to(message, 'Подробная информация о трансакциях', reply_markup=key)
    elif message.text == '👤 Баланс':
        bot.reply_to(message, 'У вас на счету: 0,00 сум', reply_markup=key)
    else:
        bot.reply_to(message, 'Я не понимаю, чего вы от меня хотите 😔', reply_markup=key)


@bot.message_handler(content_types=["text"])
def send_oplatit(message):
    if message.text == '💴Вывести средства':
        bot.reply_to(message, 'У вас недостаточно средств для вывода :-(')


if __name__ == '__main__':
    bot.polling(none_stop=True)
