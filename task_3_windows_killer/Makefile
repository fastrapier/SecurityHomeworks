.PHONY: build run clean all help
IMAGE_NAME = windows-killer
all: build run
build:
	@echo "Сборка Docker образа..."
	docker build -t $(IMAGE_NAME) .
run:
	@echo "Запуск демонстрации Windows Killer..."
	docker run -it --rm $(IMAGE_NAME)
clean:
	@echo "Очистка контейнеров и образа..."
	-docker rm $$(docker ps -a -q --filter ancestor=$(IMAGE_NAME)) 2>/dev/null
	-docker rmi $(IMAGE_NAME) 2>/dev/null
	@echo "Очистка завершена"
help:
	@echo "Доступные команды:"
	@echo "  make build  - Собрать Docker образ"
	@echo "  make run    - Запустить демонстрацию"
	@echo "  make all    - Собрать и запустить"
	@echo "  make clean  - Удалить контейнеры и образ"
