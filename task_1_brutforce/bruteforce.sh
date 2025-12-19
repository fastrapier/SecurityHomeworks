#!/bin/bash

# Скрипт для брутфорса 7z архива с помощью John The Ripper
# Автор: Студеникин Даниил 11-312

echo "========================================="
echo "  Брутфорс 7z архива с John The Ripper"
echo "========================================="
echo ""

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Проверка наличия необходимых утилит
check_requirements() {
    echo -e "${YELLOW}[*] Проверка наличия необходимых утилит...${NC}"

    if ! command -v john &> /dev/null; then
        echo -e "${RED}[!] John The Ripper не найден!${NC}"
        exit 1
    fi

    if ! command -v 7z2john &> /dev/null; then
        echo -e "${RED}[!] 7z2john не найден!${NC}"
    fi

    if ! command -v 7z &> /dev/null; then
        echo -e "${RED}[!] 7z не найден!${NC}"
        exit 1
    fi

    echo -e "${GREEN}[+] Все необходимые утилиты найдены!${NC}"
    echo ""
}

# Проверка наличия архива
check_archive() {
    if [ ! -f "flag.7z" ]; then
        echo -e "${RED}[!] Файл flag.7z не найден!${NC}"
        exit 1
    fi
    echo -e "${GREEN}[+] Архив flag.7z найден!${NC}"
    echo ""
}

# Извлечение хеша
extract_hash() {
    echo -e "${YELLOW}[*] Извлечение хеша из архива...${NC}"
    7z2john flag.7z > flag.hash 2>&1

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}[+] Хеш успешно извлечен в файл flag.hash${NC}"
        echo ""
    else
        echo -e "${RED}[!] Ошибка при извлечении хеша${NC}"
        exit 1
    fi
}

# Показать меню выбора метода
show_menu() {
    echo "Выберите метод брутфорса:"
    echo "1) Словарная атака (по умолчанию)"
    echo "2) Словарная атака с rockyou.txt (Kali Linux)"
    echo "3) Инкрементальный режим (медленно, но надежно)"
    echo ""
    read -p "Ваш выбор [1-3]: " choice
    echo ""
}

# Брутфорс
bruteforce() {
    echo -e "${YELLOW}[*] Начинаем брутфорс...${NC}"
    echo -e "${YELLOW}[*] Это может занять некоторое время. Нажмите Ctrl+C для отмены.${NC}"
    echo ""

    case $choice in
        1)
            echo -e "${YELLOW}[*] Используем встроенный словарь John...${NC}"
            john --progress-every=5 flag.hash
            ;;
        2)
            if [ -f "/usr/share/wordlists/rockyou.txt" ]; then
                echo -e "${YELLOW}[*] Используем словарь rockyou.txt...${NC}"
                john --progress-every=5 --wordlist=/usr/share/wordlists/rockyou.txt flag.hash
            else
                echo -e "${RED}[!] rockyou.txt не найден!${NC}"
            fi
            ;;
        3)
            echo -e "${YELLOW}[*] Используем инкрементальный режим...${NC}"
            john --progress-every=5 --incremental flag.hash
            ;;
        *)
            echo -e "${RED}[!] Неверный выбор!${NC}"
            exit 1
            ;;
    esac
}

# Показать результат
show_result() {
    echo ""
    echo -e "${YELLOW}[*] Проверяем результаты...${NC}"
    echo ""

    result=$(john --show flag.hash 2>&1)

    if echo "$result" | grep -q "0 password hashes cracked"; then
        echo -e "${RED}[!] Пароль не найден!${NC}"
        echo "Попробуйте другой метод или словарь."
        echo ""
        echo "Для продолжения прерванной сессии:"
        echo "  john --restore"
        exit 1
    else
        echo -e "${GREEN}[+] ПАРОЛЬ НАЙДЕН!${NC}"
        echo ""
        john --show flag.hash
        echo ""

        # Извлекаем пароль
        password=$(echo "$result" | grep "flag.7z" | cut -d':' -f2)

        if [ ! -z "$password" ]; then
            echo -e "${YELLOW}[*] Пытаемся распаковать архив...${NC}"
            echo "$password" | 7z x flag.7z -p"$password" -y

            if [ $? -eq 0 ]; then
                echo ""
                echo -e "${GREEN}[+] Архив успешно распакован!${NC}"
                echo -e "${GREEN}[+] Содержимое:${NC}"
                ls -lh flag.* 2>/dev/null | grep -v "flag.7z\|flag.hash"
            fi
        fi
    fi
}

# Основная функция
main() {
    check_requirements
    check_archive
    extract_hash
    show_menu
    bruteforce
    show_result

    echo ""
    echo -e "${GREEN}=========================================${NC}"
    echo -e "${GREEN}  Задание выполнено!${NC}"
    echo -e "${GREEN}=========================================${NC}"
}

# Запуск
main
