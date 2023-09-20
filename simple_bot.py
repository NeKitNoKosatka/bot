import vk_api
from vk_api.utils import get_random_id
from dotenv import load_dotenv
import os


class Bot:
    """
    Базовый класс бота ВКонтакте
    """

    # текущая сессия ВКонтакте
    vk_session = None

    # доступ к API ВКонтакте
    vk_api_access = None

    # пометка авторизованности
    authorized = False

    # пользователь по умолчанию
    # id пользователя ВКонтакте (например, 1234567890) в виде строки
    # default_user_id = 243416190

    def __init__(self, token=os.getenv("ACCESS_TOKEN")):
        """
        Инициализация бота при помощи получения доступа к API ВКонтакте
        """
        # загрузка информации из .env-файла
        path = os.path.join(os.path.dirname(__file__), 'data.env')
        load_dotenv(path)

        # авторизация
        self.vk_api_access = self.do_auth(token)

        if self.vk_api_access is not None:
            self.authorized = True

        # получение id пользователя из файла настроек окружения .env в виде строки USER_ID="1234567890"
        self.default_user_id = os.getenv("USER_ID")

    def do_auth(self, token):
        """
        Авторизация за пользователя (не за группу или приложение)
        Использует переменную, хранящуюся в файле настроек окружения .env в виде строки ACCESS_TOKEN="1q2w3e4r5t6y7u8i9o..."
        :return: возможность работать с API
        """
        #token = os.getenv("ACCESS_TOKEN")

        try:
            self.vk_session = vk_api.VkApi(token=token)
            return self.vk_session.get_api()
        except Exception as error:
            print(error)
            return None

    def send_message(self, receiver_user_id: str = None, message_text: str = "тестовое сообщение"):
        """
        Отправка сообщения от лица авторизованного пользователя
        :param receiver_user_id: уникальный идентификатор получателя сообщения
        :param message_text: текст отправляемого сообщения
        """
        if not self.authorized:
            print("Unauthorized. Check if ACCESS_TOKEN is valid")
            return

        # если не указан ID - берём значение по умолчанию, если таковое указано в .env-файле
        if receiver_user_id is None:
            receiver_user_id = self.default_user_id

        try:
            self.vk_api_access.messages.send(user_id=receiver_user_id, message=message_text, random_id=get_random_id())
            print(f"Сообщение отправлено для ID {receiver_user_id} с текстом: {message_text}")
        except Exception as error:
            print(error)
            return str(error)[1]