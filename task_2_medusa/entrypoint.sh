#!/bin/bash

# Запуск setup для создания пользователя и SSH
./setup.sh

# Запуск брутфорса
./medusa_bruteforce.sh

# Держим контейнер активным
echo ""
echo "Нажмите Ctrl+C для выхода или Enter для bash..."
read -t 10
/bin/bash

