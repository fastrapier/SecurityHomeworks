#!/bin/bash

# Скрипт для быстрого брутфорса 7z архива
# Автор: Студеникин Даниил 11-312

echo "========================================="
echo "  Быстрый брутфорс 7z архива"
echo "========================================="
echo ""

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Проверки
if ! command -v john &> /dev/null || ! command -v 7z &> /dev/null; then
    echo -e "${RED}[!] Необходимые утилиты не найдены${NC}"
    exit 1
fi

if [ ! -f "flag.7z" ]; then
    echo -e "${RED}[!] Файл flag.7z не найден${NC}"
    exit 1
fi

echo -e "${GREEN}[+] Архив найден${NC}"

# Извлечение хеша
echo -e "${YELLOW}[*] Извлечение хеша...${NC}"
7z2john flag.7z > flag.hash 2>&1
echo ""

# Определяем ресурсы
CPU_CORES=$(nproc 2>/dev/null || echo "4")
echo -e "${YELLOW}[*] Используем CPU ядер: $CPU_CORES${NC}"

# Проверяем GPU
GPU_SUPPORT=0
JOHN_OPTS="--fork=$CPU_CORES"
if john --list=opencl-devices 2>/dev/null | grep -q "Device #"; then
    echo -e "${GREEN}[+] Обнаружена поддержка GPU${NC}"
    GPU_SUPPORT=1
    JOHN_OPTS="--format=7z-opencl --fork=$CPU_CORES"
fi
echo ""

# Подготовка словаря
ROCKYOU_PATH=""
if [ -f "/usr/share/wordlists/rockyou.txt" ]; then
    ROCKYOU_PATH="/usr/share/wordlists/rockyou.txt"
elif [ -f "/usr/share/wordlists/rockyou.txt.gz" ]; then
    echo -e "${YELLOW}[*] Распаковка rockyou.txt.gz...${NC}"
    gunzip /usr/share/wordlists/rockyou.txt.gz
    ROCKYOU_PATH="/usr/share/wordlists/rockyou.txt"
fi

if [ -z "$ROCKYOU_PATH" ]; then
    echo -e "${RED}[!] rockyou.txt не найден${NC}"
    exit 1
fi

# Создаем оптимизированный словарь
WORDLIST_SIZE=${WORDLIST_SIZE:-10000}
echo -e "${YELLOW}[*] Создание словаря из топ $WORDLIST_SIZE паролей...${NC}"
head -n $WORDLIST_SIZE "$ROCKYOU_PATH" > /tmp/rockyou_turbo.txt
echo -e "${GREEN}[+] Словарь создан${NC}"
echo ""

# Оценка времени
ESTIMATED_SECONDS=$((WORDLIST_SIZE / 55))
ESTIMATED_MINUTES=$((ESTIMATED_SECONDS / 60))
WITH_CORES=$((ESTIMATED_MINUTES / CPU_CORES))
echo -e "${YELLOW}[*] Примерное время: ~$WITH_CORES минут${NC}"
echo ""

echo -e "${YELLOW}[*] Начинаем брутфорс...${NC}"
john --progress-every=3 $JOHN_OPTS --wordlist=/tmp/rockyou_turbo.txt flag.hash

echo ""
echo -e "${YELLOW}[*] Проверка результатов...${NC}"

result=$(john --show flag.hash 2>&1)

if echo "$result" | grep -q "0 password hashes cracked"; then
    echo -e "${RED}[!] Пароль не найден в первых $WORDLIST_SIZE записях${NC}"
    echo "Попробуйте увеличить WORDLIST_SIZE или используйте make full"
    exit 1
else
    echo -e "${GREEN}[+] ПАРОЛЬ НАЙДЕН!${NC}"
    echo ""
    john --show flag.hash
    echo ""

    password=$(echo "$result" | grep "flag.7z" | cut -d':' -f2)

    if [ ! -z "$password" ]; then
        echo -e "${YELLOW}[*] Распаковка архива...${NC}"
        echo "$password" | 7z x flag.7z -p"$password" -y > /dev/null 2>&1

        if [ $? -eq 0 ]; then
            echo -e "${GREEN}[+] Архив распакован${NC}"

            if [ -f "flag.txt" ]; then
                echo ""
                echo -e "${GREEN}[+] Содержимое flag.txt:${NC}"
                cat flag.txt
            fi
        fi
    fi
fi

echo ""
echo -e "${GREEN}[+] Готово${NC}"

