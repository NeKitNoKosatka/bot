import vk
from dotenv import load_dotenv
import os


def is_can_write_private_message(user):
    message_access = vk_api.users.get(user_ids=user, fields="can_write_private_message",  v=5.92)
    return message_access[0]['can_write_private_message']

def get_members(groupid):  # функция формирования базы участников сообщества в виде списка
    first = vk_api.groups.getMembers(group_id=groupid, v=5.92)  # Первое выполнение метода
    data = first["items"]  # присваиваем переменной первую тысячу id'шников
    count = first["count"] // 1000  # присваиваем переменной количество тысяч участников
    for i in range(1, count + 1):
        data = data + vk_api.groups.getMembers(group_id=groupid, v=5.92, offset=i * 1000)["items"]
    return data


def save_data(data, filename="users_id.txt"):  # функция сохранения базы в txt файле
    with open(filename, "w") as file:
        # записываем каждый id'шник в новой строке,
        # добавляя в начало "vk.com/id", а в конец перенос строки.
        for item in data:
            file.write("vk.com/id" + str(item) + "\n")


def enter_data(filename="users_id.txt"):  # функция вывода базы из txt файла
    with open(filename) as file:
        b = []
        # записываем каждую строчку файла в список,
        # убирая "vk.com/id" и "\n" с помощью среза.
        for line in file:
            # vk_user_id = line[9:len(line) - 1]
            # if is_can_write_private_message(vk_user_id) == 1:
            b.append(line[9:len(line) - 1])
    return b

def console_interface(): # интерфейс для управления системой парсинга из консоли
    print("\n1. Парсинг участников одного сообщества\n2. Парсинг участников двух сообществ (без повторов)\n3. Найти пересечение участников двух сообществ\n4. Добавить ботов\n5. Запуск рассылки\n")
    choise = input("Выберите действие (введите цифру): ")
    while True:
        if choise == "1":
            print("Парсинг участников одного сообщества\n")
            groupid = input("Введите id группы для парсинга участников: ")
            data = get_members(groupid)
            save_data(data)
            if data != None:
                print("Парсинг прошёл успешно\nДанные сохранены в файл users_id.txt\n")
            else:
                print("Парсинг не удался\n")

        elif choise == "2":
            print("Парсинг участников двух сообществ (без повторов)\n")
            groupid_1 = input("Введите id 1-ой группы для парсинга участников: ")
            groupid_2 = input("Введите id 2-ой группы для парсинга участников: ")
            group_1 = get_members(groupid_1)
            group_2 = get_members(groupid_2)
            data = union_members(group_1, group_2)
            save_data(data)
            if data != None:
                print("Парсинг прошёл успешно\nДанные сохранены в файл users_id.txt\n")
            else:
                print("Парсинг не удался\n")

        elif choise == "3":
            print("Найти пересечение участников двух сообществ\n")
            groupid_1 = input("Введите id 1-ой группы для парсинга участников: ")
            groupid_2 = input("Введите id 2-ой группы для парсинга участников: ")
            group_1 = get_members(groupid_1)
            group_2 = get_members(groupid_2)
            data = get_intersection(group_1, group_2)
            save_data(data)
            if data != None:
                print("Парсинг прошёл успешно\nДанные сохранены в файл users_id.txt\n")
            else:
                print("Парсинг не удался\n")

        elif choise == "4":
            print("Добавить ботов\n")
            return "да"
            break

        elif choise == "5":
            print("Запустить рассылку\n")
            return "нет"
            break

        else:
            print("Неверный ввод\n")

        print("1. Парсинг участников одного сообщества\n2. Парсинг участников двух сообществ (без повторов)\n3. Найти пересечение участников двух сообществ\n4. Добавить ботов\n5. Запуск рассылки\n")
        choise = input("Выберите действие (введите цифру): ")



def get_intersection(group1, group2): # функция нахождения пересечений двух баз
    group1 = set(group1)
    group2 = set(group2)
    intersection = group1.intersection(group2)  # находим пересечение двух множеств
    all_members = len(group1) + len(group2) - len(intersection)
    result = len(intersection)/all_members * 100  # высчитываем пересечение в процентах
    print("Пересечение аудиторий: ", round(result,2), "%", sep="")
    return list(intersection)


def union_members(group1, group2): # функция объединения двух баз без повторов
    group1 = set(group1)
    group2 = set(group2)
    union = group1.union(group2)  # объединяем два множества
    return list(union)


#if __name__ == "__main__":
path = os.path.join(os.path.dirname(__file__), 'db.config')
load_dotenv(path)
token = os.getenv("ACCESS_TOKEN")  # Сервисный ключ доступа
session = vk.Session(access_token=token)  # Авторизация
vk_api = vk.API(session)

    #console_interface()

