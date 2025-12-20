# Task 1: Брутфорс 7z архива

Брутфорс `flag.7z` с помощью John The Ripper в Docker контейнере с Kali Linux.

## Быстрый запуск

```bash
make build
make turbo
```

## Доступные команды

```bash
make build    # Собрать образ
make run      # Интерактивный режим с выбором метода
make turbo    # Быстрый брутфорс (топ 10K паролей)
make quick    # Средний брутфорс (топ 100K паролей)
make full     # Полный брутфорс (весь rockyou.txt)
make clean    # Удалить контейнеры и образ
```

## Производительность

Реализована параллельная обработка и поддержка GPU для ускорения:

- **turbo**: ~10,000 паролей, время ~3-5 мин
- **quick**: ~100,000 паролей, время ~30 мин
- **full**: ~14M паролей, время несколько часов

Скрипт автоматически использует все доступные CPU ядра и OpenCL (если доступен GPU).

## Ручной запуск

```bash
docker build -t kali-bruteforce .
docker run -it kali-bruteforce

# Или с bash
docker run -it kali-bruteforce /bin/bash
7z2john flag.7z > flag.hash
john --wordlist=/usr/share/wordlists/rockyou.txt flag.hash
john --show flag.hash
```

## Настройка размера словаря

```bash
docker run -it --rm -e WORDLIST_SIZE=50000 kali-bruteforce /task/bruteforce_turbo.sh
```






