'''Updater class неприрывно забирает адейты из Telegram и перенаправляет в Dispatcher class'''
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from lxml import etree
from telebot import types
import telebot
import logging
import requests
import xml.etree.ElementTree as ET
from functions import *

request_ids = RequestIdExp("172.22.3.86", "4545", "Admin_QSR", "190186")
request_ids.id_exp_request()



logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot('398733267:AAH01uFzFlCsBsdB-u_Wj0gZo-ndUXT8-3k')
driver_name = None

@bot.message_handler(commands=['start'])
def authorize(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.chat.id, "Отправьте телефон для авторизации", reply_markup=keyboard)
    #print(message)

# Сравниваем полученый ID контакта с ID пользователя, от которого пришло сообщение
@bot.message_handler(content_types= ["contact"])
def verification(message):
    if message.from_user.id == message.contact.user_id:
        bot.send_message(message.chat.id, "Авторизация успешна" + "\n _DRIVER_NAME_, добро пожаловать в систему.")


'''def send_welcome(message):
    bot.reply_to(message, "Howdy _DRIVER_NAME_, system is ready for action")
    # keyboard = types.ReplyKeyboardRemove(selective=None)
'''
@bot.message_handler(commands=["geophone"])
def geophone(message):
    # Эти параметры для клавиатуры необязательны, просто для удобства
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_phone, button_geo)
    bot.send_message(message.chat.id, "Отправьте телефон для авторизации", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "run")
def menu_1(message):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Menu', 'Exit']])
    bot.send_message(message.chat.id, 'Меню', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Назад")

@bot.message_handler(func=lambda message: message.text == "Menu")
def menu_1(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Свободные заказы', 'Мои заказы', 'Назад']])
    bot.send_message(message.chat.id, 'Меню', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Мои заказы")
def menu_2(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Список заказов', 'Номер заказа', 'Отчет по заказам', 'Назад']])
    bot.send_message(message.chat.id, 'Меню', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "Список заказов")
def menu_3(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in ['Выполнен', 'В Архив', 'Назад']])
    bot.send_message(message.chat.id, 'Меню', reply_markup=keyboard)

#@bot.message_handler(func=lambda m: True)
#def echo_all(message):
#	bot.send_message(message.chat.id, message.text)

# Upon calling this function, TeleBot starts polling the Telegram servers for new messages.
# - none_stop: True/False (default False) - Don't stop polling when receiving an error from the Telegram servers
# - interval: True/False (default False) - The interval between polling requests
#           Note: Editing this parameter harms the bot's response time
# - block: True/False (default True) - Blocks upon calling this function
bot.polling(none_stop=False, interval=10)