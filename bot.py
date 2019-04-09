#!/usr/bin/python3.4
# -*- coding: utf-8 -*-
import time
import logging
import re
import telebot
from telebot import util
from telebot import types
import cherry_server  # настройки сервера входящих сообщений + установка и сброс webhook

import config
import parseXML  # Parse XML file with list of sessions in cinema
import c_log

# включаем логгирование
# logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.

bot = telebot.TeleBot(config.token)

# cherry_server.webhook_rm(bot)
# cherry_server.webhook_add(bot)

# print(cherry_server.WEBHOOK_URL_BASE + cherry_server.WEBHOOK_URL_PATH)


def get_list_cinema_after_now(tuple_cinema, get_cinema_name=True):
    if type(tuple_cinema) is tuple:
        time_now = float(time.time())  # текущее время для сравнения
        sessions = ''
        index = 0
        sessions_not_zero = False
        for item in tuple_cinema:
                if index > 40:
                        break
                if float(item['timestamp']) < time_now:
                        continue
                sessions_not_zero = True
                if get_cinema_name == True:
                    sessions += '\n*' + item['time'] + '* "' + item['film'] + '" в ' + item['cinema'] + '(' + item['hall'] + ' зал) - ' + item['cost']
                else:
                    sessions += '\n*' + item['time'] + '* "' + item['film'] + '", ' + \
                                    ' зал ' + item['hall'] + ' - ' + item['cost']
                index += 1
        if not sessions_not_zero:
            sessions = 'Сегодня больше нет киносеансов! :('
    return sessions


keyboard = types.InlineKeyboardMarkup()
keyboard.add(types.InlineKeyboardButton("Ближайшие сеансы в Уфе (40шт)", callback_data='last_sessions'))
keyboard.row(types.InlineKeyboardButton("Кинотеатры", callback_data='list_cinema'), \
             types.InlineKeyboardButton("Фильмы", callback_data='list_films'))

keyboard_after = types.InlineKeyboardMarkup()
keyboard_after.row(types.InlineKeyboardButton("Ближайшие сеансы", callback_data='last_sessions'),
                   types.InlineKeyboardButton("Фильмы", callback_data='list_films'),
                   types.InlineKeyboardButton("Кинотеатры", callback_data='list_cinema'))


@bot.message_handler(commands=['start'])
def comm_cinema(message):  # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, 'Выберите:', reply_markup=keyboard)
    c_log.log_text(message)


# обработка inline меню
@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    # вывод списка кинотеатров
    if call.data == 'list_cinema':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, \
                              text='Выберите кинотеатр:', reply_markup=parseXML.cinema_keyboard())
    elif call.data == 'start_menu':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, \
                              text='Выберите:', reply_markup=keyboard)
    # вывод списка фильмов
    elif call.data == 'list_films':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, \
                              text='Выберите кинофильм:', reply_markup=parseXML.films_keyboard())
    # выводим список киносеансов по кинотеатру
    elif re.search(r'cinema\d+', call.data):
        match = re.search(r'cinema(\d+)', call.data)
        split_text = util.split_string("Фильм:" + get_list_cinema_after_now(parseXML.get_films_by_cinema(match.group(1)),
                                       False), 3000)
        for text in split_text:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, \
                                  text=text, parse_mode="Markdown", reply_markup=keyboard_after)
    # выводим список киносеансов по фильму
    elif re.search(r'film\d+', call.data):
        match = re.search(r'film(\d+)', call.data)
        split_text = util.split_string(get_list_cinema_after_now(parseXML.get_cinema_by_film(match.group(1)), True), 3000)
        for text in split_text:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, \
                                  text=text, parse_mode="Markdown", reply_markup=keyboard_after)
    # выводим ближайшие киносеансы
    elif call.data == 'last_sessions':
        split_text = util.split_string(get_list_cinema_after_now(parseXML.parse_xml()), 3000)
        for text in split_text:
            bot.send_message(call.message.chat.id, text, parse_mode="Markdown", reply_markup=keyboard_after)
    c_log.log_text_call(call)

@bot.message_handler(commands=['help'])
def comm_cinema(message):  # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, 'Добро пожаловать! Ваш chat_id=' + str(message.chat.id))
    c_log.log_text(message)

@bot.message_handler(regexp='Ближайшие сеансы в Уфе')
@bot.message_handler(commands=['c40'])
def comm_start(message):  # Название функции не играет никакой роли, в принципе
        split_text = util.split_string(get_list_cinema_after_now(parseXML.parse_xml()), 3000)
        for text in split_text:
                bot.send_message(message.chat.id, text,  parse_mode="Markdown")
        c_log.log_text(message)

@bot.message_handler(commands=['allfilms'])
def comm_cinema(message):  # Название функции не играет никакой роли, в принципе
    bot.send_message(chat_id=message.chat.id, text='Выберите фильм:', reply_markup=parseXML.films_keyboard())
    c_log.log_text(message)

@bot.message_handler(commands=['allcinemas'])
def comm_cinema(message):  # Название функции не играет никакой роли, в принципе
    bot.send_message(chat_id=message.chat.id, text='Выберите фильм:', reply_markup = parseXML.cinema_keyboard())
    c_log.log_text(message)

@bot.message_handler(func=lambda message: True, content_types=['text'])
def repeat_all_messages(message):  # Название функции не играет никакой роли, в принципе
    if message.text == 'Список кинотеатров':
        bot.send_message(message.chat.id, parseXML.cinema_list())
    elif message.text == 'Список фильмов':
        bot.send_message(message.chat.id, parseXML.film_list())
    else:
        bot.send_message(message.chat.id, 'Не будем тратить время на беседы, предлагаю найти фильм:', reply_markup = keyboard)
    c_log.log_text(message)

# Собственно, запуск!
webhook = cherry_server.WebhookServer()
webhook.add_bot(bot)
cherry_server.cherrypy.quickstart(webhook, cherry_server.WEBHOOK_URL_PATH, {'/': {}})
