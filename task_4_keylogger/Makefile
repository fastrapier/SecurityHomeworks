.PHONY: install run test clean help

help:
	@echo "Доступные команды:"
	@echo "  make install  - Установить зависимости"
	@echo "  make run      - Запустить keylogger"
	@echo "  make test     - Тестовый запуск (CI режим, 10 секунд)"
	@echo "  make clean    - Удалить лог-файл"

install:
	@echo "Установка зависимостей..."
	pip install -r requirements.txt

run:
	@echo "Запуск keylogger..."
	python3 keylogger.py

test:
	@echo "Тестовый запуск в CI режиме (10 секунд)..."
	CI_MODE=true python3 keylogger.py &
	@sleep 10
	@echo "Тестовый запуск завершен"

clean:
	@echo "Очистка лог-файлов..."
	-rm -f /tmp/keydemo.log
	-rm -f C:\\temp\\keydemo.log 2>/dev/null || true
	@echo "Очистка завершена"

