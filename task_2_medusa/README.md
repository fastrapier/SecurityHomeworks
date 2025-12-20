# Task 2: Брутфорс SSH с Medusa

Брутфорс SSH с помощью Medusa в Docker контейнере с Kali Linux.

## Описание

Контейнер автоматически:
1. Создает тестового пользователя `testuser` с паролем `password123`
2. Запускает SSH-сервер на localhost
3. Выполняет брутфорс с помощью Medusa и словаря паролей

## Быстрый запуск

```bash
make
```

## Команды

```bash
make build    # Собрать образ
make run      # Запустить брутфорс
make all      # Собрать и запустить
make clean    # Удалить контейнеры и образ
```

## Параметры атаки

- **Цель**: 127.0.0.1
- **Пользователь**: testuser
- **Пароль**: password123
- **Словарь**: /task/wordlist.txt (120+ паролей)
- **Модуль**: SSH

## Ручной запуск

```bash
docker build -t kali-medusa .
docker run -it kali-medusa

# Или с bash
docker run -it kali-medusa /bin/bash
./setup.sh
./medusa_bruteforce.sh
```

## Использование rockyou.txt

Для полного словаря rockyou.txt (14M+ паролей):
1. Отредактируйте `medusa_bruteforce.sh`
2. Замените `WORDLIST="/task/wordlist.txt"` на `WORDLIST="/usr/share/wordlists/rockyou.txt"`
3. Пересоберите: `make clean && make build`

Внимание: брутфорс с rockyou.txt займет много времени!

