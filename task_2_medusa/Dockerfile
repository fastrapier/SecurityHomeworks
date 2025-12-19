FROM kalilinux/kali-rolling

# Обновление системы и установка необходимых пакетов
RUN apt-get update && \
    apt-get install -y \
    medusa \
    openssh-server \
    wordlists \
    procps \
    netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Распаковка rockyou.txt если он запакован
RUN if [ -f /usr/share/wordlists/rockyou.txt.gz ]; then \
        gunzip /usr/share/wordlists/rockyou.txt.gz; \
    fi

# Создание директории для SSH
RUN mkdir -p /var/run/sshd /root/.ssh

# Настройка SSH для разрешения аутентификации по паролю
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    echo "PermitEmptyPasswords no" >> /etc/ssh/sshd_config

# Создаём рабочую директорию
WORKDIR /task

# Копируем скрипты
COPY setup.sh /task/
COPY medusa_bruteforce.sh /task/
COPY entrypoint.sh /task/
COPY wordlist.txt /task/

# Даём права на выполнение
RUN chmod +x /task/*.sh

# Информация о контейнере
LABEL description="Kali Linux container для брутфорса SSH с помощью Medusa"
LABEL author="Студеникин Даниил 11-312"

# Открываем порт SSH
EXPOSE 22

# Автоматический запуск
ENTRYPOINT ["./entrypoint.sh"]

