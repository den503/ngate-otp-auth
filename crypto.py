from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64


class CryptoManager:
    def __init__(self):
        # В реальном проекте используйте случайную соль и храните её безопасно
        self.salt = b'static_salt_for_example'
        self.iterations = 100000

    def get_encryption_key(self, master_password):
        """Создаёт ключ шифрования на основе мастер-пароля"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=self.iterations,
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key

    def encrypt_data(self, data, master_password):
        """Шифрует данные используя мастер-пароль"""
        key = self.get_encryption_key(master_password)
        f = Fernet(key)
        return f.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data, master_password):
        """Расшифровывает данные используя мастер-пароль"""
        key = self.get_encryption_key(master_password)
        f = Fernet(key)
        return f.decrypt(encrypted_data.encode()).decode()