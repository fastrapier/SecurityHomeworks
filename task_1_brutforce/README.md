# Task 1: Брутфорс 7z архива

Автоматический брутфорс `flag.7z` с помощью John The Ripper в Docker (Kali Linux).

## Быстрый запуск

```bash
make
```

или

```bash
docker build -t kali-bruteforce . && docker run -it kali-bruteforce
```

Контейнер автоматически запустит брутфорс при старте.

## Команды Make

```bash
make build    # Собрать образ
make run      # Запустить брутфорс
make all      # Собрать и запустить (по умолчанию)
make clean    # Удалить контейнеры и образ
```

## Ручной режим

```bash
# Запустить контейнер с bash
docker run -it kali-bruteforce /bin/bash

# Внутри контейнера
7z2john flag.7z > flag.hash
john --wordlist=/usr/share/wordlists/rockyou.txt flag.hash
john --show flag.hash
7z x flag.7z
```





