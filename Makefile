include .env

up:
	docker-compose up -d --build

down:
	docker-compose down -v

stop:
	docker-compose stop app

start:
	docker-compose start app 

restart:
	docker-compose restart app

prod_db:
	docker-compose exec -it prod psql -h localhost -U ${DB_USER} -d ${PROD_DB}

test_db:
	docker-compose exec -it test psql -h localhost -U ${DB_USER} -d ${TEST_DB}

ps:
	docker-compose ps -a

create_tables:
	docker-compose exec -T prod psql -U root -d prod < create_tables.sql
	docker-compose exec -T test psql -U root -d test < create_tables.sql

make run:
	uv run python main.py
