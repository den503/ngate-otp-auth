import time
import sys
from database import CredentialsManager
from connection import VPNConnection
from utils import InputHandler, log_time


def main():
    # Инициализация менеджеров
    credentials_manager = CredentialsManager()
    vpn_connection = VPNConnection()
    input_handler = InputHandler()

    login = None
    password = None
    secret_key = None

    # Проверяем наличие сохраненных учетных данных
    if credentials_manager.has_credentials():
        print("📋 Найдены сохраненные учетные данные")
        master_password = input_handler.get_master_password()
        login, password, secret_key = credentials_manager.get_credentials(master_password)

        # Если расшифровка не удалась, выходим
        if not login or not password or not secret_key:
            print("❌ Не удалось получить учетные данные. Выход.")
            sys.exit(1)
    else:
        print("📝 Необходимо ввести учетные данные для первого запуска")
        login, password, secret_key, master_password = input_handler.collect_new_credentials()

        credentials_manager.save_credentials(login, password, secret_key, master_password)
        print("✅ Учетные данные успешно сохранены")

    log_time("⏰ Время запуска")

    # Цикл поддержания работы скрипта
    while True:
        try:
            print("\n🚀 Запуск подключения...")
            success = vpn_connection.connect(login, password, secret_key)

            if not success:
                print("⚠️ Соединение было разорвано. Повторное подключение через 10 секунд...")
                time.sleep(10)
            else:
                # Если успешно завершено по запросу пользователя
                break

        except KeyboardInterrupt:
            print("\n👋 Программа завершена пользователем.")
            break
        except Exception as e:
            print(f"❌ Непредвиденная ошибка: {str(e)}")
            print("🔄 Перезапуск через 30 секунд...")
            time.sleep(30)


if __name__ == "__main__":
    main()