import pexpect
import pyotp
import time


class VPNConnection:
    def __init__(self):
        self.vpn_command = "/opt/cprongate/ngateconsoleclient"
        self.vpn_url = "https://ngvpn.1cupis.org"

    def get_totp(self, secret_key):
        """Генерирует текущий TOTP токен."""
        totp = pyotp.TOTP(secret_key)
        return totp.now()

    def connect(self, login, password, secret_key):
        """Выполняет подключение к VPN с OTP и поддерживает соединение активным."""
        command = [
            self.vpn_command,
            "-vvv",
            "-u", login,
            "-p", password,
            self.vpn_url,
        ]

        try:
            child = pexpect.spawn(' '.join(command), timeout=60)

            # Ждем появления приглашения ввода OTP
            child.expect("Please enter OTP for authentication:", timeout=30)
            print("🔒 Обнаружено приглашение ввода OTP...")

            otp = self.get_totp(secret_key)
            print(f"🔑 Сгенерированный OTP: {otp}")

            # Отправляем OTP
            child.sendline(otp)

            # Ожидаем успешного подключения
            result = child.expect(['VPN Online', 'Error', pexpect.TIMEOUT, pexpect.EOF], timeout=5)

            if result == 0:
                print("✅ Успешное подключение!")
            elif result == 1:
                print("❌ Ошибка подключения!")
                return False
            else:
                print("⚠️ Неизвестный статус подключения")
                return False

            # Цикл поддержания соединения
            print("\n🔄 Соединение активно. Нажмите Ctrl+C для завершения.\n")
            return self._maintain_connection(child)

        except pexpect.exceptions.TIMEOUT:
            print("⌛ Превышено время ожидания при подключении")
            return False
        except Exception as e:
            print(f"❌ Ошибка при подключении: {str(e)}")
            return False

    def _maintain_connection(self, child):
        """Поддерживает соединение активным и обрабатывает его статус."""
        while True:
            try:
                # Проверяем, не закрылось ли соединение
                if not child.isalive():
                    print("❌ Соединение разорвано!")
                    return False

                # Выводим периодически информацию о состоянии соединения
                print(f"⏰ Соединение активно: {time.strftime('%Y-%m-%d %H:%M:%S')}")

                # Обрабатываем вывод из сессии
                if child.expect(['.+', pexpect.TIMEOUT, pexpect.EOF], timeout=5) == 0:
                    output = child.match.group(0).decode('utf-8', errors='replace')
                    if output.strip():
                        print(f"📤 Получено: {output}")

                time.sleep(10)  # Делаем паузу перед следующей проверкой

            except KeyboardInterrupt:
                print("\n🛑 Завершение по запросу пользователя...")
                if child.isalive():
                    child.close(force=True)
                return True
            except Exception as e:
                print(f"⚠️ Ошибка: {str(e)}")
                if child.isalive():
                    child.close(force=True)
                return False