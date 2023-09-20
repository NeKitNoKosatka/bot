import sys
import os
from dotenv import load_dotenv
from simple_bot import Bot
import parsing_system
import time
import datetime
import configparser

def message(filename="message.txt"): # функция для чтения сообщения сообщения для рассылки из файла message.txt
    with open(filename, encoding='utf-8') as file:
        b = []
        for line in file:
            b.append(line)
    return "".join(b)

def edit_tokens(edited_tokens):
    config["DATA"]['TOKENS'] = ",".join(edited_tokens)
    with open('db.config', 'w') as configfile:
        config.write(configfile)


def add_bots(bot_nums, enter=None):
    new_api = []

    if enter is None:
        for i in range(bot_nums):
            enter = input("Введите токен API: ")
            new_api.append(enter)
        config['DATA']['TOKENS'] = ",".join(get_all_tokens()) + ",".join(new_api)
    else:
        config['DATA']['TOKENS'] = ",".join(get_all_tokens()) + "," + ",".join(enter)

    with open('db.config', 'w') as configfile:
        config.write(configfile)


def get_bots():
    all_api = get_all_tokens()
    bots = []
    for i in range(len(all_api)):
        token = all_api[i]
        bots.append(Bot(token))
    return bots


def get_all_tokens(filename="db.config"):
    config.read(filename)
    """
    with open(filename, encoding='utf-8') as file:
        all_tokens = file.readlines()[2][9:]
    return all_tokens.split(",")[:-1]
    """
    return config['DATA']['TOKENS'].split(",")


def all_time():
    users = parsing_system.enter_data()
    Bots = get_bots()
    all_time = len(users) + len(users) / len(Bots) // 20 * 24 * 3600
    return all_time

def get_time():
    users = parsing_system.enter_data()
    all_time_sec = all_time()

    hours = all_time_sec // 3600
    minute = all_time_sec % 3600 // 60
    seconds = all_time_sec % 3600 % 60

    time = {'hour': int(hours), 'min': int(minute), 'sec': int(seconds)}

    print("Пользователей для рассылки: ", len(users))
    print(f"Рассылка всем пользователям займёт: {hours} часов, {minute} минут, {seconds} секунд\n")

    return time

def start_mailing():
    message_txt = message()
    print("message: ", message_txt)
    users = parsing_system.enter_data()
    print("users:", users)

    Bots = get_bots()
    now = datetime.datetime.now()  # текущее время

    print("bots num: ", len(Bots))
    print("bots: ", Bots)

    user_number = 0

    flag = True
    counter = [0 for _ in range(len(Bots))]

    while flag:
        bot_number = 1
        for bot in Bots:
            counter[bot_number - 1] = 0
            while counter[bot_number-1] != 2:
                if user_number != len(users):
                    error_num = bot.send_message(users[user_number], message_txt)
                    if error_num is None:
                        counter[bot_number - 1] += 1
                        print("bot_number = ", bot_number)
                        pass
                    else:
                        print("error: " + error_num) # 5 - ошибка в токене, 9 - у пользователя закрыты сообщения, 7 - неправильное id
                        # прочитаем файл построчно
                        with open('users_id.txt', 'r') as f:
                            lines = f.readlines()

                        if lines != []:
                            with open('error_users_id.txt', 'a') as f:
                                f.writelines(lines[0] + "Ошибка: " + error_num + "\n\n")

                    user_number += 1

                    # прочитаем файл построчно
                    with open('users_id.txt', 'r') as f:
                        lines = f.readlines()
                    # запишем файл построчно пропустив первую строку
                    with open('users_id.txt', 'w') as f:
                        f.writelines(lines[1:])

                    time.sleep(1)
                elif not flag:
                    break
                else:
                    print("Все пользователи получили рассылку\n")
                    flag = False
            bot_number += 1

        if flag and user_number != len(users):
            print("Все боты в режиме ожидания")
            time.sleep(43200) #43200
            print("\nРежим ожидания(осталось): 12 часов\n")
            time.sleep(43200)
            print("Рассылка возобновлена\n")

    return flag


config = configparser.ConfigParser()
