build:
	docker build . --tag ee-bot
run:
	docker run -d --name EEbot ee-bot
clean:
	docker stop EEbot
	docker rm EEbot
restart:
	docker restart EEbot
