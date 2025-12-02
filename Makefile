up:
	docker compose up --build

down:
	docker compose down


backends:
	docker compose --profile backends up --build

ui:
	docker compose --profile ui up --build


.PHONY: up down
