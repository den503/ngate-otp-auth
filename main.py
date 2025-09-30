import time
import sys
from database import CredentialsManager
from connection import VPNConnection
from utils import InputHandler, log_time


def show_menu():
    """Отображает меню с доступными действиями"""
    print("\n📋 Меню:")
    print("1. Подключиться к VPN")
    print("2. Сменить пароль")
    print("3. Выход")
    return input("Выберите действие (1-3): ")


def change_password(credentials_manager, input_handler):
    """Функция для смены пароля"""
    print("\n🔄 Смена пароля")

    # Запрашиваем мастер-пароль для аутентификации
    master_password = input_handler.get_master_password()

    # Проверяем, правильный ли мастер-пароль, пытаясь получить учетные данные
    login, old_password, secret_key = credentials_manager.get_credentials(master_password)

    if not login or not old_password or not secret_key:
        print("❌ Неверный мастер-пароль. Операция отменена.")
        return None, None, None

    # Запрашиваем новый пароль
    new_password = input_handler.get_new_password()

    if not new_password:
        print("❌ Смена пароля отменена.")
        return login, old_password, secret_key

    # Обновляем пароль
    success = credentials_manager.update_password(new_password, master_password)

    if success:
        print("✅ Пароль успешно изменен!")
        return login, new_password, secret_key
    else:
        print("❌ Не удалось изменить пароль.")
        return login, old_password, secret_key


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

    # Основной цикл программы с меню
    while True:
        choice = show_menu()

        if choice == "1":
            # Подключение к VPN
            try:
                print("\n🚀 Запуск подключения...")
                success = vpn_connection.connect(login, password, secret_key)

                if not success:
                    print("⚠️ Соединение было разорвано. Возвращение в меню...")
                    time.sleep(3)
            except KeyboardInterrupt:
                print("\n👋 Подключение прервано пользователем.")
            except Exception as e:
                print(f"❌ Непредвиденная ошибка: {str(e)}")
                print("🔄 Возврат в меню через 3 секунды...")
                time.sleep(3)

        elif choice == "2":
            # Смена пароля
            login, password, secret_key = change_password(credentials_manager, input_handler)

        elif choice == "3":
            # Выход
            print("\n👋 Программа завершена.")
            break

        else:
            print("⚠️ Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")


if __name__ == "__main__":
    main()