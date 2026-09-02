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

        while True:
            master_password = getpass.getpass("🔐 Создайте мастер-пароль для шифрования: ")

            if len(master_password) < 6:
                print("❌ Мастер-пароль должен содержать не менее 6 символов.")
                continue

            confirm_master_password = getpass.getpass("🔐 Подтвердите мастер-пароль: ")

            if master_password != confirm_master_password:
                print("❌ Мастер-пароли не совпадают.")
                continue

            break

        return login, password, secret_key, master_password

    @staticmethod
    def get_master_password():
        """Запрашивает мастер-пароль для расшифровки"""
        return getpass.getpass("🔐 Введите мастер-пароль для расшифровки: ")

    @staticmethod
    def get_new_password():
        """Запрашивает новый пароль и подтверждение"""
        new_password = getpass.getpass("🔐 Введите новый PASSWORD: ")
        confirm_password = getpass.getpass("🔐 Подтвердите новый PASSWORD: ")

        if new_password != confirm_password:
            print("❌ Пароли не совпадают.")
            return None

        return new_password


def log_time(message):
    """Выводит сообщение с текущим временем"""
    print(f"{message}: {time.strftime('%Y-%m-%d %H:%M:%S')}")