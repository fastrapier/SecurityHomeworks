FROM python:3.11-slim
# Метаданные
LABEL description="Windows Killer - File Masquerading Demo (MITRE ATT&CK T1036)"
LABEL maintainer="Studenikin Daniil"
# Создание рабочей директории
WORKDIR /task
# Копирование скрипта
COPY killer.py /task/
# Создание поддельных системных директорий
RUN mkdir -p /fake_system32 /fake_program_files /fake_windows
# Права на выполнение
RUN chmod +x /task/killer.py
# Запуск скрипта при старте контейнера
CMD ["python3", "/task/killer.py"]
