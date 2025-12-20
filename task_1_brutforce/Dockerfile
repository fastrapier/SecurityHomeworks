FROM kalilinux/kali-rolling

# Обновление системы и установка необходимых пакетов
RUN apt-get update && \
    apt-get install -y \
    john \
    john-data \
    p7zip-full \
    wordlists \
    perl \
    libcompress-raw-lzma-perl \
    ocl-icd-libopencl1 \
    opencl-headers \
    clinfo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Распаковка rockyou.txt если он сжат
RUN if [ -f /usr/share/wordlists/rockyou.txt.gz ]; then \
        gunzip /usr/share/wordlists/rockyou.txt.gz; \
    fi

# Создаём рабочую директорию
WORKDIR /task

# Копируем только необходимые файлы
COPY flag.7z /task/
COPY bruteforce.sh /task/
COPY bruteforce_turbo.sh /task/

# Даём права на выполнение скриптов
RUN chmod +x /task/bruteforce.sh /task/bruteforce_turbo.sh

# Информация о контейнере
LABEL description="Kali Linux container для брутфорса 7z архива с помощью John The Ripper"
LABEL author="Студеникин Даниил 11-312"

# Автоматический запуск брутфорса при старте контейнера
CMD ["./bruteforce.sh"]

