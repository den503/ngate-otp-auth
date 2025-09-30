import json
import os
from crypto import CryptoManager


class CredentialsManager:
    def __init__(self, json_path='credentials.json'):
        self.json_path = json_path
        self.crypto = CryptoManager()

    def has_credentials(self):
        """Проверяет, есть ли учетные данные в файле"""
        return os.path.exists(self.json_path)

    def save_credentials(self, login, password, secret_key, master_password):
        """Сохраняет учетные данные в JSON файле"""
        encrypted_password = self.crypto.encrypt_data(password, master_password)
        encrypted_secret_key = self.crypto.encrypt_data(secret_key, master_password)

        credentials_data = {
            'login': login,
            'password': encrypted_password,
            'secret_key': encrypted_secret_key
        }

        with open(self.json_path, 'w') as json_file:
            json.dump(credentials_data, json_file)

    def get_credentials(self, master_password):
        """Получает и расшифровывает учетные данные из JSON файла"""
        if not os.path.exists(self.json_path):
            return None, None, None

        try:
            with open(self.json_path, 'r') as json_file:
                credentials_data = json.load(json_file)

            login = credentials_data.get('login')
            encrypted_password = credentials_data.get('password')
            encrypted_secret_key = credentials_data.get('secret_key')

            if not login or not encrypted_password or not encrypted_secret_key:
                return None, None, None

            password = self.crypto.decrypt_data(encrypted_password, master_password)
            secret_key = self.crypto.decrypt_data(encrypted_secret_key, master_password)
            return login, password, secret_key

        except Exception:
            return None, None, None

    def update_password(self, new_password, master_password):
        """Обновляет только пароль, сохраняя существующие логин и secret_key"""
        if not os.path.exists(self.json_path):
            return False

        try:
            # Загружаем текущие данные
            with open(self.json_path, 'r') as json_file:
                credentials_data = json.load(json_file)

            encrypted_secret_key = credentials_data.get('secret_key')

            # Расшифровываем secret_key для проверки правильности мастер-пароля
            try:
                self.crypto.decrypt_data(encrypted_secret_key, master_password)
            except:
                return False  # Неверный мастер-пароль

            # Шифруем новый пароль
            encrypted_password = self.crypto.encrypt_data(new_password, master_password)

            # Обновляем данные
            credentials_data['password'] = encrypted_password

            # Сохраняем обновленные данные
            with open(self.json_path, 'w') as json_file:
                json.dump(credentials_data, json_file)

            return True

        except Exception:
            return False