# Copyright 2018 Shibkov Konstantin <sendel@sendel.ru>
# All rights reserved. MIT License.
# Parse XML file with list of sessions in cinema

# -*- coding: utf-8 -*-
from lxml import etree
import time
import config
from telebot import types


# Функция чтения списка фильмов из XML
def parse_xml():
    parser = etree.XMLParser(encoding="utf-8")
    tree = etree.parse(config.xml_file_cinema, parser=parser)
    root = tree.getroot()

    c = []
    for child in root.find('sessions'):
        cinema = {}
        d = time.localtime(int(child.attrib['timestamp'].split('.')[0]))
        cinema.update({'time': time.strftime('%H:%M', d)})
        cinema.update({'film': child.attrib['film']})
        cinema.update({'cinema': child.attrib['cinema']})
        cinema.update({'hall': child.attrib['hall']})
        cinema.update({'cost': child.attrib['cost']})
        cinema.update({'date_time': time.strftime('%Y%m%d%H%M', d)})
        cinema.update({'timestamp': child.attrib['timestamp']})

        if child.attrib['is_tomorrow'] == '1':
            cinema.update({'time': time.strftime('%H:%M (%d.%m)', d)})

        c.append(cinema)
        # print(time.strftime('%d.%m %H:%M', d))
    return tuple(c)


# Функция чтения списка кинотеатров
def cinema_list(n = -1):
    parser = etree.XMLParser(encoding="utf-8")
    tree = etree.parse(config.xml_file_cinema, parser=parser)
    root = tree.getroot()
    list_cinema = ''
    for child in root.find('cinema'):
        list_cinema += child.text + '\n'
    return list_cinema


# Функция чтения списка киноcеансов
def film_list(n=-1):
    parser = etree.XMLParser(encoding="utf-8")
    tree = etree.parse(config.xml_file_cinema, parser=parser)
    root = tree.getroot()
    list_cinema = ''
    for child in root.find('films'):
            list_cinema += child.text + '\n'
    return list_cinema


# вывод инлайн меню с кинотеатрами
def cinema_keyboard(n=-1):
    parser = etree.XMLParser(encoding="utf-8")
    tree = etree.parse(config.xml_file_cinema, parser=parser)
    root = tree.getroot()
    keyboard = types.InlineKeyboardMarkup()
    i=1
    first_item = sec_item = []
    for child in root.find('cinema'):
        # keyboard.add(types.InlineKeyboardButton(child.text, callback_data='cinema' + child.attrib['id']))
        if i % 2 == 1:
            global first_item
            first_item = [child.text, child.attrib['id']]
        elif i % 2 == 0:
            global sec_item
            sec_item = [child.text, child.attrib['id']]
            keyboard.row(types.InlineKeyboardButton(first_item[0], callback_data='cinema' + first_item[1]), \
                 types.InlineKeyboardButton(sec_item[0], callback_data='cinema' + sec_item[1]))
        i += 1
    if i % 2 == 0:  # если нечтеное количество фильмов, последний элемент на всю длину
        keyboard.row(types.InlineKeyboardButton(first_item[0], callback_data='cinema' + first_item[1]))
    keyboard.row(types.InlineKeyboardButton('↩ Назад', callback_data='start_menu'))
    return keyboard


# вывод инлайн меню с фильмами
def films_keyboard(n=-1):
    parser = etree.XMLParser(encoding="utf-8")
    tree = etree.parse(config.xml_file_cinema, parser=parser)
    root = tree.getroot()
    keyboard = types.InlineKeyboardMarkup()
    i=1
    first_item = sec_item = []
    for child in root.find('films'):
        # keyboard.add(types.InlineKeyboardButton(child.text, callback_data='cinema' + child.attrib['id']))
        if i % 2 == 1:
            global first_item
            first_item = [child.text, child.attrib['id']]
        elif i % 2 == 0:
            global sec_item
            sec_item = [child.text, child.attrib['id']]
            keyboard.row(types.InlineKeyboardButton(first_item[0], callback_data='film' + first_item[1]), \
                 types.InlineKeyboardButton(sec_item[0], callback_data='film' + sec_item[1]))
        i += 1
    if i % 2 == 0:  # если нечтеное количество фильмов, последний элемент на всю длину
        keyboard.row(types.InlineKeyboardButton(first_item[0], callback_data='film' + first_item[1]))
    keyboard.row(types.InlineKeyboardButton('↩ Назад', callback_data='start_menu'))
    return keyboard


# вывод списка фильма пол id кинотеатра
def get_films_by_cinema(cinema_index):
    parser = etree.XMLParser(encoding="utf-8")
    tree = etree.parse(config.xml_file_cinema, parser=parser)
    root = tree.getroot()

    c = []  # список киносеансов текстом
    for child in root.find('sessions'):
        if str(cinema_index) == child.attrib['cinema_id']:
            cinema = {}
            d = time.localtime(int(child.attrib['timestamp'].split('.')[0]))
            cinema.update({'time': time.strftime('%H:%M', d)})
            cinema.update({'film': child.attrib['film']})
            cinema.update({'cinema': child.attrib['cinema']})
            cinema.update({'hall': child.attrib['hall']})
            cinema.update({'cost': child.attrib['cost']})
            cinema.update({'date_time': time.strftime('%Y%m%d%H%M', d)})
            cinema.update({'timestamp': child.attrib['timestamp']})

            if child.attrib['is_tomorrow'] == '1':
                cinema.update({'time': time.strftime('%H:%M (%d.%m)', d)})

            c.append(cinema)
            # print(time.strftime('%d.%m %H:%M', d))
    return tuple(c)


# вывод списка фильма пол id кинотеатра
def get_cinema_by_film(film_index):
    parser = etree.XMLParser(encoding="utf-8")
    tree = etree.parse(config.xml_file_cinema, parser=parser)
    root = tree.getroot()

    c = []  # список киносеансов текстом
    for child in root.find('sessions'):
        if str(film_index) == child.attrib['film_id']:
            cinema = {}
            d = time.localtime(int(child.attrib['timestamp'].split('.')[0]))
            cinema.update({'time': time.strftime('%H:%M', d)})
            cinema.update({'film': child.attrib['film']})
            cinema.update({'cinema': child.attrib['cinema']})
            cinema.update({'hall': child.attrib['hall']})
            cinema.update({'cost': child.attrib['cost']})
            cinema.update({'date_time': time.strftime('%Y%m%d%H%M', d)})
            cinema.update({'timestamp': child.attrib['timestamp']})

            if child.attrib['is_tomorrow'] == '1':
                cinema.update({'time': time.strftime('%H:%M (%d.%m)', d)})

            c.append(cinema)
            # print(time.strftime('%d.%m %H:%M', d))
    return tuple(c)
