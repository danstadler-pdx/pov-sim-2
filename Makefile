setup:
	@chmod +x scripts/setup.sh && scripts/setup.sh

up:
	docker compose up --build

down:
	docker compose down


backends:
	docker compose --profile backends up --build

ui:
	docker compose --profile ui up --build


.PHONY: setup up down
