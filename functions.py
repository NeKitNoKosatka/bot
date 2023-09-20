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
    #mes = "".join()
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
    # counter_2 = [0 for _ in range(len(Bots))]
    #len(users) != user_number

    while flag:
        bot_number = 1
        for bot in Bots:
            counter[bot_number - 1] = 0
            # counter_2[bot_number - 1] = 0
            # for i in range(20):
            while counter[bot_number-1] != 2:
                if user_number != len(users):
                    error_num = bot.send_message(users[user_number], message_txt)
                    #print(parsing_system.is_can_write_private_message(users[user_number]))
                    # message_access = parsing_system.is_can_write_private_message(users[user_number])
                    if error_num is None:
                        counter[bot_number - 1] += 1
                        # counter[bot_number - 1] -= 1  #
                        #print("counter = ", counter)
                        print("bot_number = ", bot_number)
                        pass
                    else:
                        #counter += 1
                        print("error: " + error_num) # 5 - ошибка в токене, 9 - у пользователя закрыты сообщения, 7 - неправильное id
                        # прочитаем файл построчно
                        # counter[bot_number-1] += 1  #
                        # print("counter = ", counter)
                        # print("bot_number = ", bot_number)
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

            #user_number += 20
            # print("\nБот №", bot_number,
            #       "\nИсчерпан лимит сообщений в день\nРассылка приостановлена\nРежим ожидания(осталось): 24 часа\nНачало режима ожидания: ",
            #       now.strftime("%H:%M %d-%m-%Y"))
            # print("Пользователей для рассылки осталось: ", len(users) - user_number, "\n")
            bot_number += 1

        if flag and user_number != len(users):
            print("Все боты в режиме ожидания")
            # print("Рассылка оставшимся пользователям займёт: ", (len(users) - user_number) / len(Bots) // 3600, " часов, ",
            #       (len(users) - user_number) / len(Bots) % 3600 // 60, " минут")
            time.sleep(43200) #43200
            print("\nРежим ожидания(осталось): 12 часов\n")
            time.sleep(43200)
            print("Рассылка возобновлена\n")

    return flag


config = configparser.ConfigParser()





# if __name__ == '__main__':
#
#     message = "".join((message()))
#     if message == "":
#         print("Не указано сообщение для рассылки\nВведите сообщение для рассылки в файл message.txt\n")
#         sys.exit()
#
#     choise = parsing_system.console_interface()  # запуск консольного интерфейса
#     users = parsing_system.enter_data()  # чтение id'шников из файла users.txt
#
#     print("Всего ботов доступно: ", len(get_all_tokens())-1, "\n")
#     while choise != "да" or choise != "нет":
#         print("Добавить новых ботов? (да/нет)")
#         choise = input("Введите ответ: ")
#         if choise == "да":
#             bot_nums = int(input("Введите число новых ботов: "))
#             add_bots(bot_nums)
#             choise = ""
#             break
#         elif choise == "нет":
#             choise = ""
#             break
#         else:
#             print("Неверный ввод\n")
#
#     Bots = get_bots()
#     now = datetime.datetime.now() # текущее время
#
#     print("Пользователей для рассылки: ", len(users))
#     print("Рассылка всем пользователям займёт: ", len(users) / len(Bots) // 3600 + (len(users) // 20) * 24, " часов, ", len(users) / len(Bots) % 3600 // 60, " минут\n")
#
#     choise = ""
#     while choise != "да" or choise != "нет":
#         print("Начать рассылку? (да/нет)")
#         choise = input("Введите ответ: ")
#         if choise == "да":
#             break
#         elif choise == "нет":
#             sys.exit()
#         else:
#             print("Неверный ввод\n")
#
#     '''
#     У Вконтакте ограничение на отправку сообщений незнакомым людям (которых нет в друзьях):
#     20 новых диалогов в день.
#
#     Каждые 24 часа бот посылает сообщение 20-ти людям из списка id'шников с интервалом в секунду.
#     '''
#
#     user_number = 0
#
#     while len(users) != user_number:
#         bot_number = 1
#         for bot in Bots:
#             try:
#                 for i in range(user_number, user_number+20):
#                     bot.send_message(users[i], message)
#                     user_number += 1
#                     time.sleep(1)
#
#                 print("\nБот №", bot_number, "\nИсчерпан лимит сообщений в день\nРассылка приостановлена\nРежим ожидания(осталось): 24 часа\nНачало режима ожидания: ", now.strftime("%H:%M %d-%m-%Y"))
#                 print("Пользователей для рассылки осталось: ", len(users)-user_number, "\n")
#                 bot_number += 1
#
#             except IndexError:
#                 print("Все пользователи получили рассылку\n")
#                 input()
#                 sys.exit()
#
#         print("Все боты в режиме ожидания")
#         print("Рассылка оставшимся пользователям займёт: ", (len(users) - user_number) / len(Bots) // 3600, " часов, ", (len(users) - user_number) / len(Bots) % 3600 // 60, " минут")
#         time.sleep(43200)
#         print("\nРежим ожидания(осталось): 12 часов\n")
#         time.sleep(43200)
#         print("Рассылка возобновлена\n")