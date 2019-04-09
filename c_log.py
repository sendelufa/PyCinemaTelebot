# Copyright 2018 Shibkov Konstantin <sendel@sendel.ru>
# All rights reserved. MIT License.
# logging text messages from user

import time


def write_log_file(txt):
    log_date = time.strftime("%d.%m.%Y %H:%M", time.localtime())
    txt = str(log_date) + " " + txt
    try:
        file = open('log.txt', "a")
        file.write(txt)
        file.close()
    except PermissionError:
        print('ошибка доступа к файлу')


def log_text(m):
    # print("\n\n", log_date, "\n\n")
    if not m.chat.id == 1181136:

        txt = "u=" + m.from_user.username + "(" + str(m.chat.id) + ') ' + "t=" + m.text + "\n"
        write_log_file(txt)


def log_text_call(call):
    if not call.message.chat.id == 1181136:
        txt = "u=" + call.from_user.username + "(" + str(call.message.chat.id) + ') ' + "t=" + call.data + "\n"
        write_log_file(txt)


