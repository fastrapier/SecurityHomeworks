#!/bin/bash

echo "========================================="
echo "  Настройка SSH-сервера"
echo "========================================="
echo ""

# Цвета
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Создание тестового пользователя
echo -e "${YELLOW}[*] Создание пользователя testuser...${NC}"
useradd -m -s /bin/bash testuser
echo "testuser:password123" | chpasswd
echo -e "${GREEN}[+] Пользователь testuser создан с паролем password123${NC}"
echo ""

# Генерация SSH ключей если их нет
if [ ! -f /etc/ssh/ssh_host_rsa_key ]; then
    echo -e "${YELLOW}[*] Генерация SSH ключей...${NC}"
    ssh-keygen -A
    echo -e "${GREEN}[+] SSH ключи сгенерированы${NC}"
    echo ""
fi

# Запуск SSH сервера
echo -e "${YELLOW}[*] Запуск SSH сервера...${NC}"
/usr/sbin/sshd -D &
SSH_PID=$!

# Ждем запуска SSH
sleep 5

# Проверка запуска
if ps -p $SSH_PID > /dev/null; then
    echo -e "${GREEN}[+] SSH сервер запущен (PID: $SSH_PID)${NC}"
    echo ""
else
    echo -e "${RED}[!] Ошибка запуска SSH сервера${NC}"
    exit 1
fi

