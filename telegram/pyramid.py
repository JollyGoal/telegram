import decimal

import telebot
import requests
import json
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '1024735974:AAFZZoTuOHDYEnOw6TCt-J-CKR9QAIDxaCQ'
bot = telebot.TeleBot(TOKEN)

withdraw_status = False
replenishment_status = False
input_card = False
input_card_replenishment = False
som = 0


def main_btns(message):
    chat_id = message.chat.id
    key = ReplyKeyboardMarkup(True, False)
    key.add('💸 Вывести средства', '💴 Пополнить баланс')
    key.add('🔗 Реферальная ссылка', '👥 Мои рефералы')
    key.add('❓ Информация')
    key.add('👤 Баланс')
    return key


def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None


def update_user_info(message):
    new_data = {
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
        'username': message.from_user.username,
    }
    response = requests.put('http://127.0.0.1:8000/api/profiles/?user_id=' + str(message.from_user.id), data=new_data)
    print(response.status_code, response.reason)


@bot.message_handler(commands=['start'])
def start(message):
    if not message.from_user.is_bot:
        referral_link = extract_unique_code(message.text)
        check_user = requests.get('http://127.0.0.1:8000/api/single_profile/?user_id=' + str(message.from_user.id))
        user_data = json.loads(check_user.text)
        if len(user_data['data']) == 0:
            # If there is no user:
            if referral_link:
                inviter = requests.get('http://127.0.0.1:8000/api/single_profile/?user_id=' + referral_link)
                data = json.loads(inviter.text)
                if len(data['data']) != 0:
                    new_data = {
                        'user_id': message.from_user.id,
                        'invited_by': referral_link,
                        'first_name': message.from_user.first_name,
                        'last_name': message.from_user.last_name,
                        'username': message.from_user.username,
                    }
                    response = requests.post('http://127.0.0.1:8000/api/profiles/', data=new_data)
                    print(response.status_code, response.reason)
                else:
                    new_data = {
                        'user_id': message.from_user.id,
                        'first_name': message.from_user.first_name,
                        'last_name': message.from_user.last_name,
                        'username': message.from_user.username,
                    }
                    response = requests.post('http://127.0.0.1:8000/api/profiles/', data=new_data)
                    print(response.status_code, response.reason)
            else:
                new_data = {
                    'user_id': message.from_user.id,
                    'first_name': message.from_user.first_name,
                    'last_name': message.from_user.last_name,
                    'username': message.from_user.username,
                }
                response = requests.post('http://127.0.0.1:8000/api/profiles/', data=new_data)
                print(response.status_code, response.reason)
        else:
            # If user exists:
            if user_data['data'][0]['invited_by']:
                # If existing user is already a referral:
                pass
            else:
                # If existing user is not a referral:
                if referral_link:
                    inviter = requests.get('http://127.0.0.1:8000/api/single_profile/?user_id=' + referral_link)
                    data = json.loads(inviter.text)
                    if len(data['data']) != 0:
                        new_data = {
                            'invited_by': referral_link,
                            'first_name': message.from_user.first_name,
                            'last_name': message.from_user.last_name,
                            'username': message.from_user.username,
                        }
                        response = requests.put('http://127.0.0.1:8000/api/profiles/?user_id=' + str(message.from_user.id), data=new_data)
                        print(response.status_code, response.reason)
                    else:
                        pass
        update_user_info(message)
        text = 'Привет, {}'.format(
            message.from_user.first_name) + '! Это бот, к которому Абдумалик должен придумать приветствие и описание'
        bot.send_message(message.from_user.id, text, reply_markup=main_btns(message))


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Help text. Как работает бот")  # TODO
    text = "Как работает бот?"
    bot.send_message(message.from_user.id, text, reply_markup=main_btns(message))


@bot.message_handler(func=lambda message: 'Назад' == message.text, content_types=['text'])
def send_oplatit(message):
    global withdraw_status
    global replenishment_status
    global input_card
    global input_card_replenishment
    global som
    replenishment_status = False
    withdraw_status = False
    input_card = False
    input_card_replenishment = False
    som = 0
    return bot.send_message(message.from_user.id, "Главное меню", reply_markup=main_btns(message))


@bot.message_handler(content_types=["text"])
def send_any_text(message):
    global withdraw_status
    global replenishment_status
    global input_card
    global input_card_replenishment
    global som
    if not message.from_user.is_bot:
        chat_id = message.chat.id
        check_user = requests.get('http://127.0.0.1:8000/api/single_profile/?user_id=' + str(message.from_user.id))
        user_data = json.loads(check_user.text)
        key = ReplyKeyboardMarkup(True, False)
        if message.text == '💸 Вывести средства':
            text = 'У вас на счету: ' + str(user_data['data'][0]['balance']) + ' сум' + '\n' + 'Минимальная сумма вывода - 30 000 сум.\n'
            if float(user_data['data'][0]['balance']) > 30000:
                text += "Пожалуйста, введите сумму, которую вы бы хотели вывести, или выберите опцию: 'ВЫВЕСТИ ВСЁ!' "
                withdraw_key = ReplyKeyboardMarkup(True, False)
                withdraw_key.add('ВЫВЕСТИ ВСЁ!')
                withdraw_key.add('Назад')
                bot.reply_to(message, text, reply_markup=withdraw_key, parse_mode="HTML")
                withdraw_status = True
                pass
            else:
                text += "\n" + 'Чтобы вывести средства, на вашем счету должно быть 30 000 сум и больше!'
                bot.reply_to(message, text, reply_markup=main_btns(message), parse_mode="HTML")

        if message.text == '💴 Пополнить баланс':
            bot.reply_to(message,
                         'Чтобы пополнить свой баланс вам необходимо перечислить средства на счёт: <b>"0000 0000 0000"</b> \n'
                         'Минимальная сумма начисления 30 000 сум. \n'
                         'Если вы уже перечислили деньги, то просто отправьте сумму начисления,\n'
                         'Например: ', parse_mode='HTML')
            replenishment_key = ReplyKeyboardMarkup(True, False)
            replenishment_key.add('Назад')
            bot.send_message(message.from_user.id, "30000", reply_markup=replenishment_key)
            replenishment_status = True
            # bot.forward_message(to_chat_id, from_chat_id, message_id)  TODO
        elif message.text == '🔗 Реферальная ссылка':
            bot.reply_to(message, 'Ваша реферальная ссылка:')
            bot.send_message(message.from_user.id, '<b>http://t.me/GeniusPlaza_bot/?start=</b>{}'.format(message.from_user.id), parse_mode='HTML', reply_markup=key)
            bot.send_message(message.from_user.id, 'Отправляйте эту реферальную ссылку своим друзьям, чтобы получать <b>реальные деньги</b> с их пополнений.', parse_mode='HTML')
        elif message.text == '👥 Мои рефералы':
            invited_by_list = requests.get('http://127.0.0.1:8000/api/invited_by/?user_id=' + str(message.from_user.id))
            referrals_data = json.loads(invited_by_list.text)
            text = 'Кол-во рефералов: <b>' + str(len(referrals_data['data'])) + '</b> \nСписок ваших рефералов: \n'
            for i in range(len(referrals_data['data'])):
                new_text = ''
                new_text += referrals_data['data'][i]['first_name']
                try:
                    new_text += ' ' + referrals_data['data'][i]['last_name']
                except:
                    pass
                new_text += ' \n'
                text += new_text
            bot.reply_to(message, text, parse_mode='HTML', reply_markup=key)
        elif message.text == '❓ Информация':
            bot.reply_to(message, 'Подробная информация о трансакциях', reply_markup=key)  # TODO
        elif message.text == '👤 Баланс':
            bot.reply_to(message, 'У вас на счету: ' + str(user_data['data'][0]['balance']) + ' сум', reply_markup=key)
        else:
            if withdraw_status:
                withdraw_key = ReplyKeyboardMarkup(True, False)
                withdraw_key.add('ВЫВЕСТИ ВСЁ!')
                withdraw_key.add('Назад')
                print("Идёт вывод средств!")
                try:
                    som = decimal.Decimal(message.text)
                    if som > 30000:
                        bot.send_message(message.from_user.id, "Введите номер карты, на которую нужно вывести средства"
                                                               "\nНапример: <b>8600 1111 2222 3333</b>", parse_mode="HTML")
                        input_card = True
                        withdraw_status = False
                    else:
                        bot.reply_to(message, "Минимальная сумма вывода - 30 000 сум.\n" + 'Пожалуйста, введите число, равное, или большее <b>300000</>, или выберите опцию: "ВЫВЕСТИ ВСЁ!" ', reply_markup=withdraw_key, parse_mode="HTML")
                except:
                    if message.text != "ВЫВЕСТИ ВСЁ!":
                        bot.send_message(message.from_user.id, 'Пожалуйста, введите число, например: <b>300000</>, или выберите опцию: "ВЫВЕСТИ ВСЁ!" ', reply_markup=withdraw_key, parse_mode="HTML")
                    else:
                        bot.send_message(message.from_user.id, "Введите номер карты, на которую нужно вывести средства"
                                                               "\nНапример: <b>8600 1111 2222 3333</b>", parse_mode="HTML")
                        som = user_data['data'][0]['balance']
                        input_card = True
                        withdraw_status = False
            elif input_card:
                text = "Ваш запрос обрабатывается! Деньги будут перечислены в течение 2-х суток." + "\n" + "Детали:" + "\nСумма: " + str(som) + "\nНомер карты: " + message.text
                bot.send_message(message.from_user.id, text)
                withdraw_data = {
                    'broker': message.from_user.id,
                    'type': "V",
                    'sum': som,
                    'card': message.text,
                }
                response = requests.post('http://127.0.0.1:8000/api/transactions_not_verified/', data=withdraw_data)
                print(response.status_code, response.reason)
                withdraw_status = False
                replenishment_status = False
                input_card = False
                som = 0

            elif replenishment_status:
                replenishment_key = ReplyKeyboardMarkup(True, False)
                replenishment_key.add('Назад')
                try:
                    som = decimal.Decimal(message.text)
                    bot.send_message(message.from_user.id, "Введите номер карты, с которой были начислены средства."
                                                           "\nНапример: <b>8600 1111 2222 3333</b>", parse_mode="HTML")
                    input_card_replenishment = True
                    replenishment_status = False
                except:
                    bot.send_message(message.from_user.id, 'Пожалуйста, введите сумму начисления, например: <b>300000</>', reply_markup=replenishment_key, parse_mode="HTML")
                    pass

            elif input_card_replenishment:

                text = "Ваш запрос обрабатывается! Данные о вашем балансе будут обновлены в течение 2-х суток." + "\n" + "Детали:" + "\nСумма: " + str(som) + "\nНомер карты: " + message.text
                bot.send_message(message.from_user.id, text)
                replenishment_data = {
                    'broker': message.from_user.id,
                    'type': "P",
                    'sum': som,
                    'card': message.text,
                }
                response = requests.post('http://127.0.0.1:8000/api/transactions_not_verified/', data=replenishment_data)
                print(response.status_code, response.reason)
                withdraw_status = False
                replenishment_status = False
                input_card = False
                input_card_replenishment = False
                som = 0

            else:
                bot.reply_to(message, 'Я не понимаю, чего вы от меня хотите 😔', reply_markup=main_btns(message))

        update_user_info(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
