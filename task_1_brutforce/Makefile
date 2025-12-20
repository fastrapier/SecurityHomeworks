.PHONY: build run turbo quick full clean all help

IMAGE_NAME = kali-bruteforce

all: build run

build:
	@echo "Сборка Docker образа..."
	docker build -t $(IMAGE_NAME) .

run:
	@echo "Запуск брутфорса (интерактивный режим)..."
	docker run -it $(IMAGE_NAME)

turbo:
	@echo "Запуск турбо-режима (топ 10K паролей)..."
	docker run -it --rm -e WORDLIST_SIZE=10000 $(IMAGE_NAME) /task/bruteforce_turbo.sh

quick:
	@echo "Запуск quick-режима (топ 100K паролей)..."
	docker run -it --rm -e WORDLIST_SIZE=100000 $(IMAGE_NAME) /task/bruteforce_turbo.sh

full:
	@echo "Запуск полного брутфорса (весь rockyou.txt)..."
	echo "2" | docker run -i --rm $(IMAGE_NAME)

clean:
	@echo "Очистка контейнеров и образа..."
	-docker rm $$(docker ps -a -q --filter ancestor=$(IMAGE_NAME)) 2>/dev/null
	-docker rmi $(IMAGE_NAME) 2>/dev/null
	@echo "Очистка завершена"

help:
	@echo "Доступные команды:"
	@echo "  make build  - Собрать Docker образ"
	@echo "  make run    - Интерактивный режим"
	@echo "  make turbo  - Топ 10K паролей (~3 мин)"
	@echo "  make quick  - Топ 100K паролей (~30 мин)"
	@echo "  make full   - Полный rockyou.txt"
	@echo "  make all    - Собрать и запустить"
	@echo "  make clean  - Удалить контейнеры и образ"

