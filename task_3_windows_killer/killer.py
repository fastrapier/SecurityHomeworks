#!/usr/bin/env python3
"""
Windows Killer - Демонстрация техники File Masquerading (MITRE ATT&CK T1036)
Образовательный проект для демонстрации маскировки вредоносных файлов
"""

import shutil
import time
from datetime import datetime
from pathlib import Path


def log(message):
    """Простое логирование без эмодзи"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def create_test_environment():
    """Создание тестовой среды с директорией Windows32"""
    log("Создание тестовой среды...")

    # Создаем тестовую системную папку
    test_dir = Path("/test_windows32")
    if test_dir.exists():
        shutil.rmtree(test_dir)

    test_dir.mkdir(parents=True)

    # Создаем тестовые системные файлы
    test_files = [
        "kernel32.dll",
        "ntdll.dll",
        "user32.dll",
        "advapi32.dll",
        "system.ini",
        "config.sys"
    ]

    for filename in test_files:
        filepath = test_dir / filename
        filepath.write_text(f"Test system file: {filename}\n")

    log(f"Создана тестовая папка: {test_dir}")
    log(f"Создано файлов: {len(test_files)}")

    return test_dir


def masquerade_files():
    """Создание замаскированных копий скрипта"""
    log("Начало процесса маскировки файлов...")

    current_script = Path(__file__)

    # Создаем поддельные системные директории
    fake_dirs = [
        Path("/fake_system32"),
        Path("/fake_program_files"),
        Path("/fake_windows")
    ]

    for fake_dir in fake_dirs:
        fake_dir.mkdir(parents=True, exist_ok=True)

    # Маскировка под документы с двойным расширением
    masquerade_files_list = [
        ("/fake_program_files/document.pdf.exe", "Документ PDF (на самом деле исполняемый файл)"),
        ("/fake_program_files/report.txt.exe", "Текстовый отчет (на самом деле исполняемый файл)"),
        ("/fake_program_files/data.docx.exe", "Документ Word (на самом деле исполняемый файл)"),
        ("/fake_system32/svchost.exe", "Системный процесс (легитимное имя)"),
        ("/fake_system32/pythonw.exe", "Python процесс (легитимное имя)"),
        ("/fake_windows/WindowsUpdate.exe", "Обновление Windows (легитимное имя)"),
        ("/fake_system32/update.exe", "Процесс обновления (легитимное имя)")
    ]

    log("Создание замаскированных копий:")
    for target_path, description in masquerade_files_list:
        target = Path(target_path)
        shutil.copy2(current_script, target)
        log(f"  -> {target.name} - {description}")

    log(f"Всего создано замаскированных файлов: {len(masquerade_files_list)}")

    # Показываем список файлов в поддельных системных директориях
    log("\nСодержимое поддельных системных папок:")
    for fake_dir in fake_dirs:
        files = list(fake_dir.iterdir())
        log(f"  {fake_dir}: {len(files)} файлов")
        for f in files:
            log(f"    - {f.name}")


def find_and_destroy_target():
    """Поиск и удаление целевой директории"""
    log("\nНачало поиска целевой директории...")

    target_dir = Path("/test_windows32")

    if not target_dir.exists():
        log(f"ОШИБКА: Целевая директория не найдена: {target_dir}")
        return False

    log(f"ОБНАРУЖЕНА целевая директория: {target_dir}")

    # Подсчет файлов
    files = list(target_dir.iterdir())
    file_count = len(files)

    log(f"Найдено файлов для удаления: {file_count}")

    # Показываем содержимое перед удалением
    log("Содержимое целевой директории:")
    for f in files:
        log(f"  - {f.name} ({f.stat().st_size} bytes)")

    # Удаление файлов
    log("\nНачало удаления файлов...")
    deleted_count = 0

    for f in files:
        try:
            f.unlink()
            deleted_count += 1
            log(f"  Удален: {f.name}")
        except Exception as e:
            log(f"  ОШИБКА при удалении {f.name}: {e}")

    # Удаление самой директории
    try:
        target_dir.rmdir()
        log(f"\nДиректория удалена: {target_dir}")
    except Exception as e:
        log(f"ОШИБКА при удалении директории: {e}")
        return False

    # Проверка успешного удаления
    if not target_dir.exists():
        log(f"\nПодтверждение: целевая директория больше не существует")
        log(f"Статистика: удалено {deleted_count} из {file_count} файлов")
        return True
    else:
        log("ОШИБКА: Директория все еще существует")
        return False


def demonstrate_masquerading():
    """Основная функция демонстрации техники маскировки"""
    log("=" * 70)
    log("Windows Killer - Демонстрация File Masquerading")
    log("MITRE ATT&CK T1036: Masquerading")
    log("=" * 70)
    log("")

    # Этап 1: Создание тестовой среды
    log("ЭТАП 1: Создание тестовой среды")
    log("-" * 70)
    test_dir = create_test_environment()
    log("")
    time.sleep(1)

    # Этап 2: Маскировка файлов
    log("ЭТАП 2: Маскировка вредоносных файлов")
    log("-" * 70)
    masquerade_files()
    log("")
    time.sleep(1)

    # Этап 3: Удаление целевой директории
    log("ЭТАП 3: Поиск и удаление целевой директории")
    log("-" * 70)
    success = find_and_destroy_target()
    log("")

    # Итоги
    log("=" * 70)
    if success:
        log("ЗАВЕРШЕНО: Демонстрация успешно выполнена")
    else:
        log("ЗАВЕРШЕНО: Демонстрация выполнена с ошибками")
    log("=" * 70)


if __name__ == "__main__":
    demonstrate_masquerading()

