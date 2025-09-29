import getpass
import time
import sys


class InputHandler:
    @staticmethod
    def collect_new_credentials():
        """Собирает новые учетные данные от пользователя"""
        login = input("👤 Введите LOGIN: ")
        password = getpass.getpass("🔐 Введите PASSWORD: ")
        secret_key = getpass.getpass("🔑 Введите SECRET_KEY: ")

        master_password = getpass.getpass("🔐 Создайте мастер-пароль для шифрования: ")
        confirm_master_password = getpass.getpass("🔐 Подтвердите мастер-пароль: ")

        if master_password != confirm_master_password:
            print("❌ Мастер-пароли не совпадают. Выход.")
            sys.exit(1)

        return login, password, secret_key, master_password

    @staticmethod
    def get_master_password():
        """Запрашивает мастер-пароль для расшифровки"""
        return getpass.getpass("🔐 Введите мастер-пароль для расшифровки: ")


def log_time(message):
    """Выводит сообщение с текущим временем"""
    print(f"{message}: {time.strftime('%Y-%m-%d %H:%M:%S')}")