import telebot
from telebot import types
import random
from datetime import date
import os


# def read_file(file_name):
#     with open(file_name, 'r') as file:
#         return file.read()
#
# bot = telebot.TeleBot(read_file('token.txt'))

token = os.getenv('TELEBOT_TOKEN')
bot = telebot.TeleBot(token)

list_name_file = ['0101', '0201', '0301', '0401', '0501', '0601', '0701', '0801', '0901', '1001']
print('Поехали!')

@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Aloha, {message.from_user.first_name}! Здесь можно получить мотивашку на день. Готовы попробовать?'
    bot.send_message(message.chat.id, mess)
    bot.send_message(message.chat.id, 'Выберите "/yes" или "/no"')


@bot.message_handler(commands=['no'])
def choice_ansver_no(message):
    bot.send_message(message.chat.id, 'До встречи в следующий раз!')


@bot.message_handler(commands=['yes'])
def choice_ansver_yes(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    choice_data = types.KeyboardButton('Дата')
    choice_random = types.KeyboardButton('Рандом')
    choice_today = types.KeyboardButton('Сегодня')
    markup.add(choice_today, choice_data, choice_random)
    bot.send_message(message.chat.id, 'Делай выбор', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def ansver_yes(message):
    if message.chat.type == 'private':
        if message.text == 'Рандом':
            name_file = random.choice(list_name_file)
            full_name_file = f'{name_file}2022'
            foto = open(f'album/{full_name_file}.jpg', 'rb')
            bot.send_photo(message.chat.id, foto)

        elif message.text == 'Дата':
            request_user = bot.send_message(message.chat.id, 'Введите дату в формате ДДММ без разделительных знаков.')
            bot.register_next_step_handler(request_user, ansver_user)

        elif message.text == 'Сегодня':
            today = date.today()
            full_name_file = today.strftime('%d%m%Y')
            foto = open(f'album/{full_name_file}.jpg', 'rb')
            bot.send_photo(message.chat.id, foto)

        else:
            choice_ansver_yes(message)


def ansver_user(message):
    mess = message.text

    if mess in list_name_file:
        full_name_file = f'{mess}2022'
        foto = open(f'album/{full_name_file}.jpg', 'rb')
        bot.send_photo(message.chat.id, foto)

    else:
        bot.send_message(message.chat.id, 'Введите дату в формате ДДММ без разделительных знаков.')


bot.polling(none_stop=True)