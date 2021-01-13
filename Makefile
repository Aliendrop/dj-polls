BACK = back/
FRONT = front/
MANAGE = python $(BACK)manage.py


all: test

test:
	@$(MANAGE) test api polls --verbosity 0

dev:
	@$(MANAGE) runserver

mmg:
	@$(MANAGE) makemigrations

mg:
	@$(MANAGE) migrate

dev-up:
	docker-compose -f docker-compose.dev.yml up -d --build

vdev:
	@cd $(FRONT); npm run serve
